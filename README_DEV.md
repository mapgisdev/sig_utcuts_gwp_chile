# Guía de Desarrollo — SIG-UTCUTS Chile

## Requisitos previos

- Docker y Docker Compose
- Node.js 20+ (para desarrollo local del frontend)
- Python 3.11+ (para desarrollo local del backend)

## Estructura del proyecto

```text
sig_utcuts_gwp_chile/
├── backend/          # FastAPI + SQLAlchemy + GeoAlchemy2
├── frontend/         # React + TypeScript + Vite + Tailwind
├── data/             # Datos raw, procesados, sample
├── docs/             # Documentación
├── insumos/          # Especificaciones funcionales
├── docker-compose.yml
├── .env.example
└── README.md
```

## Desarrollo con Docker

```bash
cp .env.example .env
docker compose up --build
```

## Desarrollo local (sin Docker)

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Tests

```bash
cd backend
pytest tests/ -v
```

## Base de datos

La base de datos se crea automáticamente al iniciar el backend. Las tablas y datos semilla se cargan mediante el lifespan de FastAPI.

## Variables de entorno

Revisar `.env.example` para todas las variables configurables.

## Convenciones de código

- **Código**: Nombres en inglés
- **Interfaz**: Textos en español
- **Documentación**: En español
- **Datos demo**: Marcados como `is_sample = true`
