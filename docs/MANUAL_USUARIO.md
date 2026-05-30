# Manual de Usuario y Guía de Operación — SIG-UTCUTS Chile

Bienvenido al **Manual de Usuario de SIG-UTCUTS Chile**, la Plataforma de Inteligencia Territorial para Inversiones, Mecanismos Financieros, Priorización y Monitoreo (MRV) del sector de Uso de la Tierra, Cambio de Uso de la Tierra y Silvicultura (UTCUTS) en Chile.

Esta plataforma integra información geográfica, financiera y ambiental para apoyar la toma de decisiones estratégicas, el seguimiento de metas NDC y el cierre de brechas de información territorial.

---

## Índice
1. [Acceso e Inicio de Sesión](#1-acceso-e-inicio-de-sesión)
2. [Estructura General de la Interfaz](#2-estructura-general-de-la-interfaz)
3. [Módulo 1: Dashboard Ejecutivo](#3-módulo-1-dashboard-ejecutivo)
4. [Módulo 2: Visor Cartográfico (Mapa Interactivo)](#4-módulo-2-visor-cartográfico-mapa-interactivo)
5. [Módulo 3: Catálogo de Mecanismos Financieros](#5-módulo-3-catálogo-de-mecanismos-financieros)
6. [Módulo 4: Inversiones y Proyectos](#6-módulo-4-inversiones-y-proyectos)
7. [Módulo 5: Priorización Territorial Multicriterio](#7-módulo-5-priorización-territorial-multicriterio)
8. [Módulo 6: Monitoreo, Reporte y Verificación (MRV)](#8-módulo-6-monitoreo-reporte-y-verificación-mrv)
9. [Módulo 7: Brechas de Información y Calidad](#9-módulo-7-brechas-de-información-y-calidad)
10. [Módulo 8: Generación de Reportes](#10-módulo-8-generación-de-reportes)
11. [Módulo 9: Consola de Administración e Ingesta de Datos](#11-módulo-9-consola-de-administración-e-ingesta-de-datos)
12. [Administración Técnica: Carga de Capas GIS y Diagnósticos SQL](#12-administración-técnica-carga-de-capas-gis-y-diagnósticos-sql)

---

## 1. Acceso e Inicio de Sesión

Para ingresar al sistema:
1. Abra su navegador web e ingrese a la dirección: `http://localhost:5173` (o la URL de producción configurada).
2. Se le redirigirá a la pantalla de acceso.
3. Ingrese sus credenciales. La plataforma cuenta con tres perfiles demo preconfigurados para pruebas:

| Usuario | Contraseña | Rol / Nivel de Permiso | Descripción |
| :--- | :--- | :--- | :--- |
| **`admin`** | `admin123` | **Administrador** | Acceso total a todos los módulos y a la consola de administración e ingesta de datos. |
| **`editor`** | `editor123` | **Editor** | Permisos de lectura, edición y creación de proyectos e inversiones. |
| **`viewer`** | `viewer123` | **Visor Público** | Acceso de solo lectura para consulta de mapas, dashboard, mecanismos y reportes. |

> [!NOTE]
> El sistema de autenticación utiliza tokens JWT (JSON Web Tokens) que expiran automáticamente por seguridad.

---

## 2. Estructura General de la Interfaz

La interfaz de usuario ha sido diseñada bajo estándares premium de experiencia visual (oscuro elegante) y cuenta con una barra lateral izquierda de navegación que le permite alternar rápidamente entre los siguientes módulos:

*   **Dashboard (Inicio):** Vista global resumida.
*   **Mapa:** Visualizador geoespacial interactivo.
*   **Mecanismos:** Catálogo interactivo de instrumentos de financiamiento.
*   **Inversiones:** Listado y registro rápido de proyectos y flujos financieros.
*   **Priorización:** Motor dinámico de ponderación multicriterio por comuna.
*   **MRV:** Panel de seguimiento físico, financiero e impacto climático.
*   **Brechas:** Semáforos de calidad y completitud de datos de la plataforma.
*   **Reportes:** Exportador de datos sintéticos y resúmenes ejecutivos.
*   **Administración (Ingesta):** Panel avanzado para control de la base de datos central (exclusivo para perfiles Editor y Administrador).

---

## 3. Módulo 1: Dashboard Ejecutivo

Es la pantalla de bienvenida. Ofrece una vista panorámica nacional consolidada del sector UTCUTS mediante indicadores clave de rendimiento (KPIs) y gráficos interactivos.

### Elementos Principales:
1.  **KPIs Nacionales (Tarjetas de Datos):**
    *   **Inversión Total:** Monto acumulado invertido en el sector UTCUTS (expresado en millones de USD).
    *   **Inversión Pública:** Financiamiento proveniente del Estado chileno.
    *   **Inversión Internacional:** Aportes de fondos de cooperación global (ej. GEF, GCF).
    *   **Mecanismos:** Total de instrumentos financieros catastrados.
    *   **Proyectos:** Cantidad de proyectos activos o en ejecución.
    *   **Comunas:** Número de comunas cubiertas por alguna iniciativa.
    *   **Hectáreas Estimadas:** Meta total de superficie a intervenir (ha).
    *   **tCO₂e Estimadas:** Estimación de mitigación (toneladas de carbono equivalente).
2.  **Gráfico de Inversión por Fuente:** Un gráfico de torta dinámico que desglosa el porcentaje de inversión según su origen (público, privado, internacional, mixto).
3.  **Ranking Territorial:** Tabla interactiva con el top de comunas con mayores índices de prioridad del país, indicando su puntaje y clasificación cualitativa.
4.  **Alerta de Brechas:** Un banner de advertencia dinámico que se activa automáticamente si existen brechas de información críticas pendientes de resolver en la base de datos.

---

## 4. Módulo 2: Visor Cartográfico (Mapa Interactivo)

El visualizador cartográfico está desarrollado sobre **MapLibre GL JS**, ofreciendo un rendimiento óptimo de carga geométrica.

```
┌────────────────────────────────────────────────────────┐
│ [ Capas ]          MAPA INTERACTIVO (MAPLIBRE GL)      │
│  [x] Regiones      (Límites y coropletas de comunas)   │
│  [x] Comunas       ┌────────────────────────┐          │
│                    │ Ficha Territorial      │          │
│ [ Leyenda ]        │ Comuna: Aysén          │          │
│ Muy Alta  [■]      │ Prioridad: Muy Alta    │          │
│ Alta      [■]      │ Superficie: 50.000 ha  │          │
│ Media     [■]      └────────────────────────┘          │
└────────────────────────────────────────────────────────┘
```

### Funciones y Operaciones:
*   **Navegación:** Puede arrastrar el mapa para desplazarse, y usar la rueda del mouse o los controles del extremo superior derecho para hacer zoom.
*   **Panel de Capas (Izquierda):** Permite encender o apagar las capas vectoriales:
    *   **Regiones:** Delinea los límites oficiales de las 16 regiones de Chile.
    *   **Comunas (Prioridad):** Colorea cada comuna con base en su prioridad territorial calculada por el algoritmo dinámico de la plataforma.
*   **Leyenda de Priorización:**
    *   🟩 **Muy Alta** (Puntaje > 80)
    *   🟢 **Alta** (Puntaje 60 - 80)
    *   🟨 **Media** (Puntaje 40 - 60)
    *   🟧 **Baja** (Puntaje 20 - 40)
    *   🟥 **Muy Baja** (Puntaje < 20)
*   **Ficha Territorial Contextual:** Al hacer clic sobre cualquier comuna pintada, se desplegará en el costado derecho una tarjeta detallada con la información base del territorio:
    *   Nombre de la comuna y código nacional (CUD).
    *   Superficie total en hectáreas.
    *   Puntaje numérico exacto de prioridad (0.0 a 100.0).
    *   Clasificación de prioridad cualitativa.

---

## 5. Módulo 3: Catálogo de Mecanismos Financieros

Este módulo presenta los **10 mecanismos financieros UTCUTS** del sistema (ej. Fondo de Conservación de Bosque Nativo, Pago por Resultados REDD+, Bonos de Carbono, Donaciones GEF).

### Cómo Utilizarlo:
1.  **Exploración:** Navegue a través de la cuadrícula de tarjetas de mecanismos. Cada tarjeta muestra un resumen rápido del mecanismo.
2.  **Métricas Rápidas:** Identifique el nivel de madurez operativa (*Concept, Design, Pilot, Operational, Scaling*), la fuente principal de financiamiento (Pública/Privada/Internacional), los beneficiarios objetivo y su horizonte de ejecución (Corto, Mediano o Largo plazo).
3.  **Consulta de Ficha Completa:** Haga clic en cualquier tarjeta para abrir un modal de pantalla completa que detalla:
    *   Descripción detallada y objetivos del instrumento.
    *   Alineación específica con las metas NDC de Chile.
    *   Lógica y criterios de asignación del financiamiento.

---

## 6. Módulo 4: Inversiones y Proyectos

Permite visualizar la tabla maestra de flujos financieros y proyectos del sector.

### Operaciones Básicas:
1.  **Filtros y Tabla:** Revise el listado detallado de inversiones con información de ID, fuente financiadora, tipo (público/privado/internacional), monto en dólares (USD), año fiscal y etiqueta de calidad del dato.
2.  **Ingresar Nueva Inversión (Perfiles Editor y Admin):**
    *   Haga clic en el botón superior **`+ Nueva Inversión`**.
    *   Se abrirá un formulario rápido en pantalla.
    *   Complete los campos requeridos: *Fuente financiadora*, *Tipo*, *Monto (USD)* y *Año*.
    *   Haga clic en **`Guardar`**. Los datos se actualizarán automáticamente en la tabla principal y en los KPI del Dashboard.

---

## 7. Módulo 5: Priorización Territorial Multicriterio

Este módulo es una de las herramientas más potentes del sistema. Permite a los planificadores ajustar la importancia (peso) de diversos factores territoriales para recalcular qué comunas del país requieren mayor focalización de recursos UTCUTS.

### Criterios Ponderables (8 Variables):
1.  **Potencial de Restauración:** Capacidad o necesidad de recuperación de áreas forestales degradadas.
2.  **Riesgo Climático (ARClim):** Vulnerabilidad física ante el cambio climático.
3.  **Riesgo de Degradación/Pérdida:** Presión antrópica u forestal sobre el suelo.
4.  **Brecha Financiera:** Falta de inversión histórica registrada.
5.  **Valor de Biodiversidad:** Presencia de especies endémicas o alto valor ecológico.
6.  **Vulnerabilidad Social:** Índices socioeconómicos de la población local.
7.  **Factibilidad Operativa:** Accesibilidad y condiciones logísticas para ejecutar proyectos.
8.  **Alineación con Mecanismos:** Disponibilidad de instrumentos financieros compatibles.

### Procedimiento para Recalcular:
1.  En el panel **Ponderaciones**, desplace los controles deslizantes (*sliders*) de cada una de las 8 variables para aumentar o disminuir su peso relativo (de 0% a 50%).
2.  *Nota de validación:* Asegúrese de que la distribución sea equilibrada y responda a las prioridades de planificación del escenario.
3.  Haga clic en el botón **`🔄 Recalcular`**.
4.  El sistema ejecutará instantáneamente el algoritmo de normalización adaptativa en el backend y actualizará:
    *   El **gráfico de barras vertical** con el nuevo Top 10 de comunas prioritarias.
    *   La **tabla completa de resultados** con la clasificación ajustada y los puntajes finales recalibrados de 0 a 100.
    *   Los colores de prioridad en el mapa dinámico (Módulo 2).

> [!TIP]
> **¿Qué es la Normalización Adaptativa?**
> Si una comuna no posee datos de alguna variable específica en la base de datos, el algoritmo de la plataforma no la penaliza con un puntaje de cero. En su lugar, distribuye el peso de esa variable faltante de forma proporcional entre los criterios que sí cuentan con información real para esa comuna. De esta manera, el puntaje final siempre representa fielmente los datos disponibles.

---

## 8. Módulo 6: Monitoreo, Reporte y Verificación (MRV)

El módulo MRV realiza el seguimiento del impacto físico y ambiental real de los proyectos, contrastando las estimaciones de diseño contra los valores verificados en terreno.

### Componentes:
1.  **KPIs de Verificación:** Muestra el número total de observaciones registradas, cuántas han sido validadas (*verified*), cuántas se mantienen como estimaciones preliminares (*estimated*), y la **Tasa de Verificación** porcentual global.
2.  **Panel de Indicadores MRV:** Catálogo de indicadores técnicos clasificados por color según su categoría:
    *   🔵 **Físico (Physical):** Hectáreas conservadas, forestadas o manejadas.
    *   🟢 **Financiero (Financial):** Ejecución presupuestaria, costos por hectárea.
    *   🟡 **Climático (Climate):** Captura de CO₂e, reducción de emisiones.
    *   🟣 **Social (Social):** Empleos generados, participación comunitaria.
3.  **Tabla de Últimas Observaciones:** Registro histórico de mediciones de campo, detallando el valor estimado original y el valor verificado tras la auditoría en terreno, junto con el estado del registro (*verified* o *estimated*).

---

## 9. Módulo 7: Brechas de Información y Calidad

Este panel actúa como un auditor automático del inventario de datos, aplicando semáforos de calidad y listando alertas de inconsistencias u omisiones en los registros financieros y territoriales.

### Clasificación de Severidades:
*   🔴 **Critical:** Falta de información estructural que impide cálculos esenciales (ej. proyectos sin territorio asociado).
*   ❌ **Error:** Ausencia de datos financieros críticos (ej. inversiones sin monto registrado).
*   ⚠️ **Warning:** Datos con nivel de confianza subóptimo o inconsistencias menores (ej. proyectos que solo reportan valores estimados en MRV).
*   ℹ️ **Info:** Recordatorios generales de actualización.

### Tipos de Alertas Frecuentes (Flags):
*   `missing_geometry`: La intervención no posee delimitación espacial en el mapa.
*   `missing_amount`: El registro de inversión tiene valor en cero o nulo.
*   `low_confidence`: La fuente de datos del proyecto está catalogada como demo o de baja confianza.
*   `possible_duplicate`: Existen registros con nombres o coordenadas idénticas en la misma área.

---

## 10. Módulo 8: Generación de Reportes

Permite exportar y consultar compilados ejecutivos en tiempo real.

### Reportes Disponibles:
1.  **Reporte Nacional:** Resumen analítico consolidado de inversiones, total de proyectos activos y metas de mitigación estimadas a nivel nacional.
2.  **Reporte MRV:** Estado actual del proceso de verificación, detallando las brechas entre la planificación física y los avances validados en terreno por cada indicador.
3.  **Reporte de Brechas:** Lista oficial de flags de calidad de datos activos por entidad y severidad para coordinar labores de limpieza de información.

### Cómo Generar un Reporte:
1.  Haga clic sobre la tarjeta del reporte que desea generar.
2.  El sistema consultará los datos dinámicos mediante la API.
3.  En la sección inferior se previsualizará la estructura jerárquica de datos en formato interactivo lista para su validación o exportación externa.

---

## 11. Módulo 9: Consola de Administración e Ingesta de Datos

> [!IMPORTANT]
> Esta sección avanzada solo es accesible para perfiles con privilegios de **Editor** y **Administrador**. El botón de agregar y las opciones de edición/eliminación directa sobre los listados maestros están protegidos por roles jerárquicos a nivel de API.

La consola de administración unifica el ciclo de vida completo (CRUD) de la base de datos territorial a través de 6 pestañas principales:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ MÓDULO DE ADMINISTRACIÓN                                      [+ AGREGAR]   │
│ ┌─────────────┬───────────┬─────────────┬───────────────┬───────┬─────────┐ │
│ │ Mecanismos  │ Proyectos │ Inversiones │ Intervencion. │ MRV   │ Capas   │ │
│ └─────────────┴───────────┴─────────────┴───────────────┴───────┴─────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Gestión por Pestañas:
*   **Mecanismos:** Permite agregar o editar la codificación oficial de los 10 mecanismos, sus metas y estados operativos (`activo`/`inactivo`).
*   **Proyectos:** Administra los proyectos de mitigación. Cuenta con un **selector jerárquico de territorio** que permite asociar un proyecto de forma precisa a nivel de Región, Provincia y Comuna mediante menús desplegables en cascada.
*   **Inversiones:** Permite vincular flujos monetarios específicos a proyectos existentes, detallando la moneda, el origen público o privado del capital y el año fiscal de asignación.
*   **Intervenciones:** Administra las acciones físicas en el territorio (ej. reforestación comunitaria de bosque nativo), permitiendo registrar el balance de hectáreas y toneladas de carbono estimadas vs. verificadas.
*   **Monitoreo MRV:** Añade observaciones periódicas a las intervenciones, vinculándolas a los indicadores estandarizados de la plataforma.
*   **Capas GIS:** Registra metadatos de las capas de soporte geoespacial integradas (nombre, URL de la fuente de datos oficial y estado activo).

---

## 12. Administración Técnica: Carga de Capas GIS y Diagnósticos SQL

Para los ingenieros de sistemas o administradores de bases de datos geográficas, la plataforma cuenta con flujos optimizados de ingesta y validación de datos espaciales.

### Flujo de Preparación de Datos Geográficos (ETL)
Antes de incorporar nuevos archivos vectoriales (Shapefile o GeoJSON) en la base de datos, estos deben cumplir con las siguientes directrices en la carpeta [datos_geo](file:///d:/web_D_anctigravity/sig_utcuts_gwp_chile/insumos/datos_geo):

1.  **Proyección Espacial:** Todas las geometrías deben venir reproyectadas al sistema geográfico **`EPSG:4326`** (WGS 84).
2.  **Optimización Estructural:** Para archivos muy pesados (superiores a 15MB) destinados a visualización general en el navegador, se debe correr un script de simplificación geométrica para evitar la degradación de rendimiento de MapLibre en el cliente.

### Ejecución de Ingesta desde Consola Docker
Para cargar una nueva capa vectorial directamente en la base de datos PostGIS, monte el archivo en el contenedor y ejecute el cargador automatizado:

```powershell
docker exec -i sigutcuts_backend python /app/scripts/load_custom_layer.py
```

### Consultas SQL de Diagnóstico Frecuentes
Conéctese directamente al motor de base de datos relacional PostgreSQL con extensión PostGIS ejecutando:
```powershell
docker exec -it sigutcuts_db psql -U sigutcuts -d sigutcuts
```

A continuación, se listan consultas útiles para la auditoría de datos geoespaciales:

#### 1. Contar registros y superficie total por tipo de territorio cargado:
```sql
SELECT type, COUNT(*), SUM(area_ha) AS superficie_total_ha
FROM territories
GROUP BY type;
```

#### 2. Buscar y reportar polígonos que tengan errores de topología o geometrías inválidas:
```sql
SELECT id, code, name
FROM territories
WHERE geom IS NOT NULL AND NOT ST_IsValid(geom);
```

#### 3. Reparar geometrías inválidas de forma masiva (corrección de auto-intersección de anillos):
```sql
UPDATE territories
SET geom = ST_Buffer(geom, 0)
WHERE geom IS NOT NULL AND NOT ST_IsValid(geom);
```

#### 4. Realizar un cruce espacial rápido para detectar traslapes entre intervenciones y áreas silvestres protegidas:
```sql
SELECT 
    i.id AS intervencion_id,
    ap.name AS area_protegida,
    ST_Area(ST_Intersection(i.geom, ap.geom)::geography) / 10000 AS ha_traslapadas
FROM territories ap
JOIN territories i ON i.type = 'intervention_layer'
WHERE ap.type = 'protected_area'
  AND ST_Intersects(i.geom, ap.geom);
```

---
*Para soporte técnico, adición de usuarios o dudas de parametrización del modelo, contacte con el equipo de soporte de SIG-UTCUTS Chile.*
