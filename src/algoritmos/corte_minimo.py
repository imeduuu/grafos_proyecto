"""Corte mínimo de arcos entre s y t.

El corte mínimo es el menor conjunto de arcos cuya eliminación impide
llegar de s a t. Por el teorema de flujo máximo y corte mínimo (Menger
para arcos), su tamaño es igual al máximo número de caminos sin arcos
compartidos.
"""

from typing import List, Set, Tuple
from src.algoritmos.flujo_maximo import RedResidual
from src.modelo.grafo import GrafoDirigido

def alcanzables_en_residual(residual: RedResidual, origen: str) -> Set[str]:
    """Calcula los vértices alcanzables desde origen en la red residual.

    Solo considera arcos con capacidad residual mayor que 0.

    Parámetros:
        residual: red residual final del flujo máximo.
        origen: vértice fuente s.

    Retorna:
        Conjunto S de vértices alcanzables desde origen.
    """
    raise NotImplementedError("TODO: implementar alcanzables_en_residual")


def corte_minimo(grafo: GrafoDirigido, origen: str, destino: str) -> List[Tuple[str, str]]:
    """Calcula un corte mínimo de arcos entre origen y destino.

    Ejecuta el flujo máximo, obtiene el conjunto S de alcanzables en la red
    residual y toma los arcos activos (u, v) con u en S y v fuera de S.

    Parámetros:
        grafo: laberinto sobre el que se calcula (solo arcos activos).
        origen: vértice de entrada s.
        destino: vértice de salida t.

    Retorna:
        Lista de arcos (u, v) del corte; [] si ya no existe camino (el
        conjunto vacío ya desconecta).
    """
    raise NotImplementedError("TODO: implementar corte_minimo")
