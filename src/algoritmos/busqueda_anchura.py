"""BFS: camino dirigido con el menor número de arcos. Complejidad O(V + E)."""
from collections import deque
from typing import Dict, List, Optional, Tuple
from src.modelo.grafo import GrafoDirigido


def busqueda_en_anchura(grafo: GrafoDirigido, origen: str) -> Tuple[Dict[str, int], Dict[str, Optional[str]]]:
    """Recorre el grafo por niveles desde un vértice y registra rutas mínimas.

    BFS visita primero los vértices a menor distancia; por eso determina
    la cantidad mínima de arcos para llegar a cada vértice alcanzable.
    Complejidad temporal: O(|V| + |E|).

    Parámetros:
        grafo: grafo dirigido que proporciona sucesores por arcos activos.
        origen: identificador de un vértice existente desde el que se busca.

    Retorna:
        Tupla (distancias, predecesores). distancias asocia cada vértice
        alcanzable con su distancia mínima en arcos, y predecesores guarda
        el vértice anterior en el recorrido (None para el origen).
        Los vértices inalcanzables no aparecen en los diccionarios.

    Errores:
        ValueError si el vértice de origen no existe.
    """
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
    """Reconstruye una ruta de origen a destino siguiendo los predecesores.

    Retrocede desde destino hasta origen y luego invierte la secuencia.
    La longitud de la ruta reconstruida es mínima cuando los predecesores
    provienen de una búsqueda BFS desde el mismo origen.

    Parámetros:
        predecesores: diccionario de vértices y su predecesor, con None
            en la raíz del recorrido.
        origen: vértice inicial de la ruta que se desea reconstruir.
        destino: vértice final de la ruta.

    Retorna:
        Lista ordenada de vértices desde origen hasta destino, incluidos
        ambos extremos; None si faltan extremos o la cadena de
        predecesores no llega al origen.
    """
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
    """Obtiene un camino dirigido con el menor número de arcos mediante BFS.

    Usa distancias por niveles y reconstruye una solución válida usando
    únicamente pasillos activos. Complejidad temporal: O(|V| + |E|).

    Parámetros:
        grafo: grafo dirigido con arcos activos y vértices registrados.
        origen: vértice de partida, que debe existir en el grafo.
        destino: vértice de llegada, que debe existir en el grafo.

    Retorna:
        Tupla (camino, longitud), donde camino es la lista de vértices
        y longitud es su número de arcos. Retorna (None, None) si no
        existe una ruta; si origen y destino coinciden, retorna
        ([origen], 0).

    Errores:
        ValueError si origen o destino no existe.
    """
    grafo._exigir_vertice(destino)
    _, predecesores = busqueda_en_anchura(grafo, origen)
    camino = reconstruir_camino(predecesores, origen, destino)
    return (camino, len(camino) - 1) if camino is not None else (None, None)
