from typing import List, Set, Tuple
from src.algoritmos.flujo_maximo import RedResidual
from src.modelo.grafo import GrafoDirigido

def alcanzables_en_residual(residual: RedResidual, origen: str) -> Set[str]:
    raise NotImplementedError("TODO: implementar alcanzables_en_residual")


def corte_minimo(grafo: GrafoDirigido, origen: str, destino: str) -> List[Tuple[str, str]]:
    raise NotImplementedError("TODO: implementar corte_minimo")
