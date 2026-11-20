"""Búsqueda en anchura (BFS) para el camino con menor número de arcos.

BFS recorre el grafo por niveles: primero los vértices a distancia 1, luego
los de distancia 2, etc. Por eso, en un grafo sin pesos, la primera vez que
alcanza un vértice lo hace con la distancia mínima, y garantiza d(s, t).
Complejidad: O(|V| + |E|). Prohibido usar networkx para calcular.
"""

from typing import Dict, List, Optional, Tuple
from src.modelo.grafo import GrafoDirigido

def busqueda_en_anchura(grafo: GrafoDirigido, origen: str) -> Tuple[Dict[str, int], Dict[str, Optional[str]]]:
    """Recorre el grafo por niveles desde ``origen`` usando una cola.

    Solo avanza por arcos activos (``grafo.sucesores``).

    Parámetros:
        grafo: laberinto sobre el que se busca.
        origen: vértice desde el que comienza el recorrido.

    Retorna:
        Tupla (distancias, predecesores): distancias[v] es el número mínimo de
        arcos de origen a v; predecesores[v] es el vértice anterior a v en ese
        recorrido (None para el origen). Solo incluye los vértices alcanzados.
    """
    raise NotImplementedError("TODO: implementar busqueda_en_anchura (usar collections.deque)")


def reconstruir_camino(predecesores: Dict[str, Optional[str]], origen: str, destino: str) -> Optional[List[str]]:
    """Arma el camino [origen, ..., destino] siguiendo los predecesores hacia atrás.

    Parámetros:
        predecesores: diccionario retornado por ``busqueda_en_anchura``.
        origen: vértice inicial del camino.
        destino: vértice final del camino.

    Retorna:
        Lista de vértices desde origen hasta destino, o None si destino no fue
        alcanzado.
    """
    raise NotImplementedError("TODO: implementar reconstruir_camino")


def camino_minimo(grafo: GrafoDirigido, origen: str, destino: str) -> Tuple[Optional[List[str]], Optional[int]]:
    """Función principal: calcula un camino con el menor número de arcos.

    Parámetros:
        grafo: laberinto sobre el que se busca (solo arcos activos).
        origen: vértice de entrada s.
        destino: vértice de salida t.

    Retorna:
        Tupla (camino, longitud) con la lista de vértices y su número de arcos,
        o (None, None) si no existe camino; nunca se inventa una longitud.
    """
    raise NotImplementedError("TODO: implementar camino_minimo")
