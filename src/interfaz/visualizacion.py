#Dibujo del laberinto con matplotlib.

#networkx se usa SOLO para dibujar, nunca para calcular. Colores: camino
#mínimo azul grueso, cada camino disjunto de un color distinto, corte rojo
#punteado, arcos bloqueados gris claro punteado, entrada s con borde verde
#y salida t con borde rojo.


from typing import List, Optional, Tuple

import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.lines import Line2D

from src.modelo.grafo import GrafoDirigido

COLORES = {
    "normal": "#9e9e9e",
    "bloqueado": "#d0d0d0",
    "camino_minimo": "#1f77b4",
    "corte": "#d62728",
    "entrada": "#2ca02c",
    "salida": "#d62728",
    "caminos_disjuntos": ["#2ca02c", "#ff7f0e", "#9467bd", "#8c564b", "#e377c2"],
}

MODOS = ("todo", "camino_minimo", "disjuntos", "corte")

# Tamaño de los vértices (se pasa tambien al dibujar arcos)
TAMANO_VERTICE = 900

# Curvatura leve de los arcos
ESTILO_CONEXION = "arc3,rad=0.08"


def calcular_posiciones(grafo: GrafoDirigido) -> dict:
    """Obtiene la posición de dibujo de cada vértice.

    Usa ``grafo.posiciones`` si están definidas para todos los vértices; si
    no, calcula una distribución automática.

    Parámetros:
        grafo: laberinto a dibujar.

    Retorna:
        Diccionario {vertice: (x, y)}.
    """
    if grafo.vertices and all(v in grafo.posiciones for v in grafo.vertices):
        # Copia: así quien reciba el diccionario no modifica el grafo.
        return {v: tuple(grafo.posiciones[v]) for v in grafo.vertices}

    # Distribución automática. Los vértices se ordenan porque grafo.vertices
    # es un set y su orden cambia entre ejecuciones; con orden fijo y seed=1
    # el dibujo sale siempre igual.
    auxiliar = nx.DiGraph()
    auxiliar.add_nodes_from(sorted(grafo.vertices))
    auxiliar.add_edges_from(grafo.arcos())
    posiciones = nx.spring_layout(auxiliar, seed=1)
    return {v: (float(x), float(y)) for v, (x, y) in posiciones.items()}


def _arcos_de_camino(camino: List[str]) -> List[Tuple[str, str]]:
    """Convierte un camino [v0, v1, ..., vk] en sus arcos [(v0, v1), ..., (vk-1, vk)].

    Parámetros:
        camino: secuencia de vértices.

    Retorna:
        Lista de arcos consecutivos del camino.
    """
    return list(zip(camino, camino[1:]))


def _texto_arcos(cantidad: int) -> str:
    """Retorna "1 arco" o "N arcos" según la cantidad.

    Parámetros:
        cantidad: número de arcos.

    Retorna:
        Texto con la cantidad y la palabra en singular o plural.
    """
    return f"{cantidad} arco" if cantidad == 1 else f"{cantidad} arcos"


def _dibujar_arcos(dibujo, posiciones, ax, arcos, color, ancho, estilo="solid", alfa=1.0) -> None:
    """Dibuja un grupo de arcos dirigidos con un mismo estilo.

    Parámetros:
        dibujo: nx.DiGraph usado solo para dibujar.
        posiciones: diccionario {vertice: (x, y)}.
        ax: eje de matplotlib donde se dibuja.
        arcos: lista de arcos (u, v) a dibujar.
        color: color de las líneas y flechas.
        ancho: grosor de la línea.
        estilo: "solid" o "dashed".
        alfa: opacidad entre 0 y 1.

    Retorna:
        None.
    """
    if not arcos:
        return
    nx.draw_networkx_edges(
        dibujo,
        posiciones,
        edgelist=arcos,
        ax=ax,
        edge_color=color,
        width=ancho,
        style=estilo,
        alpha=alfa,
        arrows=True,
        arrowstyle="-|>",
        arrowsize=18,
        node_size=TAMANO_VERTICE,
        connectionstyle=ESTILO_CONEXION,
    )


