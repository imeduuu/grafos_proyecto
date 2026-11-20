# 1. Modelación matemática

## 1.1 Modelo del laberinto

El laberinto se modela como un **grafo dirigido** G = (V, E), donde:

- **V** es el conjunto de vértices. Cada vértice representa una posición o intersección del laberinto.
- **E ⊆ V × V** es el conjunto de arcos. Cada arco (u, v) ∈ E representa un **pasillo de sentido único** que permite avanzar de u a v, pero no de v a u.
- **s ∈ V** es la **entrada** del laberinto y **t ∈ V** es la **salida**, con s ≠ t.

Un **camino s-t** es una secuencia de vértices s = v₀, v₁, …, v_k = t tal que cada par consecutivo (v_{i-1}, v_i) es un arco de E recorrido en su sentido. Su **longitud** es el número de arcos k, es decir, la cantidad de pasillos recorridos.

Se denota por **d_G(s, t)** la **distancia** de s a t en G: la menor longitud entre todos los caminos s-t. Si t no es alcanzable desde s, se dice que no existe camino y no se asigna una distancia.

Se define además un **pasillo bloqueado** como un arco que **sigue perteneciendo a E**, ya que el pasillo existe físicamente en el laberinto, pero que los algoritmos no pueden usar. Formalmente, se distingue un subconjunto B ⊆ E de arcos bloqueados, y los algoritmos (camino mínimo, caminos sin arcos compartidos y corte mínimo) trabajan sobre los **arcos activos** E \ B. Esta distinción permite simular el cierre y la reapertura de un pasillo sin alterar la estructura de la red. Por ejemplo, un pasillo bloqueado se sigue contando en |E| y en las restricciones de la configuración inicial.

## 1.2 Red inicial

La red principal del grupo se encuentra en `datos/grafo_inicial.json`.

**Vértices:**

V = {s, A, B, C, D, E, F, G, H, I, t}

**Arcos:**

E = {(s, A), (s, B), (s, C), (A, B), (A, D), (B, D), (B, E), (C, E), (C, F), (F, E), (D, G), (E, H), (G, H), (G, t), (H, I), (I, t)}

**Entrada y salida:** s = s, t = t.

**Tamaño:** |V| = 11 y |E| = 16.

La red se organiza en capas que avanzan desde la entrada hacia la salida:

| Capa 0 | Capa 1 | Capa 2 | Capa 3 | Capa 4 |
|:---:|:---:|:---:|:---:|:---:|
| s | A, B, C | D, E, F | G, H, I | t |

Dentro de las capas existen además arcos "laterales" que conectan vértices de una misma capa: (A, B), (F, E), (G, H) y (H, I). Estos arcos generan rutas alternativas de distinta longitud.

**[PENDIENTE: imagen de la red inicial generada por la app — docs/imagenes/red_inicial.png]**

## 1.3 Comprobación de las restricciones

| Restricción | Valor en la red inicial | ¿Cumple? |
|---|---|:---:|
| 10 ≤ \|V\| ≤ 12 | \|V\| = 11 | Sí |
| 14 ≤ \|E\| ≤ 20 | \|E\| = 16 | Sí |
| s ≠ t | s = s, t = t | Sí |
| Sin lazos | Ningún arco es de la forma (v, v) | Sí |
| Sin arcos repetidos | Los 16 arcos son pares ordenados distintos | Sí |
| Sin arcos recíprocos | Ningún par {u, v} aparece en ambos sentidos (ver abajo) | Sí |
| Sin vértices aislados | Los 11 vértices participan en al menos un arco (ver abajo) | Sí |
| Al menos 2 caminos s-t sin arcos compartidos | s→A→D→G→t y s→B→E→H→I→t (ver abajo) | Sí |

**Arcos recíprocos y repetidos.** Si se olvida el sentido de cada arco, los 16 arcos determinan los siguientes pares de vértices:

