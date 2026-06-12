# Metaheurísticas — Notebooks de Estudio

Cinco notebooks de Jupyter autocontenidos que explican las metaheurísticas más
importantes para optimización combinatoria y continua, **todos en español**,
con implementaciones desde cero (solo NumPy + NetworkX + Matplotlib).

## Problema compartido

Para hacer los métodos directamente comparables, todos los notebooks 2–5
resuelven la misma instancia de **Coloración de Grafos** (20 nodos, generada
con `common.py`). El notebook 1 (método exacto) usa una instancia más pequeña de
12 nodos. Cada notebook añade un segundo problema distinto para mostrar la
generalidad del método.

---

## Los cinco notebooks

| # | Notebook | Método | Tipo | Problema 1 (compartido) | Problema 2 |
|---|----------|--------|------|--------------------------|------------|
| 01 | [Ramificación y Acotación](01_ramificacion_y_acotacion.ipynb) | Branch & Bound (DSATUR) | **Exacto** (búsqueda en árbol) | Coloración de Grafos (12 nodos) | Cobertura de Vértices |
| 02 | [Búsqueda Tabú](02_busqueda_tabu.ipynb) | Tabu Search | Heurística, **trayectoria** | Coloración de Grafos (20 nodos) | Corte Máximo (Max-Cut) |
| 03 | [Colonia de Hormigas](03_colonia_de_hormigas.ipynb) | ACO (Ant System) | Heurística, **poblacional/enjambre** | Coloración de Grafos (20 nodos) | Planificación de Trabajos (makespan) |
| 04 | [Algoritmo Genético](04_algoritmo_genetico.ipynb) | GA | Heurística, **poblacional** | Coloración de Grafos (20 nodos) | Función de Ackley (continuo, 2D) |
| 05 | [Recocido Simulado](05_recocido_simulado.ipynb) | Simulated Annealing | Heurística, **trayectoria** | Coloración de Grafos (20 nodos) | Función de Schwefel (continuo, 2D) |

---

## Contenido de cada notebook

Cada notebook cubre los siguientes puntos (todo en español):

1. **Intuición y analogía** — explicación sin jerga técnica.
2. **Formulación matemática** — modelo formal del problema y del algoritmo.
3. **Pseudocódigo** — versión abstracta y clara del algoritmo.
4. **Implementación desde cero** — código Python comentado, sin librerías externas de optimización.
5. **Ejemplo 1: Coloración de Grafos** — instancia compartida para comparar métodos.
6. **Ejemplo 2** — un segundo problema distinto por notebook.
7. **Análisis de parámetros** — efecto de los parámetros clave con gráficas.
8. **Preguntas frecuentes del examen** — respuestas detalladas a lo que suele preguntar el profesor.
9. **Ejercicios** — para practicar y profundizar.
10. **Referencias** — artículos originales y libros de texto.

---

## Resumen intuitivo de cada método

- **Ramificación y Acotación** — *Búsqueda exhaustiva inteligente.* Divide el espacio
  de soluciones en un árbol; usa cotas para descartar ramas enteras sin explorarlas.
  Garantiza el óptimo, pero costo exponencial en el peor caso.

- **Búsqueda Tabú** — *Local search con memoria.* Siempre avanza al mejor vecino,
  aunque empeore, y prohíbe deshacer movimientos recientes (lista tabú) para evitar ciclos.

- **Colonia de Hormigas** — *Sigue el rastro.* Muchos agentes construyen soluciones
  probabilísticamente, reforzando con feromonas los caminos que funcionan. La evaporación
  evita el estancamiento.

- **Algoritmo Genético** — *Supervivencia del más apto.* Una población evoluciona mediante
  selección (los mejores se reproducen), cruce (combina dos padres) y mutación (cambio
  aleatorio). Los buenos rasgos se acumulan generación a generación.

- **Recocido Simulado** — *Agitar y dejar enfriar.* Acepta soluciones peores con
  probabilidad que decrece con el tiempo (temperatura). Al inicio explora libremente;
  al final explota la mejor región encontrada.

---

## Comparativa rápida

| Aspecto | B&B | Tabú | ACO | GA | SA |
|---------|-----|------|-----|----|----|
| ¿Garantiza el óptimo? | Sí (si termina) | No | No | No | No (asintótico) |
| Soluciones simultáneas | 1 (+ árbol) | 1 | Muchas (hormigas) | Muchas (población) | 1 |
| Requiere memoria | Alta (árbol) | Baja (lista tabú) | Media (feromonas) | Media (población) | Mínima |
| Parámetros clave | Cota, orden de ramificación | Tenure, vecindario | α, β, ρ, #hormigas | Tamaño pop, tasas cruce/mut | T₀, α enfriamiento |
| Fortaleza principal | Optimalidad garantizada | Vecindarios estructurados | Problemas de grafos/rutas | Paisajes multimodales | Muy general, fácil implementar |

---

## Setup

```bash
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
```

Lanzar Jupyter:

```bash
.venv\Scripts\jupyter lab
```

Probado con **Python 3.14.4**. No se usan librerías externas de optimización;
todo el código es transparente e implementado desde cero.

## Orden de lectura sugerido

**Para aprender de menor a mayor complejidad:**
1. **05 Recocido Simulado** — el más simple (una solución, regla de aceptación directa).
2. **02 Búsqueda Tabú** — local search con memoria.
3. **04 Algoritmo Genético** — introduce poblaciones y operadores evolutivos.
4. **03 Colonia de Hormigas** — poblacional con comunicación indirecta.
5. **01 Branch & Bound** — para contrastar con el método exacto y entender el gap.
