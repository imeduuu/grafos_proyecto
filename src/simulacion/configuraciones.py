from dataclasses import dataclass, field
from typing import List, Optional, Tuple
from src.modelo.grafo import GrafoDirigido

@dataclass
class ResultadoConfiguracion:

    nombre: str
    existe_camino: bool = False
    camino_minimo: Optional[List[str]] = None
    longitud_minima: Optional[int] = None
    cantidad_caminos_disjuntos: int = 0
    caminos_disjuntos: List[List[str]] = field(default_factory=list)
    corte_minimo: List[Tuple[str, str]] = field(default_factory=list)

def calcular_resultados(grafo: GrafoDirigido, nombre: str = "Configuración") -> ResultadoConfiguracion:
    raise NotImplementedError("TODO: implementar calcular_resultados")


def comparar_configuraciones(resultados: List[ResultadoConfiguracion]) -> List[dict]:
    raise NotImplementedError("TODO: implementar comparar_configuraciones")
