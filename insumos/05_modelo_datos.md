# 05 — Modelo de datos

## Entidades principales

1. Territory.
2. Watershed.
3. ProtectedArea.
4. DataSource.
5. Layer.
6. Mechanism.
7. Project.
8. Investment.
9. Intervention.
10. InterventionGeometry.
11. MRVIndicator.
12. MRVObservation.
13. EvidenceFile.
14. DataQualityFlag.
15. PrioritizationVariable.
16. PrioritizationScore.
17. User.
18. Role.
19. AuditLog.

## Relación conceptual

```text
Mechanism 1---n Project
Project 1---n Investment
Project 1---n Intervention
Intervention 1---n InterventionGeometry
Intervention 1---n MRVObservation
MRVObservation n---1 MRVIndicator
Project n---n Territory
Project n---n EvidenceFile
Territory 1---n PrioritizationScore
DataSource 1---n Layer
```

## Territorios

Tabla: `territories`

Campos:

- id;
- code;
- name;
- type: country, macrozone, region, province, commune, watershed, protected_area;
- parent_id;
- geom;
- area_ha;
- source_id;
- created_at;
- updated_at.

## Mecanismos

Tabla: `mechanisms`

Campos:

- id;
- code;
- name;
- category;
- description;
- main_funding_source;
- maturity_level;
- time_horizon;
- ndc_alignment;
- target_beneficiaries;
- enabling_conditions;
- status;
- created_at;
- updated_at.

Mecanismos iniciales:

1. Actualización Ley de Bosque Nativo.
2. Nueva Ley de Fomento a la Forestación Mixta.
3. Ampliación Ley de Donaciones hacia Bosques Naturales.
4. Vincular Manejo de Bosque Nativo al Impuesto Verde.
5. Bancos de Compensación de Biodiversidad.
6. Bancos de Compensación Privados / Murallas Verdes.
7. Fomento al Bosque Nativo / Modelo Simbiótico.
8. Billetera Digital de Carbono Campesino.
9. Cuadrillas Municipales de Prevención y Combate de Incendios.
10. Aportes Presupuestarios + Fondos Climáticos Internacionales.

## Proyectos

Tabla: `projects`

Campos:

- id;
- mechanism_id;
- name;
- description;
- start_year;
- end_year;
- status;
- geographic_precision;
- data_confidence;
- source_reference;
- created_by;
- created_at;
- updated_at.

## Inversiones

Tabla: `investments`

Campos:

- id;
- project_id;
- funding_source_id;
- amount;
- currency;
- amount_usd;
- year;
- financial_instrument;
- approved_amount;
- executed_amount;
- committed_amount;
- source_document;
- data_quality;
- created_at.

## Intervenciones

Tabla: `interventions`

Campos:

- id;
- project_id;
- intervention_type;
- ndc_component;
- hectares_estimated;
- hectares_verified;
- tco2e_estimated;
- tco2e_verified;
- beneficiaries_estimated;
- beneficiaries_verified;
- status;
- verification_status;
- created_at.

## Geometrías

Tabla: `intervention_geometries`

Campos:

- id;
- intervention_id;
- geometry_type;
- territory_id;
- geom;
- precision_level;
- source;
- validated;
- created_at.

## Indicadores MRV

Tabla: `mrv_indicators`

Campos:

- id;
- code;
- name;
- category: financial, physical, climate, social, biodiversity;
- unit;
- description;
- calculation_method;
- created_at.

## Observaciones MRV

Tabla: `mrv_observations`

Campos:

- id;
- intervention_id;
- indicator_id;
- estimated_value;
- verified_value;
- observation_date;
- verification_status;
- evidence_file_id;
- notes;
- created_at.

## Calidad de datos

Tabla: `data_quality_flags`

Campos:

- id;
- entity_type;
- entity_id;
- flag_type;
- severity;
- description;
- resolved;
- created_at;
- resolved_at.

Flag types:

- missing_geometry;
- missing_amount;
- missing_source;
- missing_year;
- low_confidence;
- estimated_value;
- missing_physical_indicator;
- missing_climate_indicator;
- possible_duplicate.

## Priorización

Tabla: `prioritization_scores`

Campos:

- id;
- territory_id;
- scenario_name;
- score_total;
- score_forest;
- score_restoration;
- score_climate_risk;
- score_biodiversity;
- score_social;
- score_financial_gap;
- score_accessibility;
- priority_class;
- calculated_at.

## Autenticación

Tablas:

- users;
- roles;
- user_roles.

Roles:

- public_viewer;
- institutional_viewer;
- analyst;
- editor;
- validator;
- admin.
