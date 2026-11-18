from typing import Dict, List, Optional, Tuple
from src.modelo.grafo import GrafoDirigido

def busqueda_en_anchura(grafo: GrafoDirigido, origen: str) -> Tuple[Dict[str, int], Dict[str, Optional[str]]]:
    raise NotImplementedError("TODO: implementar busqueda_en_anchura (usar collections.deque)")


def reconstruir_camino(predecesores: Dict[str, Optional[str]], origen: str, destino: str) -> Optional[List[str]]:
    raise NotImplementedError("TODO: implementar reconstruir_camino")


def camino_minimo(grafo: GrafoDirigido, origen: str, destino: str) -> Tuple[Optional[List[str]], Optional[int]]:
    raise NotImplementedError("TODO: implementar camino_minimo")
