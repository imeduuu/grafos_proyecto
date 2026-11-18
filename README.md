# Simulador interactivo de laberintos y rutas alternativas

**Teoría de Grafos – INFO1158 · Proyecto 1**
Integrantes: Nicolás · Ricardo · Eduardo
Entrega del informe y presentación: **jueves 26 de noviembre de 2026** (informe en Educa hasta las 23:00).

Aplicación que modela un laberinto de pasillos de sentido único como un **grafo dirigido G = (V, E)** y permite:

1. Encontrar un **camino mínimo** (menor número de pasillos) de la entrada `s` a la salida `t`.
2. Calcular el **máximo número de caminos s→t que no comparten arcos** y mostrarlos.
3. Encontrar un **corte mínimo**: el menor conjunto de pasillos cuyo bloqueo impide llegar de `s` a `t`.
4. **Simular cambios** desde la interfaz: bloquear/restablecer pasillos, agregar pasillos y cambiar `s` y `t`.
5. **Verificar** que |caminos disjuntos| = |corte mínimo| (teorema de Menger / flujo máximo–corte mínimo).

> ⚠️ **Regla del enunciado:** los algoritmos (BFS, flujo máximo, corte mínimo) se implementan con **código propio**.
> `networkx` se usa **solo para dibujar**. Prohibido usar `nx.shortest_path`, `nx.maximum_flow`, `nx.minimum_cut`, `nx.edge_disjoint_paths`, etc.

---

## Cómo ejecutar

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

streamlit run main.py              # abre la aplicación
pytest                             # corre las pruebas
```

---

## Estructura del proyecto

```
laberintos-grafos/
├── main.py                          # Punto de entrada (streamlit run main.py)
├── requirements.txt                 # Dependencias
├── README.md
├── datos/                           # Grafos en JSON
│   ├── ejemplo_figura1.json         # Laberinto de la Figura 1 (para pruebas)
│   ├── grafo_inicial.json           # Red principal del grupo (TODO)
│   ├── caso_verificacion.json       # Caso de 4–6 vértices resuelto a mano (TODO)
│   └── configuraciones/
│       ├── modificacion_1.json      # Primera modificación a comparar (TODO)
│       └── modificacion_2.json      # Segunda modificación a comparar (TODO)
├── src/
│   ├── modelo/                      # Representación del grafo
│   │   ├── grafo.py
│   │   ├── cargador.py
│   │   └── validaciones.py
│   ├── algoritmos/                  # Código propio de los algoritmos
│   │   ├── busqueda_anchura.py      # BFS → camino mínimo
│   │   ├── busqueda_profundidad.py  # DFS → para comparar con BFS
│   │   ├── flujo_maximo.py          # Edmonds-Karp unitario → caminos sin arcos compartidos
│   │   └── corte_minimo.py          # Corte mínimo desde la red residual
│   ├── simulacion/
│   │   └── configuraciones.py       # Resultados por configuración y comparación
│   ├── verificacion/
│   │   └── verificador.py           # Comprobaciones automáticas (sección 5)
│   └── interfaz/
│       ├── app.py                   # Aplicación Streamlit
│       └── visualizacion.py         # Dibujo del grafo y colores
├── tests/                           # Pruebas con pytest
│   ├── conftest.py
│   ├── test_grafo.py
│   ├── test_busquedas.py
│   ├── test_flujo_y_corte.py
│   └── test_caso_manual.py
└── docs/
    ├── fuentes.md                   # Bibliografía académica/técnica
    ├── informe/estructura_informe.md
    ├── imagenes/                    # Capturas para el informe
    └── presentacion/guion.md
