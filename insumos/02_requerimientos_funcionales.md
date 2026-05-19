# 02 — Requerimientos funcionales

## RF-01 Dashboard ejecutivo

El sistema debe mostrar:

- inversión total documentada;
- inversión por fuente;
- inversión por tipo de intervención;
- número de mecanismos;
- número de proyectos;
- número de territorios cubiertos;
- brecha financiera estimada;
- hectáreas estimadas y verificadas;
- tCO2e estimadas y verificadas;
- alertas de datos incompletos;
- ranking de territorios prioritarios.

## RF-02 Visor cartográfico

El sistema debe permitir:

- visualizar mapa base;
- activar y desactivar capas;
- consultar atributos por clic;
- filtrar por región, comuna, cuenca, mecanismo, intervención y fuente financiera;
- mostrar inversiones agregadas;
- mostrar capas ambientales;
- representar coropletas de prioridad;
- exportar mapa como imagen o PDF básico;
- mostrar leyendas dinámicas.

## RF-03 Catálogo de mecanismos

El sistema debe permitir:

- listar mecanismos;
- filtrar por categoría, fuente, plazo, madurez, beneficiario y NDC;
- ver ficha detallada;
- asociar mecanismos a territorios potenciales;
- asociar documentos;
- comparar mecanismos.

## RF-04 Registro de proyectos e inversiones

El sistema debe permitir:

- crear proyecto;
- asociarlo a mecanismo;
- registrar fuente financiera;
- registrar monto, moneda, año;
- clasificar intervención UTCUTS;
- asignar territorio;
- cargar geometría opcional;
- cargar evidencia;
- definir nivel de precisión geográfica;
- definir nivel de confianza;
- editar registros;
- enviar a validación;
- aprobar o rechazar.

## RF-05 Priorización territorial

El sistema debe:

- calcular puntaje multicriterio por comuna;
- permitir modificar pesos;
- guardar escenarios;
- clasificar prioridades;
- mostrar explicación del puntaje;
- recomendar mecanismos aplicables;
- exportar ranking.

## RF-06 MRV

El sistema debe registrar:

- avances financieros;
- avances físicos;
- hectáreas estimadas y verificadas;
- tCO2e estimadas y verificadas;
- beneficiarios estimados y verificados;
- evidencia;
- estado de verificación;
- observaciones.

## RF-07 Brechas de información

El sistema debe identificar:

- registros sin geometría;
- registros sin monto;
- registros sin fuente;
- registros sin año;
- registros con baja confianza;
- registros estimados;
- registros sin indicadores físicos;
- registros sin indicadores climáticos;
- posibles duplicados.

## RF-08 Reportes

El sistema debe generar:

- reporte nacional;
- reporte regional;
- reporte comunal;
- reporte por mecanismo;
- reporte por proyecto;
- reporte MRV;
- reporte de brechas.

Formatos mínimos:

- PDF básico.
- CSV.
- XLSX si es viable.
- GeoJSON para geometrías.

## RF-09 Administración

El sistema debe permitir:

- gestionar usuarios;
- gestionar roles;
- gestionar catálogos;
- gestionar capas;
- gestionar fuentes de datos;
- revisar bitácora.

## RF-10 Autenticación

Roles mínimos:

- public_viewer;
- institutional_viewer;
- analyst;
- editor;
- validator;
- admin.
