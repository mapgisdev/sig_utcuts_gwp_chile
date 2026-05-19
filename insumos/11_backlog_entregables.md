# 11 — Backlog y entregables

## Épica 1 — Scaffolding

Historias:

- Crear estructura del monorepo.
- Configurar Docker Compose.
- Crear backend FastAPI.
- Crear frontend React.
- Crear PostGIS.
- Crear `.env.example`.
- Crear documentación inicial.

## Épica 2 — Base de datos

Historias:

- Crear modelos territoriales.
- Crear modelos de mecanismos.
- Crear modelos de proyectos.
- Crear modelos financieros.
- Crear modelos MRV.
- Crear modelos de priorización.
- Crear modelos de brechas.
- Crear migraciones.
- Crear seeds.

## Épica 3 — Backend API

Historias:

- Healthcheck.
- Auth.
- CRUD mecanismos.
- CRUD proyectos.
- CRUD inversiones.
- CRUD intervenciones.
- Endpoints territorios.
- Endpoints capas.
- Endpoints dashboard.
- Endpoints priorización.
- Endpoints MRV.
- Endpoints brechas.
- Endpoints reportes.

## Épica 4 — Frontend

Historias:

- Layout principal.
- Sidebar/menu.
- Dashboard.
- Mapa.
- Catálogo de mecanismos.
- Tabla de inversiones.
- Formularios.
- Priorización.
- MRV.
- Brechas.
- Reportes.
- Administración básica.

## Épica 5 — Geoespacial

Historias:

- Cargar GeoJSON demo.
- Servir GeoJSON desde backend.
- Renderizar polígonos en MapLibre.
- Coropletas por prioridad.
- Clic en territorio.
- Panel de atributos.
- Control de capas.
- Leyenda.

## Épica 6 — Priorización

Historias:

- Definir variables demo.
- Normalizar 0–100.
- Aplicar pesos.
- Calcular puntaje.
- Clasificar prioridad.
- Guardar escenario.
- Mostrar explicación.
- Exportar ranking.

## Épica 7 — MRV

Historias:

- Crear indicadores.
- Registrar observaciones.
- Asociar evidencia.
- Separar estimado/verificado.
- Mostrar avance.
- Validar estado.
- Exportar reporte.

## Épica 8 — Calidad de datos

Historias:

- Crear flags.
- Detectar faltantes.
- Mostrar resumen.
- Resolver brechas.
- Exportar reporte.

## Épica 9 — Testing

Historias:

- Tests backend.
- Tests frontend básicos.
- Test seed data.
- Test docker compose.
- Test priorización.

## Entregables

1. Código fuente.
2. Docker Compose.
3. Base de datos inicial.
4. Datos demo.
5. API documentada.
6. Frontend funcional.
7. Mapa funcional.
8. Dashboard.
9. Catálogo.
10. Priorización.
11. MRV.
12. Brechas.
13. Reportes básicos.
14. Documentación.
15. Pruebas.

## Prioridad MVP

Debe implementarse primero:

1. Dashboard.
2. Mapa.
3. Mecanismos.
4. Inversiones.
5. Priorización.
6. MRV básico.
7. Brechas.
