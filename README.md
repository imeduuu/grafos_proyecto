
# Simulador interactivo de laberintos y rutas alternativas

**Teoría de Grafos – INFO1158 | Proyecto 1**

**Integrantes:** Eduardo, Ricardo y Nicolás.

**Fecha de presentación:** jueves 26 de noviembre de 2026.  
**Entrega del informe:** jueves 26 de noviembre de 2026, hasta las 23:00 horas en Educa.

## Descripción del proyecto

Este proyecto consiste en un simulador interactivo de laberintos representados mediante un grafo dirigido G = (V, E).

Los vértices representan posiciones o intersecciones y los arcos representan pasillos de sentido único.

La aplicación permite:

1. Encontrar un camino mínimo entre una entrada y una salida mediante BFS.
2. Calcular el número máximo de caminos dirigidos sin arcos compartidos mediante flujo máximo.
3. Identificar un corte mínimo de pasillos cuya eliminación impide llegar a la salida.
4. Bloquear, restablecer y agregar pasillos desde una interfaz.
5. Cambiar los vértices seleccionados como entrada y salida.
6. Comparar la red original con dos modificaciones.
7. Verificar matemáticamente los caminos y cortes obtenidos.

Se utiliza Python para implementar los algoritmos y Streamlit para la interfaz interactiva.

**Restricción importante:** todos los algoritmos matemáticos solicitados están implementados con código propio. NetworkX se utiliza exclusivamente para dibujar el grafo; no se emplea para calcular caminos mínimos, flujo máximo ni cortes mínimos.

---

## Requisitos

- Python 3.11 o superior.
- pip, para instalar dependencias.
- Navegador web.
- Entorno virtual de Python (recomendado).

Dependencias declaradas en `requirements.txt`:

- streamlit >= 1.30
- networkx >= 3.0
- matplotlib >= 3.7
- pytest >= 7.0

---

## Cómo ejecutar el proyecto

Abrir PowerShell en la carpeta principal del repositorio.

### 1. Crear un entorno virtual (opcional)

```powershell
python -m venv .venv
```

### 2. Activar el entorno virtual

En Windows con PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Si no se utiliza un entorno virtual, los siguientes comandos pueden ejecutarse directamente con Python instalado en el sistema.

### 3. Instalar las dependencias

```powershell
python -m pip install -r requirements.txt
```

### 4. Ejecutar la aplicación

```powershell
python -m streamlit run main.py
```

La aplicación se abrirá normalmente en:

http://localhost:8501

Para detenerla, presionar Ctrl + C en la terminal.

### 5. Ejecutar las pruebas

```powershell
python -m pytest -q
```

En la revisión del 24 de noviembre de 2026 se ejecutaron las pruebas disponibles y se obtuvo:

```text
64 passed
```

El resultado puede cambiar si posteriormente se agregan o modifican pruebas.

---

## Guía de uso

### Simulación interactiva

1. Abrir la pestaña **Simulación interactiva**.
2. Seleccionar los vértices de entrada y salida en la barra lateral.
3. Presionar **Aplicar entrada y salida**.
4. Bloquear o restablecer pasillos mediante los controles laterales.
5. Agregar pasillos dirigidos utilizando el formulario correspondiente.
6. Presionar **Recalcular** para ejecutar los algoritmos.
7. Utilizar el selector **Destacar** para visualizar diferentes resultados.
8. Revisar el camino mínimo, los caminos independientes, el corte mínimo y las verificaciones.

Cuando se modifica la red, la aplicación advierte que los resultados anteriores necesitan actualizarse.

El botón **Restaurar red original** descarta las modificaciones interactivas y carga nuevamente el grafo inicial.

### Comparación de configuraciones

La pestaña **Comparación de configuraciones** muestra la red original y las dos modificaciones predefinidas.

Incluye una tabla con los resultados y visualizaciones individuales de cada configuración.

Para mantener una comparación consistente, las tres configuraciones utilizan la misma entrada `s` y salida `t`.

---

## Estructura del proyecto

