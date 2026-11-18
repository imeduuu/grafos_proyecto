from typing import List, Tuple
from src.modelo.grafo import GrafoDirigido

def verificar_camino_valido(grafo: GrafoDirigido, camino: List[str], origen: str, destino: str) -> bool:
    raise NotImplementedError("TODO: implementar verificar_camino_valido")


def verificar_sin_arcos_compartidos(caminos: List[List[str]]) -> bool:
    raise NotImplementedError("TODO: implementar verificar_sin_arcos_compartidos")


def verificar_corte_desconecta(grafo: GrafoDirigido, corte: List[Tuple[str, str]], origen: str, destino: str) -> bool:
    raise NotImplementedError("TODO: implementar verificar_corte_desconecta")


def verificar_igualdad_menger(cantidad_caminos: int, corte: List[Tuple[str, str]]) -> bool:
    raise NotImplementedError("TODO: implementar verificar_igualdad_menger")


def verificar_todo(grafo: GrafoDirigido, resultado) -> dict:
    raise NotImplementedError("TODO: implementar verificar_todo")
