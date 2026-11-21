"""Corte mínimo de arcos usando el teorema de flujo máximo y corte mínimo."""
from collections import deque
from typing import List, Set, Tuple
from src.algoritmos.flujo_maximo import RedResidual, flujo_maximo_unitario
from src.modelo.grafo import GrafoDirigido


def alcanzables_en_residual(residual: RedResidual, origen: str) -> Set[str]:
    """Devuelve los vértices alcanzables con capacidad residual positiva."""
    visitados = {origen}
    cola = deque([origen])
    while cola:
        u = cola.popleft()
        for v, capacidad in residual[u].items():
            if capacidad > 0 and v not in visitados:
                visitados.add(v)
                cola.append(v)
    return visitados


def corte_minimo(grafo: GrafoDirigido, origen: str, destino: str) -> List[Tuple[str, str]]:
    """Retorna arcos activos del corte mínimo; [] si ya está desconectado."""
    valor, residual = flujo_maximo_unitario(grafo, origen, destino)
    if valor == 0:
        return []
    alcanzables = alcanzables_en_residual(residual, origen)
    return [(u, v) for u, v in grafo.arcos_activos() if u in alcanzables and v not in alcanzables]