```text
grafos_proyecto/
├── main.py
├── README.md
├── requirements.txt
├── datos/
│   ├── ejemplo_figura1.json
│   ├── grafo_inicial.json
│   ├── caso_verificacion.json
│   └── configuraciones/
│       ├── modificacion_1.json
│       └── modificacion_2.json
├── src/
│   ├── modelo/
│   │   ├── grafo.py
│   │   ├── cargador.py
│   │   └── validaciones.py
│   ├── algoritmos/
│   │   ├── busqueda_anchura.py
│   │   ├── busqueda_profundidad.py
│   │   ├── flujo_maximo.py
│   │   └── corte_minimo.py
│   ├── simulacion/
│   │   └── configuraciones.py
│   ├── verificacion/
│   │   └── verificador.py
│   └── interfaz/
│       ├── app.py
│       └── visualizacion.py
├── tests/
│   ├── conftest.py
│   ├── test_grafo.py
│   ├── test_cargador.py
│   ├── test_validaciones.py
│   ├── test_busquedas.py
│   ├── test_flujo_y_corte.py
│   ├── test_caso_manual.py
│   ├── test_verificador.py
│   ├── test_visualizacion.py
│   └── test_configuraciones.py
└── docs/
    ├── fuentes.md
    ├── informe/
    │   ├── seccion1_modelo.md
    │   └── seccion5_verificacion.md
    └── imagenes/
        └── .gitkeep
```

Los archivos `__init__.py` de los paquetes Python se omiten del árbol para facilitar la lectura.

---

## Datos del laberinto

Los grafos y las configuraciones se almacenan mediante archivos JSON.

### Red inicial del grupo

Archivo: `datos/grafo_inicial.json`

La configuración original contiene:

- 11 vértices.
- 16 arcos dirigidos.
- Entrada: `s`.
- Salida: `t`.
- Sin lazos.
- Sin arcos repetidos.
- Sin arcos recíprocos.
- Sin vértices aislados.
- Al menos dos caminos dirigidos sin arcos compartidos entre `s` y `t`.

Conjunto de vértices:

V = {s, A, B, C, D, E, F, G, H, I, t}

Conjunto de arcos:

E = {
(s,A), (s,B), (s,C),
(A,B), (A,D),
(B,D), (B,E),
(C,E), (C,F),
(F,E),
(D,G), (E,H),
(G,H), (G,t),
(H,I), (I,t)
}

### Archivos de datos

| Archivo | Descripción |
|---|---|
| `ejemplo_figura1.json` | Grafo ilustrativo de la pauta con 9 vértices y 12 arcos. |
| `grafo_inicial.json` | Red principal del grupo con 11 vértices y 16 arcos. |
| `caso_verificacion.json` | Grafo pequeño utilizado para la comprobación manual y automática. |
| `modificacion_1.json` | Bloquea el pasillo D→G. |
| `modificacion_2.json` | Agrega el pasillo C→t. |

La primera modificación elimina temporalmente una conexión importante, reduciendo la cantidad de caminos disponibles.

La segunda incorpora un atajo hacia la salida y aumenta la disponibilidad de caminos independientes.

---

## Resultados de las configuraciones

Los resultados se obtienen ejecutando los algoritmos sobre la red original y cada modificación.

| Configuración | d(s,t) | Caminos sin arcos compartidos | Corte mínimo |
|---|---:|---:|---|
| Original | 4 | 2 | {D→G, E→H} |
| Mod. 1 (bloquea D→G) | 5 | 1 | {E→H} |
| Mod. 2 (agrega C→t) | 2 | 3 | {s→A, s→B, s→C} |

### Interpretación

**Configuración original**

Existe un camino mínimo de longitud 4 y se pueden encontrar dos caminos dirigidos sin arcos compartidos.

El corte mínimo contiene dos pasillos: D→G y E→H.

**Modificación 1**

Al bloquear D→G, el camino mínimo aumenta de 4 a 5 arcos.

La cantidad máxima de caminos sin arcos compartidos disminuye de 2 a 1.

El corte mínimo restante contiene E→H.

**Modificación 2**

Al agregar C→t, aparece un camino mínimo de longitud 2.

La cantidad máxima de caminos independientes aumenta a 3.

El corte mínimo está formado por s→A, s→B y s→C.

En las tres configuraciones se cumple la igualdad entre la cantidad máxima de caminos sin arcos compartidos y la cardinalidad del corte mínimo.

---

## Módulos del proyecto

### 1. Modelo del grafo

Carpeta: `src/modelo/`

**grafo.py**

Contiene la clase `GrafoDirigido`, responsable de almacenar vértices y arcos mediante listas de adyacencia.

Funciones y métodos principales:

