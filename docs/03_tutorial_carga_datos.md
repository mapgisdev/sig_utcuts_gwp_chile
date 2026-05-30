# Guía de Ingesta de Datos Adicionales e Integración de Prioridades
## SIG-UTCUTS Chile

Esta guía proporciona el procedimiento paso a paso para alimentar y actualizar el sistema con nuevas fuentes de datos geográficos (ej. capas de CONAF, Banco Integrado de Proyectos - BIP, etc.) y cómo el motor de priorización dinámico normaliza y recalcula automáticamente los pesos basándose únicamente en los datos disponibles.

---

## 1. Arquitectura de Datos Territoriales

En SIG-UTCUTS Chile, el repositorio central de geometrías es la tabla `territories`. Esta tabla almacena de forma nativa objetos espaciales indexados con PostGIS (SRID 4326):

*   **Comunas (`type = 'commune'`)**
*   **Regiones (`type = 'region'`)**
*   **Áreas Protegidas y ECMPOs (`type = 'protected_area'`)**
*   **Capas Adicionales (`type = 'custom_layer'`)**

### Estructura de la Tabla `territories`

*   `id` (Integer, Primary Key)
*   `code` (String, Unique) — Ej: `AP-0021` (Área Protegida) o `11101` (Código Comunal CUD)
*   `name` (String) — Nombre oficial del territorio.
*   `type` (String) — Tipo de territorio (ej. `commune`, `region`, `protected_area`, `conaf_layer`).
*   `area_ha` (Float) — Superficie calculada en hectáreas.
*   `geom` (Geometry, SRID: 4326) — Objeto geométrico nativo (MultiPolygon).
*   `parent_id` (Integer, Foreign Key) — Referencia jerárquica (ej. Comuna -> Región).

---

## 2. Ingesta de Nuevas Capas Espaciales

Para cargar un nuevo archivo GeoJSON o Shapefile en la base de datos, se debe crear un script de ingesta en Python que se ejecute en el contenedor `sigutcuts_backend`.

### Estructura del Script de Ingesta (`backend/scripts/load_custom_layer.py`)

A continuación se presenta una plantilla optimizada que incluye:
1. Conversión de coordenadas a EPSG:4326.
2. Reparación topológica automática (`ST_Buffer(geom, 0)`).
3. Transaccionalidad segura en SQLAlchemy.

```python
import os
import sys
import json
from shapely.geometry import shape, MultiPolygon
from sqlalchemy import text

# Agregar el path del backend para importar dependencias
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.db.session import SessionLocal
from app.models.territory import Territory

def load_new_layer(geojson_path, layer_type_name):
    db = SessionLocal()
    try:
        print(f"Cargando archivo {geojson_path}...")
        with open(geojson_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        features = data.get("features", [])
        print(f"Detectados {len(features)} polígonos en el archivo.")

        count = 0
        for idx, feat in enumerate(features):
            properties = feat.get("properties", {})
            geometry = feat.get("geometry")

            if not geometry:
                continue

            # Extraer atributos útiles
            name = properties.get("NOM_CAPA") or properties.get("name") or f"Polígono {idx}"
            code = properties.get("COD_CAPA") or f"CUSTOM-{idx:04d}"
            area = properties.get("AREA_HA") or properties.get("shape_area") or 0.0

            # Convertir geometría a WKT
            geom_shapely = shape(geometry)
            if not isinstance(geom_shapely, MultiPolygon):
                geom_shapely = MultiPolygon([geom_shapely])
            wkt_geom = geom_shapely.wkt

            # Crear registro temporal
            new_item = Territory(
                code=code,
                name=name,
                type=layer_type_name,
                area_ha=float(area),
            )
            db.add(new_item)
            db.flush() # Obtener el ID autogenerado

            # Insertar la geometría nativa de forma segura con PostGIS
            db.execute(
                text("UPDATE territories SET geom = ST_GeomFromText(:wkt, 4326) WHERE id = :id"),
                {"wkt": wkt_geom, "id": new_item.id}
            )
            count += 1

        db.commit()
        print(f"[OK] Ingestados exitosamente {count} registros de la capa '{layer_type_name}'.")

        # Limpiar y validar geometrías
        print("Optimizando geometrías en base de datos...")
        db.execute(text("UPDATE territories SET geom = ST_Buffer(geom, 0) WHERE type = :t AND geom IS NOT NULL AND NOT ST_IsValid(geom)"), {"t": layer_type_name})
        db.execute(text("CREATE INDEX IF NOT EXISTS territories_geom_gist_idx ON territories USING gist(geom)"))
        db.commit()
        print("[OK] Reparación de geometrías y actualización de índice espacial finalizados.")

    except Exception as e:
        db.rollback()
        print(f"Error al ingestar capa: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    # Ruta del archivo montado en el contenedor
    geojson_file = "/insumos/datos_geo/descargas/conaf_capas.geojson"
    load_new_layer(geojson_file, "conaf_layer")
```

