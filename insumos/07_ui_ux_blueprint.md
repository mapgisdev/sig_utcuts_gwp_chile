# 07 — UI/UX blueprint

## Idioma de interfaz

Todos los textos visibles para usuarios deben estar en español.

## Estilo visual

- Interfaz limpia, institucional y técnica.
- Diseño sobrio.
- Uso de tarjetas, mapas, tablas y gráficos.
- Colores sugeridos:
  - Verde: bosque/restauración.
  - Azul: agua/clima.
  - Naranja/rojo: riesgo/incendios/brechas.
  - Gris: datos incompletos.
- Debe funcionar en escritorio y tablet.

## Navegación principal

```text
Inicio
Mapa
Mecanismos
Inversiones
Priorización
MRV
Brechas
Reportes
Administración
```

## Pantalla Inicio

Componentes:

- Título del sistema.
- KPIs nacionales.
- Mapa pequeño resumen.
- Gráfico de inversión por fuente.
- Gráfico de inversión por intervención.
- Ranking de territorios prioritarios.
- Alertas de brechas.
- Accesos rápidos.

## Pantalla Mapa

Layout:

```text
Topbar: búsqueda, filtros globales, usuario

Left panel:
- Capas base
- Capas forestales
- Capas climáticas
- Capas biodiversidad
- Capas financieras
- Priorización

Center:
- Mapa interactivo

Right panel:
- Ficha del elemento seleccionado
- Indicadores
- Acciones

Bottom:
- Leyenda
- Escala
- Coordenadas
- Exportar
```

Funciones:

- activar/desactivar capas;
- cambiar opacidad;
- consultar atributos;
- filtrar inversiones;
- ver ficha territorial;
- exportar vista.

## Pantalla Mecanismos

Vista de tarjetas con:

- nombre;
- categoría;
- fuente financiera;
- plazo;
- estado;
- intervención principal;
- botón “Ver ficha”.

Ficha:

- descripción;
- actores;
- beneficiarios;
- condiciones habilitantes;
- indicadores;
- territorios potenciales;
- proyectos asociados;
- documentos.

## Pantalla Inversiones

Tabla con filtros:

- nombre;
- mecanismo;
- fuente;
- monto;
- moneda;
- año;
- región;
- comuna;
- intervención;
- precisión geográfica;
- confianza;
- estado.

Acciones:

- crear;
- editar;
- ver;
- exportar;
- enviar a validación.

## Pantalla Priorización

Componentes:

- selector de escenario;
- sliders de ponderación;
- mapa de prioridad;
- tabla ranking;
- explicación del puntaje;
- mecanismos recomendados;
- botón recalcular;
- botón exportar.

## Pantalla MRV

Componentes:

- lista de proyectos;
- avance financiero;
- avance físico;
- indicadores climáticos;
- indicadores sociales;
- evidencia;
- estado de verificación;
- línea de tiempo.

## Pantalla Brechas

Componentes:

- resumen de brechas;
- tabla por tipo de brecha;
- semáforos;
- filtros por entidad;
- acciones de resolución;
- exportar reporte.

## Pantalla Reportes

Reportes disponibles:

- nacional;
- regional;
- comunal;
- mecanismo;
- proyecto;
- MRV;
- brechas.

Cada reporte debe poder previsualizarse y descargarse.

## Accesibilidad

- Buen contraste.
- Tamaños legibles.
- Botones claros.
- Navegación por teclado cuando sea posible.
- Mensajes de error comprensibles.

## Estados vacíos

Todas las pantallas deben tener estados vacíos elegantes:

- “No hay datos cargados todavía”.
- “No se encontraron resultados con estos filtros”.
- “Este registro no tiene geometría asociada”.
- “Este indicador aún no ha sido verificado”.