{s,A}, {s,B}, {s,C}, {A,B}, {A,D}, {B,D}, {B,E}, {C,E}, {C,F}, {E,F}, {D,G}, {E,H}, {G,H}, {G,t}, {H,I}, {I,t}.

Los 16 pares son distintos entre sí. Si existieran dos arcos repetidos, o dos arcos recíprocos (u, v) y (v, u), ambos producirían el mismo par {u, v} y esta lista tendría menos de 16 elementos. En consecuencia, la red no tiene arcos repetidos ni arcos recíprocos.

**Vértices aislados.** Cada vértice es extremo de al menos un arco:

| Vértice | Arco de ejemplo |
|:---:|---|
| s | (s, A) |
| A | (s, A) |
| B | (s, B) |
| C | (s, C) |
| D | (A, D) |
| E | (B, E) |
| F | (C, F) |
| G | (D, G) |
| H | (E, H) |
| I | (H, I) |
| t | (G, t) |

**Dos caminos sin arcos compartidos.** Se consideran los caminos:

- P₁ = s→A→D→G→t, con arcos {(s, A), (A, D), (D, G), (G, t)}.
- P₂ = s→B→E→H→I→t, con arcos {(s, B), (B, E), (E, H), (H, I), (I, t)}.

Todos los arcos de P₁ y P₂ pertenecen a E, y cada uno se recorre en su sentido. La intersección de los dos conjuntos de arcos es vacía: P₁ sale de s por (s, A) y P₂ por (s, B), y P₁ llega a t por (G, t) y P₂ por (I, t). Los vértices intermedios {A, D, G} y {B, E, H, I} también son distintos, así que ningún arco interno puede coincidir. Por lo tanto, existen al menos 2 caminos s-t sin arcos compartidos.

**Comprobación automática.** El programa revisa estas restricciones de forma automática con la función `validar_configuracion_inicial` (`src/modelo/validaciones.py`). Esta función retorna la lista de restricciones incumplidas, y al aplicarla a `datos/grafo_inicial.json` la lista resultante es vacía. Además, el método `agregar_arco` de la clase `GrafoDirigido` (`src/modelo/grafo.py`) rechaza con un error cualquier intento de agregar un lazo, un arco repetido o el recíproco de un arco existente. Así se impide que estas condiciones se violen también durante la simulación.

## 1.4 Modificaciones de la red

Se definen dos modificaciones de la red inicial. Ambas mantienen la misma entrada s y la misma salida t, para que los resultados sean comparables con la configuración original.

| Configuración | Archivo | Cambio | \|E\| | Arcos activos |
|---|---|---|:---:|:---:|
| Original | `datos/grafo_inicial.json` | — | 16 | 16 |
| Modificación 1 | `datos/configuraciones/modificacion_1.json` | Se **bloquea** el pasillo D→G | 16 | 15 |
| Modificación 2 | `datos/configuraciones/modificacion_2.json` | Se **agrega** el pasillo C→t | 17 | 17 |

**Modificación 1: bloqueo de D→G.** El arco (D, G) sigue perteneciendo a E, pero queda bloqueado y los algoritmos no lo usan. Se eligió porque D→G forma parte del corte mínimo de la red original. Por eso, bloquearlo debería reducir el número de rutas alternativas y alargar el camino mínimo, ya que el camino más corto de la red original (s→A→D→G→t) pasa por este pasillo.

**Modificación 2: incorporación de C→t.** Se agrega el arco (C, t), con lo que |E| pasa de 16 a 17, un valor que sigue dentro del rango permitido. No se crea un arco recíproco, porque (t, C) no existe en la red. Se eligió porque crea un **atajo** directo hacia la salida: el vértice C, que en la red original solo conduce a E y F, pasa a conectar con t, lo que debería acortar el camino mínimo y aumentar el número de rutas alternativas.

Los efectos de ambas modificaciones sobre d_G(s, t), el número de caminos sin arcos compartidos y el tamaño del corte mínimo se presentan en la sección 5.3.