```

---

## Detalle de cada carpeta y archivo

### `datos/` — Grafos de entrada

Todos los grafos se guardan en JSON con el formato:

```json
{
  "vertices": ["s", "A", "B", "t"],
  "arcos": [["s", "A"], ["A", "B"], ["B", "t"]],
  "entrada": "s",
  "salida": "t",
  "posiciones": {"s": [0, 0], "A": [1, 0]}
}
```

| Archivo | Qué contiene |
|---|---|
| `ejemplo_figura1.json` | La red de la Figura 1 del enunciado (9 vértices, 12 arcos). Se usa en las pruebas: d(s,t)=4, 2 caminos sin arcos compartidos, corte de tamaño 2. **No** es la red de entrega. |
| `grafo_inicial.json` | Red principal del grupo. Debe cumplir: 10–12 vértices, 14–20 arcos, sin lazos, sin arcos repetidos, sin recíprocos, sin vértices aislados y al menos 2 caminos s→t sin arcos compartidos. |
| `caso_verificacion.json` | Caso pequeño (4–6 vértices) resuelto a mano. Incluye `resultado_manual_esperado` para comparar con el código. |
| `configuraciones/modificacion_1.json` y `_2.json` | Las dos modificaciones a comparar con la original (arcos bloqueados/agregados). **Mismos `s` y `t`** que la original. |

### `src/modelo/` — Representación del laberinto

Aquí definimos el grafo dirigido, que es la base de todo lo demás.

**`grafo.py`** — clase `GrafoDirigido` (lista de adyacencia + conjunto de arcos bloqueados).

| Función | Qué hace |
|---|---|
| `agregar_vertice(vertice)` | Agrega un vértice. |
| `agregar_arco(origen, destino)` | Agrega un pasillo dirigido; rechaza lazos, repetidos y recíprocos (`ValueError`). |
| `bloquear_arco(origen, destino)` | Bloquea un pasillo sin borrarlo. |
| `restablecer_arco(origen, destino)` | Quita el bloqueo. |
| `esta_bloqueado(origen, destino)` | Indica si un pasillo está bloqueado. |
| `definir_entrada_salida(entrada, salida)` | Define `s` y `t` (deben existir y ser distintos). |
| `sucesores(vertice)` | Vecinos por arcos **activos** (lo que usan los algoritmos). |
| `arcos()` / `arcos_activos()` | Todos los arcos / solo los no bloqueados. |
| `existe_arco(origen, destino)` | Indica si el arco existe. |
| `cantidad_vertices()` / `cantidad_arcos()` | Retornan \|V\| y \|E\|. |
| `copiar()` | Copia independiente (para comparar configuraciones). |

**`cargador.py`** — lectura y escritura de JSON.

| Función | Qué hace |
|---|---|
| `cargar_grafo_json(ruta)` | Crea un `GrafoDirigido` desde un JSON. |
| `guardar_grafo_json(grafo, ruta)` | Guarda el grafo actual en JSON. |
| `cargar_configuracion(ruta_base, ruta_modificacion)` | Carga la red original y le aplica una modificación. |

**`validaciones.py`** — restricciones de la configuración inicial.

| Función | Qué hace |
|---|---|
| `tiene_lazos(grafo)` | Detecta arcos (v, v). |
| `tiene_arcos_reciprocos(grafo)` | Detecta (u, v) y (v, u) a la vez. |
| `vertices_aislados(grafo)` | Lista los vértices sin arcos. |
| `validar_configuracion_inicial(grafo)` | Revisa todas las restricciones y retorna la lista de errores. |

### `src/algoritmos/` — Algoritmos con código propio

**`busqueda_anchura.py`** — camino mínimo con BFS. Garantiza la menor cantidad de arcos porque recorre el grafo por niveles. O(\|V\|+\|E\|).

| Función | Qué hace |
|---|---|
| `busqueda_en_anchura(grafo, origen)` | Retorna `distancias` y `predecesores`. |
| `reconstruir_camino(predecesores, origen, destino)` | Arma la lista `[s, ..., t]` siguiendo los predecesores hacia atrás. |
| `camino_minimo(grafo, origen, destino)` | Función principal: `(camino, longitud)` o `(None, None)` si no hay camino. |

**`busqueda_profundidad.py`** — DFS, implementada para comparar con BFS en el informe (encuentra un camino, pero no necesariamente el más corto).

| Función | Qué hace |
|---|---|
| `busqueda_en_profundidad(grafo, origen, destino)` | Retorna un camino cualquiera o `None`. |
| `existe_camino(grafo, origen, destino)` | Indica si `t` es alcanzable desde `s`. |

**`flujo_maximo.py`** — máximo número de caminos sin arcos compartidos, usando flujo máximo con capacidad 1 por arco (Edmonds-Karp).

| Función | Qué hace |
|---|---|
| `construir_red_residual(grafo)` | Capacidad 1 en cada arco activo y 0 en su inverso. |
| `buscar_camino_aumentante(residual, origen, destino)` | BFS sobre arcos con capacidad residual > 0. |
| `aumentar_flujo(residual, camino)` | Envía 1 unidad por el camino y actualiza la red residual. |
| `flujo_maximo_unitario(grafo, origen, destino)` | Repite hasta que no haya más caminos aumentantes; retorna `(valor, residual)`. |
| `descomponer_en_caminos(grafo, residual, origen, destino)` | Extrae los caminos concretos a partir del flujo. |
| `maximo_caminos_disjuntos(grafo, origen, destino)` | Función principal: `(cantidad, caminos)`. |

**`corte_minimo.py`** — conjunto mínimo de pasillos que desconecta `s` de `t`.

| Función | Qué hace |
|---|---|
| `alcanzables_en_residual(residual, origen)` | Conjunto S de vértices alcanzables en la red residual final. |
| `corte_minimo(grafo, origen, destino)` | Arcos (u, v) con u ∈ S y v ∉ S. Retorna `[]` si ya no hay camino. |

### `src/simulacion/` — Configuraciones y comparación

**`configuraciones.py`**

| Elemento | Qué hace |
|---|---|
| `ResultadoConfiguracion` (dataclass) | Guarda los resultados de una configuración: existe camino, camino mínimo, longitud, caminos disjuntos y corte. |
| `calcular_resultados(grafo, nombre)` | Ejecuta todos los algoritmos (es el botón “Recalcular”). |
| `comparar_configuraciones(resultados)` | Arma la tabla comparativa original / mod. 1 / mod. 2. |

### `src/verificacion/` — Comprobaciones (sección 5)

**`verificador.py`**

| Función | Qué comprueba |
|---|---|
| `verificar_camino_valido(grafo, camino, origen, destino)` | El camino va de s a t usando solo arcos activos y en su sentido. |
| `verificar_sin_arcos_compartidos(caminos)` | Ningún arco se repite entre caminos (los vértices sí pueden repetirse). |
| `verificar_corte_desconecta(grafo, corte, origen, destino)` | Al bloquear el corte ya no hay camino s→t. |
| `verificar_igualdad_menger(cantidad_caminos, corte)` | \|caminos\| = \|corte\|. |
| `verificar_todo(grafo, resultado)` | Ejecuta todas las comprobaciones y retorna un diccionario de ✔/✘. |

### `src/interfaz/` — Aplicación visual (Streamlit)

**`visualizacion.py`** — dibujo del grafo con flechas y colores distintos para cada solución.

| Función | Qué hace |
|---|---|
| `calcular_posiciones(grafo)` | Usa las posiciones del JSON o una distribución automática. |
| `dibujar_grafo(grafo, camino_minimo, caminos_disjuntos, corte, modo)` | Retorna la figura de matplotlib con la solución destacada. |

Colores: camino mínimo en **azul**, cada camino disjunto en un color distinto, corte mínimo en **rojo punteado** y arcos bloqueados en **gris**.

**`app.py`** — la aplicación.

| Función | Qué hace |
|---|---|
| `inicializar_estado()` | Carga el grafo inicial en `st.session_state`. |
| `panel_seleccion_extremos()` | Selectores de `s` y `t`. |
| `panel_bloqueos()` | Bloquear/restablecer un pasillo. |
| `panel_agregar_arco()` | Formulario para agregar un pasillo (muestra errores si es lazo, repetido o recíproco). |
| `panel_resultados()` | Botón *Recalcular*, dibujo y resultados con verificaciones. |
| `panel_comparacion()` | Tabla de las tres configuraciones. |
| `ejecutar_aplicacion()` | Arma la página completa. |

### `tests/` — Pruebas (pytest)

| Archivo | Qué prueba |
|---|---|
| `conftest.py` | Fixture `grafo_figura1` con la red del enunciado. |
| `test_grafo.py` | Rechazo de lazos y recíprocos; bloquear y restablecer. |
| `test_busquedas.py` | d(s,t)=4 en la Figura 1; sin camino no se entrega longitud. |
| `test_flujo_y_corte.py` | 2 caminos disjuntos en la Figura 1; el corte desconecta y tiene el mismo tamaño. |
| `test_caso_manual.py` | Compara el caso resuelto a mano con el código (quitar el `skip` cuando esté listo). |

### `docs/` — Material para el informe y la presentación

| Archivo/carpeta | Uso |
|---|---|
| `fuentes.md` | Bibliografía (obligatorio citar fuentes académicas/técnicas). |
| `informe/estructura_informe.md` | Índice del informe, alineado con la rúbrica. |
| `imagenes/` | Capturas de la app y del caso manual. |
| `presentacion/guion.md` | Reparto de los 12 minutos entre los tres. |

---

## Orden de dependencias (qué se necesita primero)

```
modelo/grafo.py ──► modelo/cargador.py ──► algoritmos/* ──► simulacion/ ──► interfaz/
                                              │
                                              └──► verificacion/
```
