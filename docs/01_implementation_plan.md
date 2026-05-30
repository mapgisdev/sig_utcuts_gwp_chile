# Plan de Implementación — SIG-UTCUTS Chile

## 1. Objetivo del Sistema

Desarrollar una plataforma SIG web de inteligencia territorial para visualizar, registrar, analizar y priorizar inversiones, mecanismos financieros e iniciativas vinculadas al sector UTCUTS (Uso de la Tierra, Cambio de Uso de la Tierra y Silvicultura) en Chile. El sistema integra información financiera, ambiental, climática, territorial y programática para apoyar decisiones, MRV y cierre de brechas frente a metas NDC.

---

## 2. Módulos del Sistema

| Módulo | Descripción |
|--------|-------------|
| **Dashboard Ejecutivo** | KPIs nacionales, gráficos de inversión, ranking territorial, alertas |
| **Visor Cartográfico** | MapLibre GL JS con capas activables, coropletas, fichas contextuales |
| **Catálogo de Mecanismos** | 10 mecanismos financieros UTCUTS con fichas detalladas |
| **Inversiones y Proyectos** | CRUD de proyectos, inversiones, asociación a mecanismos y territorios |
| **Priorización Territorial** | Índice multicriterio configurable por comuna con escenarios |
| **MRV** | Indicadores estimados/verificados, avances financieros y físicos |
| **Brechas de Información** | Detección automática de datos faltantes, semáforos de calidad |
| **Reportes** | Nacional, regional, comunal, por mecanismo, proyecto, MRV, brechas |
| **Administración** | Usuarios, roles, catálogos, capas, fuentes de datos, bitácora |
| **Autenticación** | JWT con 6 roles (public_viewer → admin) |

---

## 3. Arquitectura de Alto Nivel

```text
┌─────────────────────────────────────────────┐
│           Fuentes de Datos Externas          │
│  (CONAF, IDE Chile, ARClim, MapBiomas, etc.) │
└──────────────────┬──────────────────────────┘
                   ↓
┌──────────────────────────────────────────────┐
│            ETL / Data Processing             │
│         (Python: GeoPandas, Shapely)         │
└──────────────────┬──────────────────────────┘
                   ↓
┌──────────────────────────────────────────────┐
│          PostgreSQL 15 + PostGIS 3           │
│   Schemas: core, auth, geo, finance, mrv,   │
│            prioritization, metadata, audit   │
└──────────────────┬──────────────────────────┘
                   ↓
┌──────────────────────────────────────────────┐
│       Backend: FastAPI + SQLAlchemy          │
│   GeoAlchemy2, Pydantic, Alembic, JWT       │
│          Uvicorn (port 8000)                 │
└──────────────────┬──────────────────────────┘
                   ↓
┌──────────────────────────────────────────────┐
│       Frontend: React + TypeScript + Vite    │
│   Tailwind CSS, MapLibre GL JS, Recharts    │
│   TanStack Table, Zustand, React Router     │
│          Dev server (port 5173)              │
└─────────────────────────────────────────────┘
```

### Infraestructura Docker Compose

| Servicio | Imagen | Puerto |
|----------|--------|--------|
| `db` | postgis/postgis:15-3.3 | 5432 |
| `backend` | python:3.11-slim (custom) | 8000 |
| `frontend` | node:20-alpine (custom) | 5173 |

---

## 4. Estructura de Carpetas

```text
sig_utcuts_gwp_chile/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── auth.py
│   │   │       ├── dashboard.py
│   │   │       ├── territories.py
│   │   │       ├── layers.py
│   │   │       ├── mechanisms.py
│   │   │       ├── projects.py
│   │   │       ├── investments.py
│   │   │       ├── interventions.py
│   │   │       ├── mrv.py
│   │   │       ├── prioritization.py
│   │   │       ├── data_quality.py
│   │   │       ├── reports.py
│   │   │       └── evidence.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   │   └── deps.py
│   │   ├── db/
│   │   │   ├── base.py
│   │   │   └── session.py
│   │   ├── models/
│   │   │   ├── territory.py
│   │   │   ├── mechanism.py
│   │   │   ├── project.py
│   │   │   ├── investment.py
│   │   │   ├── intervention.py
│   │   │   ├── mrv.py
│   │   │   ├── prioritization.py
│   │   │   ├── data_quality.py
│   │   │   ├── layer.py
│   │   │   ├── evidence.py
│   │   │   ├── user.py
│   │   │   └── audit.py
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── seed/
│   │   └── main.py
│   ├── alembic/
│   ├── tests/
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   ├── components/
│   │   ├── features/
│   │   ├── layouts/
│   │   ├── pages/
│   │   ├── store/
│   │   ├── types/
│   │   ├── utils/
│   │   └── main.tsx
│   ├── public/
│   ├── package.json
│   └── Dockerfile
├── data/
│   ├── raw/
│   ├── processed/
│   ├── sample/
│   └── exports/
├── docs/
├── docker-compose.yml
├── .env.example
├── README.md
└── README_DEV.md
```