| Función | Descripción |
|---|---|
| `agregar_vertice` | Incorpora un vértice. |
| `agregar_arco` | Incorpora un arco dirigido válido. |
| `bloquear_arco` | Desactiva temporalmente un pasillo. |
| `restablecer_arco` | Reactiva un pasillo bloqueado. |
| `sucesores` | Obtiene los sucesores mediante arcos activos. |
| `arcos` | Obtiene todos los arcos. |
| `arcos_activos` | Obtiene los arcos no bloqueados. |
| `existe_arco` | Comprueba la existencia de un arco. |
| `esta_bloqueado` | Comprueba si un arco está bloqueado. |
| `cantidad_vertices` | Retorna la cantidad de vértices. |
| `cantidad_arcos` | Retorna la cantidad de arcos. |
| `definir_entrada_salida` | Establece la entrada y salida del laberinto. |
| `copiar` | Genera una copia independiente del grafo. |

**cargador.py**

| Función | Descripción |
|---|---|
| `cargar_grafo_json` | Carga un grafo desde un archivo JSON. |
| `guardar_grafo_json` | Guarda un grafo en JSON. |
| `cargar_configuracion` | Carga la red base y aplica una modificación. |

**validaciones.py**

| Función | Descripción |
|---|---|
| `tiene_lazos` | Detecta lazos. |
| `tiene_arcos_reciprocos` | Detecta arcos en ambos sentidos. |
| `vertices_aislados` | Encuentra vértices aislados. |
| `validar_configuracion_inicial` | Comprueba las restricciones de la pauta. |

### 2. Algoritmos

Carpeta: `src/algoritmos/`

Todos los algoritmos son implementaciones propias en Python.

**busqueda_anchura.py — BFS**

| Función | Descripción |
|---|---|
| `busqueda_en_anchura` | Recorre el grafo por niveles. |
| `reconstruir_camino` | Reconstruye el recorrido mediante predecesores. |
| `camino_minimo` | Obtiene un camino con el menor número de arcos. |

BFS garantiza el camino mínimo en grafos no ponderados porque explora los vértices por niveles.

Complejidad temporal: O(|V| + |E|).

**busqueda_profundidad.py — DFS**

| Función | Descripción |
|---|---|
| `busqueda_en_profundidad` | Busca un camino utilizando una pila. |
| `existe_camino` | Determina si un destino es alcanzable. |

DFS puede encontrar una ruta válida, pero no garantiza que tenga la menor cantidad de arcos.

**flujo_maximo.py — Edmonds-Karp**

| Función | Descripción |
|---|---|
| `construir_red_residual` | Construye la red con capacidades unitarias. |
| `buscar_camino_aumentante` | Busca una ruta con capacidad residual positiva. |
| `aumentar_flujo` | Actualiza las capacidades residuales. |
| `flujo_maximo_unitario` | Calcula el flujo máximo. |
| `descomponer_en_caminos` | Reconstruye los caminos que transportan flujo. |
| `maximo_caminos_disjuntos` | Obtiene el máximo de caminos sin arcos compartidos. |

Cada arco activo tiene capacidad 1, lo cual impide que dos unidades de flujo utilicen el mismo pasillo simultáneamente.

Edmonds-Karp utiliza BFS para encontrar caminos aumentantes.

Complejidad general: O(|V| · |E|²).

**corte_minimo.py — Corte mínimo**

| Función | Descripción |
|---|---|
| `alcanzables_en_residual` | Obtiene los vértices alcanzables en la red residual. |
| `corte_minimo` | Encuentra un conjunto mínimo de arcos que desconecta entrada y salida. |

Se utiliza la red residual final del flujo máximo para determinar el conjunto S de vértices alcanzables desde la entrada.

Los arcos que salen de S hacia fuera de S forman el corte mínimo.

Por el teorema de flujo máximo–corte mínimo, su cardinalidad coincide con el máximo número de caminos sin arcos compartidos.

### 3. Simulación de configuraciones

Archivo: `src/simulacion/configuraciones.py`

| Elemento | Descripción |
|---|---|
| `ResultadoConfiguracion` | Clase de datos que almacena los resultados. |
| `calcular_resultados` | Ejecuta los algoritmos para una configuración. |
| `formatear_camino` | Convierte un camino en texto con flechas. |
| `formatear_corte` | Convierte el corte en una representación textual. |
| `comparar_configuraciones` | Construye la tabla comparativa. |

Los resultados incluyen existencia de caminos, longitud mínima, rutas independientes y corte mínimo.

Cuando no existe un camino, la aplicación no presenta una distancia numérica válida. El número de caminos es cero y el corte mínimo es el conjunto vacío.

### 4. Verificación de resultados

Archivo: `src/verificacion/verificador.py`

