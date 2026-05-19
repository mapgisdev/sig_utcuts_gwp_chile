# Modelo de Datos — SIG-UTCUTS Chile

## Entidades (19 tablas)

### Territoriales
- **territories** — Regiones, comunas, país (jerárquica con parent_id, geometría PostGIS)
- **data_sources** — Fuentes de datos oficiales y sus estados de integración
- **layers** — Capas geoespaciales configurables

### Mecanismos y Proyectos
- **mechanisms** — 10 mecanismos financieros UTCUTS
- **projects** — Proyectos con nivel de precisión y confianza
- **investments** — Flujos financieros con fuente, monto, moneda, año
- **interventions** — Acciones físicas (restauración, forestación, conservación...)
- **intervention_geometries** — Geometrías opcionales por intervención

### MRV
- **mrv_indicators** — 15 indicadores en 7 categorías
- **mrv_observations** — Valores estimados vs verificados

### Calidad y Priorización
- **data_quality_flags** — 9 tipos de brechas de información
- **prioritization_scores** — 8 criterios ponderados con clasificación 5 niveles

### Auth y Auditoría
- **users** / **roles** / **user_roles** — 6 roles jerárquicos
- **evidence_files** — Documentos de soporte
- **audit_logs** — Bitácora de acciones

## Reglas clave
- Geometrías en EPSG:4326
- Datos demo marcados con `is_sample = true`
- Valores estimados y verificados separados en MRV
- Nivel de confianza en inversiones y proyectos
