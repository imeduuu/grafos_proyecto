
# Fuentes académicas y técnicas

Proyecto 1: Simulador interactivo de laberintos y rutas alternativas.  
Asignatura: Teoría de Grafos — INFO1158.

Este documento identifica las fuentes utilizadas como fundamento teórico y técnico para el diseño de los algoritmos y las herramientas de visualización del proyecto.

Los algoritmos BFS, DFS, flujo máximo y corte mínimo fueron implementados mediante código Python propio. Las bibliotecas externas se utilizan para construir la interfaz y representar gráficamente el laberinto, no para resolver los problemas algorítmicos solicitados.

## 1. Caminos mínimos (BFS vs DFS)

### Fuente 1: Cormen, Leiserson, Rivest y Stein

Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022). *Introduction to algorithms* (4.ª ed., cap. 20, Elementary Graph Algorithms; cap. 24, Maximum Flow). The MIT Press.

https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/

**Uso en el proyecto:** Fundamenta las búsquedas en anchura (BFS) y profundidad (DFS). Justifica que BFS recorre los vértices por niveles y obtiene distancias mínimas en cantidad de arcos cuando todos tienen el mismo costo. También permite explicar por qué DFS puede encontrar un camino sin garantizar que sea el más corto.

### Fuente 2: Kleinberg y Tardos

Kleinberg, J., & Tardos, É. (2005). *Algorithm design* (1.ª ed., cap. 3, Graphs). Addison-Wesley.

https://www.pearson.com/en-us/subject-catalog/p/algorithm-design/P200000003259/9780321295354

**Uso en el proyecto:** Permite comparar los recorridos de grafos realizados mediante colas y pilas. Fundamenta la selección de BFS para calcular caminos mínimos y de DFS como estrategia alternativa para determinar la existencia de caminos.

### Comparación y selección

Se seleccionó BFS para encontrar el camino dirigido con menor número de arcos entre la entrada y la salida.

BFS emplea una cola FIFO y explora los vértices por niveles, garantizando el camino mínimo en un grafo no ponderado.

DFS utiliza una pila y explora una rama antes de retroceder. Puede encontrar un camino válido, pero no necesariamente el más corto.

Ambos recorridos tienen complejidad O(|V| + |E|) en su implementación convencional con listas de adyacencia.

## 2. Caminos sin arcos compartidos / flujo máximo

### Fuente 3: Ford y Fulkerson

Ford, L. R., Jr., & Fulkerson, D. R. (1956). Maximal flow through a network. *Canadian Journal of Mathematics, 8*, 399–404.

https://doi.org/10.4153/CJM-1956-045-5

**Uso en el proyecto:** Fundamenta el procedimiento de flujo máximo mediante caminos aumentantes y el uso de capacidades residuales. Sirve como base para calcular el máximo número de caminos dirigidos que no comparten arcos.

### Fuente 4: Edmonds y Karp

Edmonds, J., & Karp, R. M. (1972). Theoretical improvements in algorithmic efficiency for network flow problems. *Journal of the ACM, 19*(2), 248–264.

https://doi.org/10.1145/321694.321699

**Uso en el proyecto:** Fundamenta la selección de caminos aumentantes mediante BFS dentro del algoritmo de flujo máximo. Esta estrategia, conocida como Edmonds-Karp, tiene una complejidad temporal general O(|V| · |E|²).

### Fuente 5: Kleinberg y Tardos — Flujo en redes

Kleinberg, J., & Tardos, É. (2005). *Algorithm design* (1.ª ed., cap. 7, Network Flow, especialmente secciones 7.1, 7.2, 7.3 y 7.6). Addison-Wesley.

https://www.pearson.com/en-us/subject-catalog/p/algorithm-design/P200000003259/9780321295354

**Uso en el proyecto:** Explica el flujo máximo, los cortes mínimos y los caminos disjuntos en redes dirigidas. Fundamenta la representación de cada pasillo activo con capacidad unitaria y la relación entre unidades de flujo y caminos sin arcos compartidos.

### Comparación y selección

Se consideraron dos estrategias:

1. Buscar repetidamente caminos de entrada a salida y eliminar los arcos utilizados.
2. Calcular un flujo máximo con capacidad unitaria por arco y descomponer el flujo obtenido en caminos.

Se seleccionó la segunda estrategia mediante Edmonds-Karp.

La eliminación directa de arcos después de encontrar cada camino puede impedir descubrir una cantidad máxima de rutas independientes, porque las decisiones anteriores no siempre pueden corregirse.

El algoritmo de flujo máximo utiliza una red residual que permite reajustar el flujo mediante arcos inversos.

