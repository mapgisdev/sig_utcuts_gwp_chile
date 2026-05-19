# Arquitectura — SIG-UTCUTS Chile

## Diagrama de alto nivel

```text
┌──────────────────────────────────────────────┐
│       Frontend: React + TypeScript + Vite    │
│   Tailwind CSS, MapLibre GL JS, Recharts     │
│          http://localhost:5173                │
└──────────────────┬───────────────────────────┘
                   │ REST API (JSON/GeoJSON)
                   ↓
┌──────────────────────────────────────────────┐
│       Backend: FastAPI + SQLAlchemy          │
│   GeoAlchemy2, Pydantic, JWT Auth            │
│          http://localhost:8000               │
└──────────────────┬───────────────────────────┘
                   │ SQL + PostGIS
                   ↓
┌──────────────────────────────────────────────┐
│          PostgreSQL 15 + PostGIS 3           │
│          localhost:5432                       │
└──────────────────────────────────────────────┘
```

## Módulos del Backend

| Módulo | Responsabilidad |
|--------|----------------|
| `api/v1/` | Endpoints REST |
| `core/` | Config, seguridad, dependencias |
| `models/` | Modelos SQLAlchemy + GeoAlchemy2 |
| `schemas/` | Validación Pydantic |
| `seed/` | Datos demo |
| `services/` | Lógica de negocio |

## Módulos del Frontend

| Módulo | Responsabilidad |
|--------|----------------|
| `pages/` | Pantallas principales |
| `layouts/` | Layout con sidebar |
| `api/` | Cliente Axios |
| `store/` | Estado Zustand |
| `components/` | Componentes reutilizables |

## Schemas de Base de Datos

Todas las tablas están en el schema `public` para simplificar el MVP. Futuras versiones pueden separar en: core, auth, geo, finance, mrv, prioritization, metadata, audit.

## Autenticación

JWT con tokens Bearer. 6 roles jerárquicos: public_viewer → institutional_viewer → analyst → editor → validator → admin.