| Función | Descripción |
|---|---|
| `verificar_camino_valido` | Comprueba que el recorrido utiliza arcos activos en el sentido correcto. |
| `verificar_sin_arcos_compartidos` | Comprueba que las rutas no repiten arcos entre sí. |
| `verificar_corte_desconecta` | Comprueba que bloquear el corte impide llegar al destino. |
| `verificar_igualdad_menger` | Comprueba la igualdad entre caminos y corte. |
| `verificar_todo` | Ejecuta las verificaciones anteriores. |

El verificador utiliza una búsqueda independiente para comprobar la conectividad sin depender de los algoritmos que está evaluando.

### 5. Interfaz y visualización

Carpeta: `src/interfaz/`

**visualizacion.py**

| Función | Descripción |
|---|---|
| `calcular_posiciones` | Determina las posiciones de los vértices. |
| `dibujar_grafo` | Representa el grafo dirigido mediante NetworkX y Matplotlib. |

La visualización distingue:

- Camino mínimo en azul.
- Caminos sin arcos compartidos con diferentes colores.
- Corte mínimo en rojo punteado.
- Pasillos bloqueados en gris claro.
- Entrada y salida mediante bordes diferenciados.

**app.py**

| Función | Descripción |
|---|---|
| `inicializar_estado` | Carga el grafo inicial en la sesión. |
| `panel_seleccion_extremos` | Permite seleccionar entrada y salida. |
| `panel_bloqueos` | Bloquea y restablece pasillos. |
| `panel_agregar_arco` | Permite agregar pasillos válidos. |
| `panel_restaurar` | Restaura la red original. |
| `panel_resultados` | Muestra los cálculos, gráficos y verificaciones. |
| `panel_comparacion` | Compara las tres configuraciones. |
| `ejecutar_aplicacion` | Organiza e inicia la aplicación Streamlit. |

La interfaz tiene dos pestañas principales:

1. **Simulación interactiva:** permite modificar el grafo y recalcular los resultados.
2. **Comparación de configuraciones:** muestra la red original y las dos modificaciones.

---

## Pruebas automatizadas

Las pruebas están desarrolladas con pytest y se encuentran en la carpeta `tests/`.

| Archivo | Qué verifica |
|---|---|
| `conftest.py` | Configuración compartida para las pruebas. |
| `test_grafo.py` | Métodos y restricciones de la clase GrafoDirigido. |
| `test_cargador.py` | Carga y manejo de archivos JSON. |
| `test_validaciones.py` | Validación matemática de la red inicial. |
| `test_busquedas.py` | BFS, DFS y casos sin camino. |
| `test_flujo_y_corte.py` | Flujo máximo, rutas independientes y corte mínimo. |
| `test_caso_manual.py` | Contraste entre resultados manuales y algoritmos. |
| `test_verificador.py` | Comprobaciones independientes de los resultados. |
| `test_visualizacion.py` | Funciones de representación gráfica. |
| `test_configuraciones.py` | Cálculo y comparación de configuraciones. |

Para ejecutar todas las pruebas:

```powershell
python -m pytest -q
```

Resultado registrado:

```text
64 passed
```

---

## Documentación

Los siguientes archivos de documentación están presentes en la versión revisada del repositorio.

| Archivo o carpeta | Contenido |
|---|---|
| `docs/fuentes.md` | Fuentes académicas y técnicas utilizadas. |
| `docs/informe/seccion1_modelo.md` | Modelación matemática del laberinto. |
| `docs/informe/seccion5_verificacion.md` | Verificación manual y matemática. |
| `docs/imagenes/` | Carpeta preparada para incorporar imágenes y capturas. |


---

## Fundamento matemático

El proyecto utiliza conceptos de teoría de grafos y algoritmos clásicos.

**Camino mínimo:** BFS obtiene la menor cantidad de arcos entre la entrada y la salida en un grafo no ponderado.

**Caminos sin arcos compartidos:** el flujo máximo con capacidad unitaria determina el número máximo de rutas dirigidas que no reutilizan pasillos.

**Corte mínimo:** la red residual final permite identificar el conjunto mínimo de arcos que desconecta el origen del destino.

La relación matemática fundamental es:

Máximo número de caminos sin arcos compartidos = tamaño del corte mínimo.

Esta igualdad está fundamentada en el teorema de flujo máximo–corte mínimo y la versión por arcos del teorema de Menger.

---

## Consideraciones finales

El proyecto cumple su propósito de representar un laberinto dirigido, resolver problemas de conectividad y analizar modificaciones de la red.

Los algoritmos matemáticos están desarrollados mediante código propio, mientras que Streamlit, NetworkX y Matplotlib proporcionan la interfaz y la visualización.

El código fuente, sus dependencias, los datos de prueba y las instrucciones de ejecución están organizados en este repositorio.
