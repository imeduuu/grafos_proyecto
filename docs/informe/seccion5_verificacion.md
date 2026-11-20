# 5. Verificación de resultados

## 5.1 Caso pequeño resuelto a mano

Para verificar los algoritmos se usa un caso pequeño, almacenado en `datos/caso_verificacion.json`, que se resuelve completamente a mano.

- V = {s, a, b, c, t}, con |V| = 5.
- E = {(s, a), (s, b), (a, b), (a, c), (b, c), (b, t), (c, t)}, con |E| = 7.
- Entrada s y salida t.

**[PENDIENTE: imagen del caso manual — docs/imagenes/caso_manual.png]**

### a) Camino mínimo

Se aplica una búsqueda en anchura (BFS) desde s. Los vecinos de cada vértice se examinan en el orden en que aparecen sus arcos. Un vértice se descubre la primera vez que se alcanza, y en ese momento se registran su nivel (distancia desde s) y su predecesor.

| Paso | Vértice procesado | Arcos examinados | Vértices descubiertos (nivel, predecesor) |
|:---:|:---:|---|---|
| 0 | — | — | s (nivel 0, —) |
| 1 | s | (s, a), (s, b) | a (nivel 1, s); b (nivel 1, s) |
| 2 | a | (a, b), (a, c) | b ya descubierto; c (nivel 2, a) |
| 3 | b | (b, c), (b, t) | c ya descubierto; t (nivel 2, b) |
| 4 | c | (c, t) | t ya descubierto |
| 5 | t | — | — |

Agrupando por niveles:

| Nivel | Vértices |
|:---:|---|
| 0 | s |
| 1 | a, b |
| 2 | c, t |

El vértice t se alcanza en el nivel 2 con predecesor b, y b tiene predecesor s. Al reconstruir el camino hacia atrás se obtiene **s→b→t**, de longitud 2.

**Justificación del mínimo.** Un camino de longitud 0 es imposible porque s ≠ t. Un camino de longitud 1 requeriría el arco (s, t), que no pertenece a E. Por lo tanto, todo camino s-t tiene longitud al menos 2. Como s→b→t tiene longitud 2, se concluye que

**d(s, t) = 2**, con camino mínimo s→b→t.

### b) Caminos sin arcos compartidos

Se consideran los caminos:

- P₁ = s→a→c→t, con arcos {(s, a), (a, c), (c, t)}.
- P₂ = s→b→t, con arcos {(s, b), (b, t)}.

Ambos son caminos válidos: todos sus arcos pertenecen a E y se recorren en su sentido. Sus conjuntos de arcos son disjuntos:

{(s, a), (a, c), (c, t)} ∩ {(s, b), (b, t)} = ∅.

Se obtienen así **2 caminos s-t sin arcos compartidos**.

### c) Corte

Se considera el conjunto C = {(s, a), (s, b)}, con |C| = 2. Estos son los únicos arcos que salen de s. Si se eliminan, s queda sin arcos de salida, por lo que desde s no se puede alcanzar ningún otro vértice y, en particular, t no es alcanzable. Por lo tanto, C es un **corte s-t**.

### d) Optimalidad (teorema de Menger, versión para arcos)

Se demuestra a continuación que la familia de b) es máxima y que el corte de c) es mínimo.

1. **Hay como máximo 2 caminos sin arcos compartidos.** Todo camino s-t debe salir de s, y por lo tanto usa algún arco de C. Si una familia de caminos no comparte arcos, cada camino usa un arco de C distinto. En consecuencia, el número de caminos de la familia es a lo sumo |C| = 2.
2. **Todo corte tiene al menos 2 arcos.** Un corte debe interrumpir todo camino s-t, en particular P₁ y P₂. Como P₁ y P₂ no comparten arcos, el arco que interrumpe P₁ es distinto del que interrumpe P₂. Por lo tanto, cualquier corte contiene al menos 2 arcos.

Como el máximo número de caminos sin arcos compartidos y el tamaño mínimo de un corte valen ambos 2, la familia {P₁, P₂} es **máxima** y el corte C es **mínimo**. Este resultado coincide con lo que establece el teorema de Menger en su versión para arcos: el máximo número de caminos s-t sin arcos compartidos es igual al mínimo número de arcos cuya eliminación desconecta t de s.

### e) Observación: el corte mínimo no es único

El conjunto C' = {(b, t), (c, t)} también tiene tamaño 2 y desconecta s de t, porque contiene los únicos arcos que llegan a t. Por lo tanto, C' es otro corte mínimo. En consecuencia, al contrastar con el código basta exigir que el corte obtenido **tenga tamaño 2 y desconecte s de t**. No es necesario que coincida arco por arco con C.

## 5.2 Contraste con el código

| Resultado | Manual | Código | ¿Coincide? |
|---|---|---|:---:|
| d(s, t) | 2 | **[PENDIENTE: resultado del código]** | **[PENDIENTE]** |
| Camino mínimo | s→b→t | **[PENDIENTE: resultado del código]** | **[PENDIENTE]** |
| N.º de caminos sin arcos compartidos | 2 | **[PENDIENTE: resultado del código]** | **[PENDIENTE]** |
| Tamaño del corte mínimo | 2 | **[PENDIENTE: resultado del código]** | **[PENDIENTE]** |

