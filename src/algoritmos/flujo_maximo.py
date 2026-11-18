from typing import Dict, List, Optional, Tuple
from src.modelo.grafo import GrafoDirigido

RedResidual = Dict[str, Dict[str, int]]

def construir_red_residual(grafo: GrafoDirigido) -> RedResidual:
    raise NotImplementedError("TODO: implementar construir_red_residual")


def buscar_camino_aumentante(residual: RedResidual, origen: str, destino: str) -> Optional[List[str]]:
    raise NotImplementedError("TODO: implementar buscar_camino_aumentante")


def aumentar_flujo(residual: RedResidual, camino: List[str]) -> None:
    raise NotImplementedError("TODO: implementar aumentar_flujo")


def flujo_maximo_unitario(grafo: GrafoDirigido, origen: str, destino: str) -> Tuple[int, RedResidual]:
    raise NotImplementedError("TODO: implementar flujo_maximo_unitario")


def descomponer_en_caminos(grafo: GrafoDirigido, residual: RedResidual, origen: str, destino: str) -> List[List[str]]:
    raise NotImplementedError("TODO: implementar descomponer_en_caminos")


def maximo_caminos_disjuntos(grafo: GrafoDirigido, origen: str, destino: str) -> Tuple[int, List[List[str]]]:
    raise NotImplementedError("TODO: implementar maximo_caminos_disjuntos")
