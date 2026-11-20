"""Búsqueda en profundidad (DFS).

Se usa solo para comparar con BFS en el informe: encuentra un camino si
existe, pero no garantiza que sea el más corto.
"""

from typing import List, Optional
from src.modelo.grafo import GrafoDirigido

def busqueda_en_profundidad(grafo: GrafoDirigido, origen: str, destino: str) -> Optional[List[str]]:
    """Busca un camino de origen a destino con DFS iterativo (pila y visitados).

    Solo avanza por arcos activos.

    Parámetros:
        grafo: laberinto sobre el que se busca.
        origen: vértice de inicio.
        destino: vértice que se quiere alcanzar.

    Retorna:
        Lista de vértices de un camino de origen a destino (no necesariamente
        el más corto), o None si no existe.
    """
    raise NotImplementedError("TODO: implementar busqueda_en_profundidad")


def existe_camino(grafo: GrafoDirigido, origen: str, destino: str) -> bool:
    """Indica si destino es alcanzable desde origen usando arcos activos.

    Parámetros:
        grafo: laberinto sobre el que se busca.
        origen: vértice de inicio.
        destino: vértice que se quiere alcanzar.

    Retorna:
        True si existe un camino de origen a destino; False en caso contrario.
    """
    raise NotImplementedError("TODO: implementar existe_camino")
