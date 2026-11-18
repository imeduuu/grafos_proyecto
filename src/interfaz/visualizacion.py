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
    raise NotImplementedError("TODO: implementar calcular_posiciones")


def dibujar_grafo(
    grafo: GrafoDirigido,
    camino_minimo: Optional[List[str]] = None,
    caminos_disjuntos: Optional[List[List[str]]] = None,
    corte: Optional[List[Tuple[str, str]]] = None,
    modo: str = "todo",
):
    raise NotImplementedError("TODO: implementar dibujar_grafo")
