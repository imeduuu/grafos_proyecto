"""Cálculo y comparación de resultados de la red original y sus modificaciones.

Todas las configuraciones se comparan con la misma entrada s y salida t.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Tuple
from src.modelo.grafo import GrafoDirigido

@dataclass
class ResultadoConfiguracion:
    """Resultados calculados para una configuración del laberinto.

    Atributos:
        nombre: nombre de la configuración (por ejemplo "Original").
        existe_camino: True si existe al menos un camino s-t.
        camino_minimo: camino con menos arcos, o None si no hay camino.
        longitud_minima: número de arcos del camino mínimo (None si no hay camino).
        cantidad_caminos_disjuntos: máximo número de caminos sin arcos compartidos.
        caminos_disjuntos: lista de esos caminos.
        corte_minimo: arcos (u, v) de un corte mínimo.
    """

    nombre: str
    existe_camino: bool = False
    camino_minimo: Optional[List[str]] = None
    longitud_minima: Optional[int] = None
    cantidad_caminos_disjuntos: int = 0
    caminos_disjuntos: List[List[str]] = field(default_factory=list)
    corte_minimo: List[Tuple[str, str]] = field(default_factory=list)

def calcular_resultados(grafo: GrafoDirigido, nombre: str = "Configuración") -> ResultadoConfiguracion:
    """Calcula todos los resultados de una configuración (acción "Recalcular").

    Ejecuta camino mínimo, caminos sin arcos compartidos y corte mínimo
    usando ``grafo.entrada`` y ``grafo.salida``.

    Parámetros:
        grafo: laberinto con entrada y salida definidas.
        nombre: nombre con el que se identifica la configuración.

    Retorna:
        ResultadoConfiguracion con los resultados obtenidos.
    """
    raise NotImplementedError("TODO: implementar calcular_resultados")


def comparar_configuraciones(resultados: List[ResultadoConfiguracion]) -> List[dict]:
    """Arma la tabla comparativa de varias configuraciones.

    Genera una fila por configuración; si no hay camino muestra "No existe"
    en lugar de un número.

    Parámetros:
        resultados: lista de ResultadoConfiguracion a comparar.

    Retorna:
        Lista de diccionarios, uno por fila de la tabla.
    """
    raise NotImplementedError("TODO: implementar comparar_configuraciones")