Para correr este cargador en producción local:
```bash
docker exec -i sigutcuts_backend python /app/scripts/load_custom_layer.py
```

---

## 3. Funcionamiento de la Priorización Multicriterio Dinámica

El motor de priorización de SIG-UTCUTS Chile implementa **normalización adaptativa multicriterio**. Si una comuna o el sistema completo no dispone de datos de algún criterio, el software **no asigna puntajes ficticios ni penaliza**, sino que **redistribuye los pesos de forma proporcional** únicamente entre los criterios que sí cuentan con datos reales (es decir, aquellos cuyo valor en base de datos no es `None` o `Null`).

### Algoritmo de Cálculo Dinámico en la API

La lógica está escrita en [`prioritization_router.py`](file:///d:/web_D_anctigravity/sig_utcuts_gwp_chile/backend/app/api/v1/prioritization_router.py). Supongamos que el usuario define los siguientes pesos en la interfaz:
*   Potencial de Restauración: `0.20`
*   Riesgo Climático (ARClim): `0.15`
*   Riesgo de Degradación: `0.15`
*   Brecha Financiera: `0.15`
*   Valor de Biodiversidad: `0.10`
*   Vulnerabilidad Social: `0.10`
*   Factibilidad Operativa: `0.10`
*   Alineación con Mecanismos: `0.05`

Si una comuna solo cuenta con datos reales de **Riesgo Climático** e **Intersección de Biodiversidad** en la base de datos (y los otros 6 campos están en `Null/None`):

1.  El motor recopila los valores disponibles:
    *   $\text{Score}_{\text{Clima}} = 75.0$
    *   $\text{Score}_{\text{Biodiversidad}} = 100.0$
2.  Recupera los pesos de los criterios válidos:
    *   $\text{Peso}_{\text{Clima}} = 0.15$
    *   $\text{Peso}_{\text{Biodiversidad}} = 0.10$
3.  Calcula el denominador de normalización:
    *   $\text{Suma de Pesos} = 0.15 + 0.10 = 0.25$
4.  Aplica el promedio ponderado normalizado:
    $$Score_{Total} = \frac{(0.15 \times 75.0) + (0.10 \times 100.0)}{0.25} = \frac{11.25 + 10.00}{0.25} = 85.0$$

De esta forma, la comuna obtiene un puntaje final real de **85.0** (Prioridad Muy Alta), sin verse afectada por la ausencia de otros criterios que todavía no han sido catastrados en su zona geográfica.

---

## 4. SQL de Diagnóstico y Monitoreo Espacial

Puedes conectarte a la base de datos PostGIS para auditar las capas cargadas y diagnosticar errores usando la consola o scripts interactivos:

```bash
docker exec -it sigutcuts_db psql -U sigutcuts -d sigutcuts
```

### Consultas Útiles de Diagnóstico

#### Contar registros por tipo de capa cargada
```sql
SELECT type, count(*), sum(area_ha) as area_total_ha 
FROM territories 
GROUP BY type;
```

#### Identificar geometrías inválidas
```sql
SELECT id, code, name 
FROM territories 
WHERE geom IS NOT NULL AND NOT ST_IsValid(geom);
```

#### Reparar geometrías inválidas en masa
```sql
UPDATE territories 
SET geom = ST_Buffer(geom, 0) 
WHERE geom IS NOT NULL AND NOT ST_IsValid(geom);
```

#### Probar intersección espacial rápida entre una comuna y la capa CONAF
```sql
SELECT c.name as comuna, conaf.name as elemento_conaf
FROM territories c
JOIN territories conaf ON conaf.type = 'conaf_layer'
WHERE c.type = 'commune'
  AND c.name = 'Aysén'
  AND ST_Intersects(c.geom, conaf.geom);
```