def dibujar_grafo(
    grafo: GrafoDirigido,
    camino_minimo: Optional[List[str]] = None,
    caminos_disjuntos: Optional[List[List[str]]] = None,
    corte: Optional[List[Tuple[str, str]]] = None,
    modo: str = "todo",
):
    """Dibuja el laberinto con flechas y destaca la solución según el modo.

    Parámetros:
        grafo: laberinto a dibujar.
        camino_minimo: camino con menos arcos a destacar (opcional).
        caminos_disjuntos: caminos sin arcos compartidos a destacar (opcional).
        corte: arcos del corte mínimo a destacar (opcional).
        modo: qué destacar: "todo", "camino_minimo", "disjuntos" o "corte".

    Retorna:
        La figura de matplotlib.
    """
    if modo not in MODOS:
        raise ValueError(f"Modo '{modo}' no válido. Use uno de: {', '.join(MODOS)}.")

    # Grafo de networkx
    dibujo = nx.DiGraph()
    dibujo.add_nodes_from(sorted(grafo.vertices))
    dibujo.add_edges_from(grafo.arcos())
    posiciones = calcular_posiciones(grafo)

    fig, ax = plt.subplots(figsize=(10, 6))
    leyenda = []

    # 1. Base: todos los pasillos activos en gris
    activos = grafo.arcos_activos()
    bloqueados = [arco for arco in grafo.arcos() if grafo.esta_bloqueado(*arco)]
    _dibujar_arcos(dibujo, posiciones, ax, activos, COLORES["normal"], 1.5)
    _dibujar_arcos(dibujo, posiciones, ax, bloqueados, COLORES["bloqueado"], 1.5, estilo="dashed")
    leyenda.append(Line2D([], [], color=COLORES["normal"], lw=1.5, label="Pasillo"))
    if bloqueados:
        leyenda.append(Line2D([], [], color=COLORES["bloqueado"], lw=1.5, ls="--", label="Pasillo bloqueado"))

    # 2. Camino mínimo en azul grueso
    if modo in ("todo", "camino_minimo") and camino_minimo:
        ancho, alfa = (7, 0.35) if modo == "todo" else (4, 1.0)
        _dibujar_arcos(dibujo, posiciones, ax, _arcos_de_camino(camino_minimo),
                       COLORES["camino_minimo"], ancho, alfa=alfa)
        leyenda.append(Line2D([], [], color=COLORES["camino_minimo"], lw=ancho, alpha=alfa,
                              label=f"Camino mínimo ({_texto_arcos(len(camino_minimo) - 1)})"))

    # 3. Cada camino sin arcos compartidos con un color distinto
    if modo in ("todo", "disjuntos") and caminos_disjuntos:
        paleta = COLORES["caminos_disjuntos"]
        for i, camino in enumerate(caminos_disjuntos):
            color = paleta[i % len(paleta)]
            _dibujar_arcos(dibujo, posiciones, ax, _arcos_de_camino(camino), color, 2.5)
            leyenda.append(Line2D([], [], color=color, lw=2.5, label=f"Camino disjunto {i + 1}"))

    # 4. Corte mínimo en rojo punteado, al final para que quede encima
    if modo in ("todo", "corte") and corte:
        _dibujar_arcos(dibujo, posiciones, ax, corte, COLORES["corte"], 3, estilo="dashed")
        leyenda.append(Line2D([], [], color=COLORES["corte"], lw=3, ls="--",
                              label=f"Corte mínimo ({_texto_arcos(len(corte))})"))

    # 5. Vértices: fondo blanco, borde verde para s, rojo para t y negro
    #    para el resto. s y t con borde más grueso para distinguirlos.
    nodos = list(dibujo.nodes)
    bordes = []
    grosores = []
    for v in nodos:
        if v == grafo.entrada:
            bordes.append(COLORES["entrada"])
            grosores.append(3.5)
        elif v == grafo.salida:
            bordes.append(COLORES["salida"])
            grosores.append(3.5)
        else:
            bordes.append("black")
            grosores.append(1.2)
    nx.draw_networkx_nodes(dibujo, posiciones, nodelist=nodos, ax=ax, node_size=TAMANO_VERTICE,
                           node_color="white", edgecolors=bordes, linewidths=grosores)
    nx.draw_networkx_labels(dibujo, posiciones, ax=ax, font_size=12, font_weight="bold")

    if grafo.entrada is not None:
        leyenda.append(Line2D([], [], marker="o", ls="", markersize=12, markerfacecolor="white",
                              markeredgecolor=COLORES["entrada"], markeredgewidth=3,
                              label=f"Entrada ({grafo.entrada})"))
    if grafo.salida is not None:
        leyenda.append(Line2D([], [], marker="o", ls="", markersize=12, markerfacecolor="white",
                              markeredgecolor=COLORES["salida"], markeredgewidth=3,
                              label=f"Salida ({grafo.salida})"))

    # Leyenda fuera del área del grafo para no tapar vértices ni arcos
    ax.legend(handles=leyenda, loc="upper left", bbox_to_anchor=(1.01, 1), frameon=False)
    ax.axis("off")
    fig.tight_layout()
    return fig