Como cada arco original tiene capacidad 1, ningún arco puede transportar más de una unidad de flujo. De esta manera, los caminos extraídos no comparten arcos, aunque sí pueden compartir vértices.

## 3. Corte mínimo / teorema de Menger

### Fuente 6: Menger

Menger, K. (1927). Zur allgemeinen Kurventheorie. *Fundamenta Mathematicae, 10*(1), 96–115.

https://doi.org/10.4064/fm-10-1-96-115

**Uso en el proyecto:** Fundamenta la relación entre el número máximo de caminos sin arcos compartidos y la cantidad mínima de arcos cuya eliminación desconecta la entrada de la salida. Se aplica la versión del teorema correspondiente a caminos disjuntos en arcos.

### Fuente 7: Elias, Feinstein y Shannon

Elias, P., Feinstein, A., & Shannon, C. E. (1956). A note on the maximum flow through a network. *IRE Transactions on Information Theory, 2*(4), 117–119.

https://doi.org/10.1109/TIT.1956.1056816

**Uso en el proyecto:** Proporciona un fundamento clásico del teorema de flujo máximo y corte mínimo. Permite justificar que el valor del flujo máximo coincide con la capacidad de un corte mínimo de la red.

### Fuente 8: Bondy y Murty

Bondy, J. A., & Murty, U. S. R. (2008). *Graph theory* (Graduate Texts in Mathematics, vol. 244). Springer.

https://link.springer.com/book/9781846289699

**Uso en el proyecto:** Sirve como referencia general para las definiciones matemáticas de grafo dirigido, vértice, arco, camino y conectividad. También respalda los conceptos de caminos disjuntos y separación mediante conjuntos de arcos.

### Relación matemática utilizada

Después de calcular el flujo máximo, se determina el conjunto S de vértices alcanzables desde la entrada en la red residual final, utilizando únicamente arcos con capacidad residual positiva.

El corte mínimo está formado por los arcos originales activos que salen de S hacia los vértices que no pertenecen a S.

Por el teorema de flujo máximo–corte mínimo, el valor del flujo máximo coincide con la capacidad de ese corte.

Como todos los arcos tienen capacidad 1, la capacidad del corte es igual a su cantidad de arcos.

Por lo tanto:

Máximo número de caminos dirigidos sin arcos compartidos = mínimo número de arcos que deben eliminarse para desconectar la entrada de la salida.

Esta igualdad permite verificar matemáticamente los resultados entregados por el simulador.

## 4. Herramientas

### Python

Python Software Foundation. (s. f.). *Python 3 documentation* [Documentación técnica].

https://docs.python.org/3/

**Uso en el proyecto:** Lenguaje utilizado para implementar las clases, las estructuras de datos, los recorridos BFS y DFS, el cálculo de flujo máximo, el corte mínimo y las funciones de verificación.

### Streamlit

Streamlit. (s. f.). *Streamlit documentation* [Documentación técnica].

https://docs.streamlit.io/

**Uso en el proyecto:** Desarrollo de la interfaz interactiva. Permite seleccionar entrada y salida, bloquear o restablecer pasillos, agregar arcos, recalcular los resultados y comparar configuraciones.

### NetworkX

NetworkX Developers. (s. f.). *NetworkX documentation: Drawing* [Documentación técnica].

https://networkx.org/documentation/stable/reference/drawing.html

**Uso en el proyecto:** Representación visual de los vértices y arcos dirigidos, incluyendo posiciones de los nodos y dibujo de conexiones.

**Restricción:** NetworkX se utiliza solamente para la visualización del grafo. No se utilizan sus funciones para calcular caminos mínimos, recorridos BFS o DFS, flujo máximo, caminos disjuntos ni cortes mínimos.

### Matplotlib

Matplotlib Development Team. (s. f.). *Matplotlib documentation* [Documentación técnica].

https://matplotlib.org/stable/

**Uso en el proyecto:** Creación de figuras para mostrar el laberinto. Permite diferenciar con colores los caminos mínimos, las rutas independientes, los pasillos bloqueados y el corte mínimo.

---

## 5. Declaración de implementación propia

Los procedimientos principales del simulador fueron implementados directamente en Python, utilizando estructuras de datos y operaciones básicas del lenguaje.

Los archivos responsables de los algoritmos son:

- `src/algoritmos/busqueda_anchura.py`
- `src/algoritmos/busqueda_profundidad.py`
- `src/algoritmos/flujo_maximo.py`
- `src/algoritmos/corte_minimo.py`

No se utilizan bibliotecas externas que ejecuten directamente los algoritmos matemáticos exigidos por la pauta.

Las referencias académicas presentadas fundamentan las estrategias seleccionadas y permiten explicar sus propiedades, corrección y complejidad.
