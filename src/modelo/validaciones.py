from typing import List
from src.modelo.grafo import GrafoDirigido

def tiene_lazos(grafo: GrafoDirigido) -> bool:
    raise NotImplementedError("TODO: implementar tiene_lazos")

def tiene_arcos_reciprocos(grafo: GrafoDirigido) -> bool:
    raise NotImplementedError("TODO: implementar tiene_arcos_reciprocos")

def vertices_aislados(grafo: GrafoDirigido) -> List[str]:
    raise NotImplementedError("TODO: implementar vertices_aislados")

def validar_configuracion_inicial(grafo: GrafoDirigido) -> List[str]:
    raise NotImplementedError("TODO: implementar validar_configuracion_inicial")
