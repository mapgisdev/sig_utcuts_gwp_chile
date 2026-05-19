# SIG-UTCUTS Chile

## Plataforma de Inteligencia Territorial para Inversiones, Mecanismos Financieros, Priorización y MRV del Sector UTCUTS en Chile

### Descripción

SIG-UTCUTS Chile es una plataforma web geoespacial para visualizar, registrar, analizar y priorizar inversiones, mecanismos financieros e iniciativas vinculadas al sector UTCUTS (Uso de la Tierra, Cambio de Uso de la Tierra y Silvicultura) en Chile.

### Características principales

- 📊 **Dashboard ejecutivo** con KPIs nacionales
- 🗺️ **Visor cartográfico** interactivo con MapLibre GL JS
- ⚙️ **Catálogo de mecanismos** financieros (10 mecanismos UTCUTS)
- 💰 **Registro de inversiones** y proyectos
- 🎯 **Priorización territorial** multicriterio configurable
- 📋 **MRV** — Monitoreo, Reporte y Verificación
- ⚠️ **Brechas de información** con semáforos de calidad
- 📄 **Reportes** descargables
- 🔐 **Autenticación** JWT con roles

### Stack tecnológico

| Componente | Tecnología |
|-----------|-----------|
| Frontend | React 18 + TypeScript + Vite + Tailwind CSS |
| Backend | Python 3.11 + FastAPI + SQLAlchemy + GeoAlchemy2 |
| Base de datos | PostgreSQL 15 + PostGIS 3 |
| Mapa | MapLibre GL JS |
| Gráficos | Recharts |
| Estado | Zustand |
| Contenedores | Docker Compose |

### Inicio rápido

```bash
# 1. Copiar variables de entorno
cp .env.example .env

# 2. Levantar servicios
docker compose up --build

# 3. Acceder
# Frontend: http://localhost:5173
# Backend:  http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Usuarios demo

| Usuario | Contraseña | Rol |
|---------|-----------|-----|
| admin | admin123 | Administrador |
| editor | editor123 | Editor |
| viewer | viewer123 | Visor público |

### Documentación

- [Plan de implementación](docs/01_implementation_plan.md)
- [Guía de desarrollo](README_DEV.md)

### Datos

Todos los datos incluidos son **sintéticos (demo)** y no representan información oficial. Están marcados con `is_sample = true`.

### Licencia

Proyecto desarrollado para GWP Chile. Consultar términos de uso.