**[PENDIENTE: captura de la app con el caso manual — docs/imagenes/caso_manual_app.png]**

Mientras tanto, el resultado manual ya está confirmado por el verificador independiente. Las pruebas de `tests/test_caso_manual.py` cargan los valores esperados guardados en `datos/caso_verificacion.json` (campo `resultado_manual_esperado`) y comprueban lo siguiente:

- s→b→t es un camino válido de longitud 2.
- s→a→c→t y s→b→t son caminos válidos que no comparten arcos.
- El corte {(s, a), (s, b)} desconecta s de t y su tamaño coincide con el número de caminos.

Estas pruebas no dependen de los algoritmos de `src/algoritmos`. La comparación directa entre el resultado manual y el resultado del código está incluida en el mismo archivo y se ejecutará cuando los algoritmos estén implementados.

## 5.3 Verificación de la red principal y sus modificaciones

Cada vez que se calculan los resultados de una configuración, la función `verificar_todo` (`src/verificacion/verificador.py`) ejecuta seis comprobaciones automáticas:

| Comprobación | Qué verifica |
|---|---|
| `camino_minimo_valido` | El camino mínimo empieza en s, termina en t y cada par de vértices consecutivos es un arco **activo** recorrido en su sentido. Si el código informa que no hay camino, se comprueba que t efectivamente no sea alcanzable desde s. |
| `caminos_disjuntos_validos` | Cada uno de los caminos sin arcos compartidos es un camino s-t válido, con el mismo criterio anterior. |
| `sin_arcos_compartidos` | Ningún arco aparece en más de un camino. Los vértices sí pueden repetirse entre caminos. |
| `cantidad_coincide` | La cantidad de caminos informada es igual al número de caminos efectivamente entregados. |
| `corte_desconecta` | Al bloquear los arcos del corte en una copia del grafo, t deja de ser alcanzable desde s. |
| `igualdad_menger` | El número de caminos sin arcos compartidos es igual al tamaño del corte. |

**Independencia del verificador.** El módulo de verificación no importa nada de `src/algoritmos`. Para decidir si t es alcanzable desde s usa su **propia búsqueda** (una búsqueda en profundidad iterativa, `_es_alcanzable`), que recorre solo los arcos activos del grafo. Por lo tanto, un error en BFS, en el flujo máximo o en el corte mínimo no puede ocultarse por compartir código con la verificación. Además, las comprobaciones no aceptan los resultados sin revisarlos: los recorren sobre el grafo arco por arco. La comprobación de la igualdad de Menger se complementa con `corte_desconecta`. Por la desigualdad débil, ningún corte puede ser menor que el número de caminos sin arcos compartidos. Entonces, si un conjunto de arcos desconecta s de t y tiene exactamente ese tamaño, la familia de caminos es máxima y el corte es mínimo.

La tabla siguiente resume los valores esperados según el diseño de la red, para la configuración original y las dos modificaciones (sección 1.4), junto con los que entregará el código:

| Configuración | d(s, t) esperado | N.º caminos esperado | \|corte\| esperado | Obtenido por el código (d / caminos / \|corte\|) | Verificaciones |
|---|:---:|:---:|:---:|:---:|:---:|
| Original | 4 | 2 | 2 | **[PENDIENTE]** | **[PENDIENTE]** |
| Mod. 1 (bloqueo D→G) | 5 | 1 | 1 | **[PENDIENTE]** | **[PENDIENTE]** |
| Mod. 2 (agrega C→t) | 2 | 3 | 3 | **[PENDIENTE]** | **[PENDIENTE]** |

Los valores esperados se justifican brevemente así:

- **Original.** Los únicos arcos que llegan a t son (G, t) e (I, t), así que hay a lo sumo 2 caminos sin arcos compartidos, y s→A→D→G→t y s→B→E→H→I→t alcanzan esa cota. El único arco que entra a G es (D, G), y a D solo se llega desde A o B, que están a distancia 1 de s. Por lo tanto, todo camino que termine por G tiene longitud al menos 4. Todo camino que termine por I debe pasar por H, que no está a distancia menor que 3, y por eso tiene longitud al menos 5. En consecuencia, d(s, t) = 4.
- **Mod. 1.** Al bloquear (D, G), G deja de ser alcanzable, porque es su único arco de entrada. Entonces todo camino debe terminar por H→I→t. El arco (H, I) por sí solo es un corte de tamaño 1, y s→B→E→H→I→t, de longitud 5, es un camino mínimo.
- **Mod. 2.** El arco (C, t) produce el camino s→C→t, de longitud 2, y no existe el arco (s, t). Los caminos s→A→D→G→t, s→B→E→H→I→t y s→C→t no comparten arcos, y los únicos arcos que salen de s, {(s, A), (s, B), (s, C)}, forman un corte de tamaño 3.

La columna "Obtenido por el código" y la columna de verificaciones se completarán con la salida de la aplicación, cuando `verificar_todo` indique ✔ en sus seis comprobaciones.