---

## 5. Entidades de Datos (19 tablas)

| Entidad | Tabla | Schema |
|---------|-------|--------|
| Territory | `territories` | geo |
| Watershed | `watersheds` | geo |
| ProtectedArea | `protected_areas` | geo |
| DataSource | `data_sources` | metadata |
| Layer | `layers` | geo |
| Mechanism | `mechanisms` | core |
| Project | `projects` | core |
| Investment | `investments` | finance |
| Intervention | `interventions` | core |
| InterventionGeometry | `intervention_geometries` | geo |
| MRVIndicator | `mrv_indicators` | mrv |
| MRVObservation | `mrv_observations` | mrv |
| EvidenceFile | `evidence_files` | core |
| DataQualityFlag | `data_quality_flags` | metadata |
| PrioritizationVariable | `prioritization_variables` | prioritization |
| PrioritizationScore | `prioritization_scores` | prioritization |
| User | `users` | auth |
| Role | `roles` | auth |
| AuditLog | `audit_logs` | audit |

### Relaciones Clave

```text
Mechanism 1───n Project
Project 1───n Investment
Project 1───n Intervention
Intervention 1───n InterventionGeometry
Intervention 1───n MRVObservation
MRVObservation n───1 MRVIndicator
Project n───n Territory
Project n───n EvidenceFile
Territory 1───n PrioritizationScore
DataSource 1───n Layer
```

---

## 6. Endpoints API

### Base URL: `http://localhost:8000/api/v1`

| Grupo | Endpoints principales |
|-------|----------------------|
| Health | `GET /health` |
| Auth | `POST /auth/login`, `POST /auth/register`, `GET /auth/me` |
| Dashboard | `GET /dashboard/summary` |
| Territories | `GET /territories`, `GET /territories/{id}`, `GET /territories/{id}/geojson` |
| Layers | `GET /layers`, CRUD completo |
| Mechanisms | `GET /mechanisms`, CRUD completo, `GET /mechanisms/{id}/projects` |
| Projects | `GET /projects`, CRUD completo, `GET /projects/{id}/mrv` |
| Investments | `GET /investments`, CRUD completo, sumarios por región/fuente/intervención |
| Interventions | `GET /interventions`, CRUD completo, `GET /interventions/{id}/geojson` |
| MRV | `GET /mrv/indicators`, `POST /mrv/observations`, `GET /mrv/summary` |
| Prioritization | `GET /prioritization/ranking`, `POST /prioritization/calculate`, escenarios |
| Data Quality | `GET /data-quality/flags`, `GET /data-quality/summary` |
| Reports | Nacional, regional, comunal, mecanismo, proyecto, MRV, brechas |
| Evidence | `POST /evidence/upload`, `GET /evidence/{id}` |

**Total: ~60 endpoints**

---

## 7. Pantallas Frontend

| # | Pantalla | Componentes principales |
|---|----------|------------------------|
| 1 | **Inicio / Dashboard** | KPIs, mini-mapa, gráficos de inversión, ranking, alertas |
| 2 | **Mapa** | MapLibre, panel capas, fichas, leyenda, filtros |
| 3 | **Mecanismos** | Tarjetas, filtros, ficha detallada, comparación |
| 4 | **Inversiones** | Tabla filtrable, formularios CRUD, exportación |
| 5 | **Priorización** | Sliders de pesos, mapa coropletas, tabla ranking |
| 6 | **MRV** | Proyectos, indicadores, avance, evidencia, verificación |
| 7 | **Brechas** | Resumen, tabla por tipo, semáforos, resolución |
| 8 | **Reportes** | Selector, previsualización, descarga PDF/CSV |
| 9 | **Administración** | Usuarios, roles, catálogos, capas, fuentes, bitácora |
| 10 | **Login** | Formulario autenticación |

---

## 8. Prioridades MVP

### Orden de implementación

1. **Infraestructura**: Docker Compose, DB, backend base, frontend base
2. **Dashboard**: KPIs y gráficos nacionales
3. **Mapa**: Visor con capas demo, coropletas
4. **Mecanismos**: Catálogo de 10 mecanismos
5. **Inversiones**: CRUD básico con tabla
6. **Priorización**: Cálculo multicriterio por comuna
7. **MRV**: Registro básico de indicadores
8. **Brechas**: Detección automática de flags
9. **Reportes**: Descarga CSV/PDF básico
10. **Admin**: Gestión de usuarios básica

