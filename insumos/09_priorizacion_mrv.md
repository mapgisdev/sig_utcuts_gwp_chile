# 09 — Priorización territorial y MRV

## Priorización territorial

### Objetivo

Identificar territorios donde la inversión UTCUTS puede tener mayor impacto potencial.

### Unidad inicial

Comuna.

Posteriormente:

- región;
- cuenca;
- área protegida;
- polígono;
- predio.

### Variables del índice

1. Potencial forestal/restauración.
2. Riesgo climático.
3. Riesgo de degradación o pérdida.
4. Brecha financiera.
5. Valor de biodiversidad.
6. Vulnerabilidad social.
7. Factibilidad operativa.
8. Alineación con mecanismos existentes.

### Pesos por defecto

```text
forest_restoration_potential: 0.20
climate_risk: 0.15
degradation_loss_risk: 0.15
financial_gap: 0.15
biodiversity_value: 0.10
social_vulnerability: 0.10
operational_feasibility: 0.10
mechanism_alignment: 0.05
```

### Fórmula

```text
priority_score =
  0.20 * forest_restoration_potential
+ 0.15 * climate_risk
+ 0.15 * degradation_loss_risk
+ 0.15 * financial_gap
+ 0.10 * biodiversity_value
+ 0.10 * social_vulnerability
+ 0.10 * operational_feasibility
+ 0.05 * mechanism_alignment
```

### Normalización

Cada variable debe escalarse de 0 a 100.

### Clasificación

- 80–100: Muy alta.
- 60–79: Alta.
- 40–59: Media.
- 20–39: Baja.
- 0–19: Muy baja.

### Explicabilidad

El sistema debe mostrar por qué una comuna tiene cierto puntaje.

Ejemplo:

```text
Prioridad alta porque combina:
- alto potencial de restauración;
- riesgo climático medio-alto;
- baja inversión histórica;
- presencia de bosque nativo;
- buena factibilidad operativa.
```

### Escenarios

Crear escenarios:

- Restauración.
- Manejo de bosque nativo.
- Forestación.
- Reducción de deforestación.
- Incendios.
- Biodiversidad.
- Financiamiento socialmente justo.

Cada escenario puede modificar pesos.

## MRV

### Objetivo

Relacionar inversión con resultados financieros, físicos, climáticos, sociales y ambientales.

### Categorías de indicadores

1. Financieros.
2. Físicos.
3. Climáticos.
4. Sociales.
5. Biodiversidad.
6. Gobernanza.
7. Calidad de datos.

### Indicadores financieros

- monto aprobado;
- monto comprometido;
- monto ejecutado;
- porcentaje de ejecución;
- fuente de financiamiento;
- costo por hectárea;
- costo por tCO2e.

### Indicadores físicos

- hectáreas bajo manejo;
- hectáreas restauradas;
- hectáreas forestadas;
- hectáreas conservadas;
- hectáreas con prevención de incendios;
- número de predios;
- número de proyectos.

### Indicadores climáticos

- tCO2e estimadas;
- tCO2e verificadas;
- emisiones evitadas;
- carbono secuestrado;
- carbono protegido.

### Indicadores sociales

- beneficiarios estimados;
- beneficiarios verificados;
- pequeños propietarios;
- comunidades rurales;
- participación de mujeres;
- empleo generado.

### Indicadores de biodiversidad

- superficie en áreas protegidas;
- superficie en sitios prioritarios;
- ecosistemas cubiertos;
- restauración de hábitat;
- conectividad.

### Estados de verificación

- estimated;
- reported;
- under_review;
- verified;
- rejected;
- needs_evidence.

### Reglas MRV

1. Separar valores estimados y verificados.
2. Todo valor verificado requiere evidencia.
3. Toda evidencia debe registrar fuente, fecha y usuario.
4. Cada cambio debe quedar en auditoría.
5. El sistema debe mostrar nivel de confianza.
6. Los reportes deben indicar si los datos son oficiales, estimados o demo.
