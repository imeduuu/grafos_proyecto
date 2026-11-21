"""BFS: camino dirigido con el menor número de arcos. Complejidad O(V + E)."""
from collections import deque
from typing import Dict, List, Optional, Tuple
from src.modelo.grafo import GrafoDirigido


def busqueda_en_anchura(grafo: GrafoDirigido, origen: str) -> Tuple[Dict[str, int], Dict[str, Optional[str]]]:
    """Retorna distancias mínimas y predecesores desde origen, usando solo arcos activos."""
    grafo._exigir_vertice(origen)
    cola = deque([origen])
    distancias = {origen: 0}
    predecesores = {origen: None}
    while cola:
        actual = cola.popleft()
        for vecino in grafo.sucesores(actual):
            if vecino not in distancias:
                distancias[vecino] = distancias[actual] + 1
                predecesores[vecino] = actual
                cola.append(vecino)
    return distancias, predecesores


def reconstruir_camino(predecesores: Dict[str, Optional[str]], origen: str, destino: str) -> Optional[List[str]]:
    """Reconstruye el camino usando los predecesores; None si no es alcanzable."""
    if origen not in predecesores or destino not in predecesores:
        return None
    camino = []
    actual = destino
    while actual is not None:
        camino.append(actual)
        if actual == origen:
            camino.reverse()
            return camino
        actual = predecesores.get(actual)
    return None


def camino_minimo(grafo: GrafoDirigido, origen: str, destino: str) -> Tuple[Optional[List[str]], Optional[int]]:
    """Retorna (camino, cantidad de arcos) o (None, None) si no existe."""
    grafo._exigir_vertice(destino)
    _, predecesores = busqueda_en_anchura(grafo, origen)
    camino = reconstruir_camino(predecesores, origen, destino)
    return (camino, len(camino) - 1) if camino is not None else (None, None)

