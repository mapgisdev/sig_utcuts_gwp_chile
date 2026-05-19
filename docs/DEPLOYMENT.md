# Despliegue — SIG-UTCUTS Chile

## Despliegue local (Docker Compose)

```bash
cp .env.example .env
docker compose up --build
```

### URLs

| Servicio | URL |
|----------|-----|
| Frontend | http://localhost:5173 |
| Backend | http://localhost:8000 |
| API Docs | http://localhost:8000/docs |
| PostgreSQL | localhost:5432 |

## Verificar que funciona

1. Abrir http://localhost:8000/health → `{"status": "ok"}`
2. Abrir http://localhost:8000/docs → Swagger UI
3. Abrir http://localhost:5173 → Dashboard

## Detener

```bash
docker compose down
```

## Limpiar datos

```bash
docker compose down -v
```
