# 10 — Seguridad, testing y despliegue

## Seguridad

### Principios

- No guardar secretos en el repositorio.
- Usar `.env.example`.
- Usar JWT.
- Validar inputs.
- Sanitizar cargas.
- Limitar tipos de archivos.
- Registrar auditoría.
- Separar roles.
- No permitir operaciones destructivas masivas sin confirmación.

### Roles

| Rol | Permisos |
|---|---|
| public_viewer | Ver información pública |
| institutional_viewer | Ver información institucional ampliada |
| analyst | Crear escenarios y reportes |
| editor | Crear y editar registros |
| validator | Validar registros y geometrías |
| admin | Administrar usuarios, catálogos y sistema |

### Permisos mínimos

- Solo `admin` gestiona usuarios.
- Solo `editor`, `validator` y `admin` crean o editan proyectos.
- Solo `validator` y `admin` aprueban datos.
- Solo `admin` elimina registros.
- Eliminaciones deben ser soft delete cuando sea posible.

## Testing

### Backend

Usar Pytest.

Pruebas mínimas:

- `/health`.
- login.
- listar mecanismos.
- crear proyecto.
- listar inversiones.
- obtener dashboard.
- calcular priorización.
- listar brechas.
- servir GeoJSON.

### Frontend

Usar Vitest/React Testing Library si es viable.

Pruebas mínimas:

- render de App.
- navegación principal.
- render de dashboard.
- render de tabla de mecanismos.
- render de mapa sin fallos.

### Integración

Probar:

- frontend consume backend.
- backend conecta a DB.
- seed data carga correctamente.
- docker compose levanta servicios.

## Despliegue local

Comando esperado:

```bash
docker compose up --build
```

URLs esperadas:

```text
Frontend: http://localhost:5173
Backend:  http://localhost:8000
Docs API: http://localhost:8000/docs
DB:       localhost:5432
```

## Documentación obligatoria

Crear:

- `README.md`.
- `README_DEV.md`.
- `docs/ARCHITECTURE.md`.
- `docs/API.md`.
- `docs/DATA_MODEL.md`.
- `docs/USER_GUIDE.md`.
- `docs/DEPLOYMENT.md`.
- `docs/NEXT_STEPS.md`.

## Criterios de aceptación

La app está lista si:

1. Docker Compose levanta los servicios.
2. El backend responde en `/health`.
3. La documentación API abre en `/docs`.
4. El frontend abre correctamente.
5. El mapa renderiza geometrías demo.
6. El dashboard muestra datos demo.
7. Se puede listar mecanismos.
8. Se puede crear una inversión demo.
9. Se puede calcular priorización.
10. Se puede registrar MRV.
11. Se pueden ver brechas.
12. Hay pruebas mínimas.
