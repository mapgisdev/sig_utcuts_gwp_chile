# 04 — Arquitectura y stack tecnológico

## Arquitectura de alto nivel

```text
External Data Sources
        ↓
ETL / Data Processing
        ↓
PostgreSQL + PostGIS
        ↓
FastAPI Backend + Geospatial Services
        ↓
React Frontend + MapLibre + Dashboards
```

## Backend

Usar:

- Python 3.11+.
- FastAPI.
- SQLAlchemy.
- GeoAlchemy2.
- Pydantic.
- Alembic.
- JWT.
- Pytest.
- Uvicorn.

Carpetas sugeridas:

```text
backend/
├── app/
│   ├── api/
│   ├── core/
│   ├── db/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── etl/
│   ├── seed/
│   └── main.py
├── alembic/
├── tests/
├── requirements.txt
└── Dockerfile
```

## Frontend

Usar:

- React.
- TypeScript.
- Vite.
- Tailwind CSS.
- MapLibre GL JS.
- Recharts o ECharts.
- TanStack Table.
- React Router.
- Zustand.

Carpetas sugeridas:

```text
frontend/
├── src/
│   ├── api/
│   ├── components/
│   ├── features/
│   ├── layouts/
│   ├── pages/
│   ├── store/
│   ├── types/
│   ├── utils/
│   └── main.tsx
├── public/
├── package.json
└── Dockerfile
```

## Base de datos

Usar PostgreSQL + PostGIS.

Schemas recomendados:

- core;
- auth;
- geo;
- finance;
- mrv;
- prioritization;
- metadata;
- audit.

## Docker Compose

Servicios mínimos:

- db: PostGIS.
- backend: FastAPI.
- frontend: Vite/React.

Servicio opcional:

- geoserver o pg_tileserv.

## Variables de entorno

Crear `.env.example`:

```text
POSTGRES_USER=sigutcuts
POSTGRES_PASSWORD=sigutcuts
POSTGRES_DB=sigutcuts
DATABASE_URL=postgresql://sigutcuts:sigutcuts@db:5432/sigutcuts
JWT_SECRET=change_me
BACKEND_CORS_ORIGINS=http://localhost:5173
VITE_API_BASE_URL=http://localhost:8000
```

## Reglas

- No usar secretos reales.
- Mantener código portable.
- No depender de servicios externos para que el MVP funcione.
- Todo dato inicial debe cargarse con seed scripts.
- El sistema debe ser modular para reemplazar datos demo por datos oficiales.
