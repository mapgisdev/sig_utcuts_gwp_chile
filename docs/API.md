# API — SIG-UTCUTS Chile

## Base URL

`http://localhost:8000/api/v1`

## Documentación interactiva

Swagger UI: `http://localhost:8000/docs`

## Endpoints

### Health
- `GET /health` — Estado del servicio

### Auth
- `POST /api/v1/auth/login` — Iniciar sesión (OAuth2 form)
- `POST /api/v1/auth/register` — Registrar usuario
- `GET /api/v1/auth/me` — Usuario actual

### Dashboard
- `GET /api/v1/dashboard/summary` — KPIs nacionales

### Territorios
- `GET /api/v1/territories` — Listar (filtrar por type, parent_id)
- `GET /api/v1/territories/{id}` — Detalle
- `GET /api/v1/territories/{id}/geojson` — GeoJSON
- `GET /api/v1/territories/{id}/profile` — Perfil territorial
- `GET /api/v1/territories/geojson/all?type=commune` — FeatureCollection

### Mecanismos
- `GET /api/v1/mechanisms` — CRUD completo
- `GET /api/v1/mechanisms/{id}/projects` — Proyectos del mecanismo

### Proyectos
- `GET /api/v1/projects` — CRUD completo

### Inversiones
- `GET /api/v1/investments` — CRUD completo
- `GET /api/v1/investments/summary/by-source` — Por fuente
- `GET /api/v1/investments/summary/by-region` — Por región

### MRV
- `GET /api/v1/mrv/indicators` — Indicadores
- `GET/POST /api/v1/mrv/observations` — Observaciones
- `GET /api/v1/mrv/summary` — Resumen

### Priorización
- `GET /api/v1/prioritization/ranking` — Ranking
- `POST /api/v1/prioritization/calculate` — Recalcular con pesos

### Calidad de Datos
- `GET /api/v1/data-quality/flags` — Flags
- `GET /api/v1/data-quality/summary` — Resumen

### Reportes
- `GET /api/v1/reports/national` — Nacional
- `GET /api/v1/reports/mrv` — MRV
- `GET /api/v1/reports/data-gaps` — Brechas
