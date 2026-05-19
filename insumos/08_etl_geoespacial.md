# 08 — ETL geoespacial

## Objetivo

Definir cómo integrar, limpiar, normalizar y publicar datos geoespaciales y financieros.

## Principios

- Separar datos brutos de datos procesados.
- Mantener metadatos de fuente.
- Registrar fecha de descarga.
- Registrar licencia.
- Registrar escala y resolución.
- No mezclar datos oficiales con datos demo sin marcar.
- Validar geometrías.
- Simplificar capas pesadas para web.

## Carpetas sugeridas

```text
data/
├── raw/
├── processed/
├── sample/
├── external/
└── exports/
```

## Proceso ETL general

```text
Extract
→ Validate
→ Normalize
→ Transform
→ Load
→ Publish
→ Document
```

## Extract

Fuentes posibles:

- CSV.
- XLSX.
- GeoJSON.
- SHP.
- WMS/WFS.
- APIs JSON.
- Descargas manuales.

## Validate

Validar:

- existencia de campos obligatorios;
- geometrías válidas;
- sistema de referencia;
- duplicados;
- valores nulos;
- rangos numéricos;
- códigos territoriales;
- consistencia de fechas.

## Normalize

Normalizar:

- nombres de regiones y comunas;
- códigos territoriales;
- monedas;
- años;
- categorías de intervención;
- fuentes de financiamiento;
- nivel de precisión geográfica.

## Transform

Transformaciones:

- reproyección a EPSG:4326;
- simplificación geométrica para web;
- cálculo de área en hectáreas;
- agregación por comuna/región;
- join espacial;
- cálculo de indicadores;
- normalización 0–100 para priorización.

## Load

Cargar en PostGIS:

- territorios;
- capas;
- inversiones;
- mecanismos;
- intervenciones;
- indicadores;
- puntajes de priorización.

## Publish

Publicar mediante:

- endpoints GeoJSON;
- WMS/WFS opcional;
- tiles opcionales;
- API REST.

## ETL mínimos del MVP

Crear scripts:

```text
backend/app/etl/load_sample_territories.py
backend/app/etl/load_sample_mechanisms.py
backend/app/etl/load_sample_projects.py
backend/app/etl/calculate_prioritization.py
backend/app/etl/check_data_quality.py
```

## Datos semilla

Crear datos demo para:

- 4 regiones de ejemplo;
- 8 comunas de ejemplo;
- 10 mecanismos;
- 6 proyectos demo;
- inversiones demo;
- intervenciones demo;
- indicadores MRV demo;
- brechas demo.

## Reglas de geometría

- Usar EPSG:4326 en frontend y API.
- Validar geometrías antes de guardar.
- Calcular áreas usando proyección adecuada internamente si es necesario.
- Mostrar advertencia si la geometría es aproximada.
- No usar geometrías de alta complejidad en el frontend sin simplificación.

## Metadatos de capas

Cada capa debe registrar:

- name;
- description;
- institution;
- source_url;
- license;
- update_frequency;
- last_downloaded;
- spatial_resolution;
- temporal_resolution;
- geometry_type;
- is_official;
- is_sample;
- processing_notes.