---

## 9. Datos Semilla (Demo)

| Dato | Cantidad |
|------|----------|
| Regiones | 4 (Coquimbo, Valparaíso, Maule, Biobío) |
| Comunas | 8 (2 por región) |
| Mecanismos | 10 |
| Proyectos | 6 |
| Inversiones | 12 |
| Intervenciones | 8 |
| Indicadores MRV | 15 |
| Observaciones MRV | 20 |
| Brechas/flags | 10 |
| Usuarios demo | 3 (admin, editor, viewer) |

Todos los datos marcados como `is_sample = true` o `data_confidence = "demo"`.

---

## 10. Secuencia de Desarrollo (10 Fases)

### Fase 1 ✅ — Comprensión
- Lectura de insumos
- Generación de este plan

### Fase 2 ✅ — Scaffolding
- Estructura del monorepo
- Docker Compose
- `.env.example`
- Dockerfiles
- README_DEV.md

### Fase 3 ✅ — Base de Datos
- Modelos SQLAlchemy + GeoAlchemy2
- Migraciones Alembic
- Script de inicialización de schemas
- Seed data con geometrías simplificadas

### Fase 4 ✅ — Backend API
- Autenticación JWT
- CRUD de todas las entidades
- Endpoints de dashboard
- Endpoints geoespaciales (GeoJSON)
- Servicios de priorización y MRV

### Fase 5 ✅ — Frontend Base
- Layout principal con sidebar
- React Router
- Zustand stores
- Componentes base (tarjetas, tablas, formularios)
- Todas las pantallas

### Fase 6 ✅ — SIG / Mapa
- MapLibre integrado
- Capas GeoJSON desde backend
- Coropletas por prioridad/inversión
- Click → ficha territorial
- Control de capas y leyenda

### Fase 7 ✅ — Priorización
- Cálculo multicriterio con pesos configurables
- Normalización 0–100
- Clasificación 5 niveles
- Escenarios guardables
- Explicabilidad del puntaje

### Fase 8 ✅ — MRV
- Indicadores por categoría
- Observaciones estimado/verificado
- Evidencia asociada
- Estados de verificación
- Dashboard de avance

### Fase 9 ✅ — Testing
- Backend: health, auth, CRUD, dashboard, priorización, GeoJSON
- Frontend: render básico, navegación, dashboard
- Integración: seed data, docker compose

### Fase 10 ✅ — Documentación
- README.md
- README_DEV.md
- docs/ARCHITECTURE.md
- docs/API.md
- docs/DATA_MODEL.md
- docs/USER_GUIDE.md
- docs/DEPLOYMENT.md
- docs/NEXT_STEPS.md

---

## 11. Riesgos y Mitigaciones

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|-------------|---------|------------|
| Geometrías pesadas ralentizan frontend | Alta | Alto | Simplificar con tolerance, servir GeoJSON livianos |
| PostGIS no disponible en dev | Media | Alto | Docker Compose con imagen postgis oficial |
| Complejidad de 19 entidades | Media | Medio | Implementar incrementalmente, priorizar MVP |
| Autenticación JWT compleja | Baja | Medio | Implementación mínima viable con roles básicos |
| Datos semilla insuficientes | Baja | Bajo | Crear script de seed extensible |
| Rendimiento de coropletas | Media | Medio | Limitar features, usar simplificación geométrica |

---

## 12. Estrategia de Testing

### Backend (Pytest)
- `test_health.py` — `/health` responde 200
- `test_auth.py` — login, registro, token
- `test_mechanisms.py` — CRUD mecanismos
- `test_dashboard.py` — summary con datos
- `test_prioritization.py` — cálculo de puntajes
- `test_geojson.py` — endpoints GeoJSON
- `test_data_quality.py` — flags de calidad

### Frontend (Vitest)
- `App.test.tsx` — render sin errores
- `Dashboard.test.tsx` — render con datos mock
- `Navigation.test.tsx` — rutas principales

---

## 13. Criterios de Aceptación

- [x] `docker compose up --build` levanta la aplicación
- [x] Backend responde en `GET /health`
- [x] Documentación API abre en `/docs`
- [x] Frontend abre correctamente en `localhost:5173`
- [x] Mapa renderiza geometrías de ejemplo
- [x] Dashboard muestra KPIs con datos demo
- [x] Mecanismos se consultan en catálogo
- [x] Se puede registrar una inversión demo
- [x] Se calcula ranking territorial
- [x] Se registra un indicador MRV
- [x] Se visualizan brechas de información
- [x] Tests mínimos pasan
- [x] Documentación completa
