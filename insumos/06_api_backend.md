# 06 — API backend

## Convenciones

- Base URL local: `http://localhost:8000/api/v1`.
- Formato: JSON.
- Autenticación: JWT.
- Geometrías: GeoJSON.
- Fechas: ISO 8601.
- Coordenadas: EPSG:4326.

## Endpoints generales

```text
GET /health
GET /api/v1/dashboard/summary
```

## Auth

```text
POST /api/v1/auth/login
POST /api/v1/auth/register
GET  /api/v1/auth/me
POST /api/v1/auth/logout
```

## Territorios

```text
GET /api/v1/territories
GET /api/v1/territories/{id}
GET /api/v1/territories/{id}/profile
GET /api/v1/territories/{id}/geojson
GET /api/v1/territories?type=region
GET /api/v1/territories?type=commune
```

## Capas

```text
GET /api/v1/layers
GET /api/v1/layers/{id}
GET /api/v1/layers/{id}/geojson
POST /api/v1/layers
PUT /api/v1/layers/{id}
DELETE /api/v1/layers/{id}
```

## Mecanismos

```text
GET /api/v1/mechanisms
GET /api/v1/mechanisms/{id}
POST /api/v1/mechanisms
PUT /api/v1/mechanisms/{id}
DELETE /api/v1/mechanisms/{id}
GET /api/v1/mechanisms/{id}/projects
GET /api/v1/mechanisms/{id}/territories
```

## Proyectos

```text
GET /api/v1/projects
GET /api/v1/projects/{id}
POST /api/v1/projects
PUT /api/v1/projects/{id}
DELETE /api/v1/projects/{id}
GET /api/v1/projects/{id}/mrv
GET /api/v1/projects/{id}/investments
GET /api/v1/projects/{id}/interventions
```

## Inversiones

```text
GET /api/v1/investments
GET /api/v1/investments/{id}
POST /api/v1/investments
PUT /api/v1/investments/{id}
DELETE /api/v1/investments/{id}
GET /api/v1/investments/summary/by-region
GET /api/v1/investments/summary/by-source
GET /api/v1/investments/summary/by-intervention
```

## Intervenciones

```text
GET /api/v1/interventions
GET /api/v1/interventions/{id}
POST /api/v1/interventions
PUT /api/v1/interventions/{id}
DELETE /api/v1/interventions/{id}
GET /api/v1/interventions/{id}/geojson
```

## MRV

```text
GET /api/v1/mrv/indicators
POST /api/v1/mrv/indicators
GET /api/v1/mrv/observations
POST /api/v1/mrv/observations
PUT /api/v1/mrv/observations/{id}
GET /api/v1/mrv/project/{project_id}
GET /api/v1/mrv/summary
```

## Priorización

```text
GET /api/v1/prioritization/ranking
GET /api/v1/prioritization/territory/{territory_id}
POST /api/v1/prioritization/scenarios
GET /api/v1/prioritization/scenarios/{id}
POST /api/v1/prioritization/calculate
```

## Brechas de información

```text
GET /api/v1/data-quality/flags
GET /api/v1/data-quality/summary
POST /api/v1/data-quality/flags
PUT /api/v1/data-quality/flags/{id}/resolve
```

## Reportes

```text
GET /api/v1/reports/national
GET /api/v1/reports/region/{region_id}
GET /api/v1/reports/commune/{commune_id}
GET /api/v1/reports/mechanism/{mechanism_id}
GET /api/v1/reports/project/{project_id}
GET /api/v1/reports/mrv
GET /api/v1/reports/data-gaps
```

## Evidencia

```text
POST /api/v1/evidence/upload
GET /api/v1/evidence/{id}
DELETE /api/v1/evidence/{id}
```

## Respuesta estándar de error

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Required field is missing",
    "details": {}
  }
}
```

## Respuesta dashboard summary

```json
{
  "total_investment_usd": 0,
  "public_investment_usd": 0,
  "private_investment_usd": 0,
  "international_investment_usd": 0,
  "mechanisms_count": 10,
  "projects_count": 0,
  "territories_count": 0,
  "estimated_hectares": 0,
  "verified_hectares": 0,
  "estimated_tco2e": 0,
  "verified_tco2e": 0,
  "data_gaps_count": 0
}
```
