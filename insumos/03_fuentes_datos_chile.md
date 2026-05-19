# 03 — Fuentes de datos clave para Chile

## Propósito

Este archivo define las fuentes de datos que la aplicación debe considerar para el diseño de conectores, ETL, capas y catálogos. En el MVP se pueden usar datos semilla, pero la arquitectura debe estar preparada para estas fuentes.

## Fuentes territoriales base

### IDE Chile / Geoportal
Uso:
- división político-administrativa;
- regiones;
- provincias;
- comunas;
- metadatos oficiales;
- servicios WMS/WFS cuando estén disponibles.

### SUBDERE / IDE SUBDERE
Uso:
- inversión territorial;
- información regional y municipal;
- límites y planificación territorial.

### INE / Censo
Uso:
- población;
- hogares;
- ruralidad;
- indicadores sociodemográficos;
- relación con beneficiarios potenciales.

## Fuentes forestales y uso de suelo

### CONAF / SIT CONAF
Uso:
- catastro de uso de suelo y vegetación;
- bosque nativo;
- plantaciones;
- tipos forestales;
- capas forestales institucionales.

### IDE MINAGRI
Uso:
- suelos;
- información agrícola;
- recuperación de suelos degradados;
- riego;
- variables agroclimáticas;
- datos CIREN, ODEPA, INFOR, SAG, CNR.

### CIREN / ODEPA
Uso:
- catastro frutícola;
- suelos;
- erosión;
- aptitud productiva;
- presión agroproductiva.

## Fuentes biodiversidad

### MMA / SIMBIO / SBAP
Uso:
- áreas protegidas;
- sitios prioritarios;
- humedales;
- ecosistemas;
- especies;
- restauración ecológica;
- biodiversidad.

### Líneas de Base Públicas MMA
Uso:
- datos descargables en SHP/GeoJSON;
- áreas protegidas;
- humedales;
- sitios prioritarios.

### Pisos vegetacionales Luebert y Pliscoff
Uso:
- clasificación ecológica;
- estratificación por ecosistema;
- representatividad de inversiones por ecosistema.

## Fuentes climáticas e hídricas

### ARClim
Uso:
- riesgo climático;
- sequía;
- temperatura;
- precipitación;
- exposición;
- sensibilidad;
- riesgo por comuna o cuenca.

### DGA / SNIA
Uso:
- caudales;
- estaciones;
- agua;
- cuencas;
- disponibilidad hídrica.

### CR2
Uso:
- datos climáticos históricos;
- precipitación;
- temperatura;
- sequía;
- cuencas.

### MeteoChile
Uso:
- estaciones meteorológicas;
- precipitación;
- temperatura;
- sequía;
- eventos extremos.

## Fuentes satelitales y cambio de cobertura

### MapBiomas Chile
Uso:
- serie temporal de cobertura 1999–2024 o posteriores;
- cambio de uso;
- pérdida y ganancia;
- análisis por comuna, cuenca o región.

### Global Forest Watch
Uso:
- pérdida de cobertura arbórea;
- validación cruzada;
- alertas globales.

### NASA FIRMS
Uso:
- focos de calor;
- incendios activos;
- presión por fuego.

### Copernicus
Uso:
- cobertura de suelo;
- vegetación;
- agua;
- productos globales complementarios.

## Fuentes financieras

### BIP / Sistema Nacional de Inversiones
Uso:
- proyectos de inversión pública;
- códigos BIP;
- sector;
- región/comuna;
- costos;
- estado.

### DIPRES
Uso:
- presupuesto público;
- ejecución presupuestaria;
- asignaciones institucionales.

### ChileIndica
Uso:
- inversión regional;
- FNDR;
- proyectos territoriales.

### Cooperación internacional
Uso:
- GCF;
- GEF;
- Banco Mundial;
- FCPF;
- FAO;
- BID;
- PNUD;
- cooperación bilateral.

## Diseño de integración

Crear tabla `data_sources` con:

- name;
- institution;
- category;
- url;
- access_type;
- update_frequency;
- license;
- spatial_resolution;
- temporal_resolution;
- geometry_type;
- integration_status;
- notes.

## Estados de integración

- planned;
- manual_download;
- semi_automated;
- automated_api;
- wms_wfs;
- deprecated;
- unavailable.

## Importante

El MVP debe incluir la estructura para estas fuentes, aunque no todas se conecten en la primera versión.
