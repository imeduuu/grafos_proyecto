"""Dibujo del laberinto con matplotlib.

networkx se usa SOLO para dibujar, nunca para calcular. Colores: camino
mínimo azul grueso, cada camino disjunto de un color distinto, corte rojo
punteado, arcos bloqueados gris claro punteado, entrada s con borde verde
y salida t con borde rojo.
"""

from typing import List, Optional, Tuple
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

def calcular_posiciones(grafo: GrafoDirigido) -> dict:
    """Obtiene la posición de dibujo de cada vértice.

    Usa ``grafo.posiciones`` si están definidas para todos los vértices; si
    no, calcula una distribución automática.

    Parámetros:
        grafo: laberinto a dibujar.

    Retorna:
        Diccionario {vertice: (x, y)}.
    """
    raise NotImplementedError("TODO: implementar calcular_posiciones")


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
    raise NotImplementedError("TODO: implementar dibujar_grafo")
