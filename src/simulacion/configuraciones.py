"""Cálculo y comparación de resultados de la red original y sus modificaciones.

Todas las configuraciones se comparan con la misma entrada s y salida t.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Tuple
from src.algoritmos.busqueda_anchura import camino_minimo
from src.algoritmos.corte_minimo import corte_minimo
from src.algoritmos.flujo_maximo import maximo_caminos_disjuntos
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
    s, t = grafo.entrada, grafo.salida
    if s is None or t is None:
        raise ValueError("El grafo debe tener entrada y salida definidas antes de calcular.")

    camino, longitud = camino_minimo(grafo, s, t)
    cantidad, caminos = maximo_caminos_disjuntos(grafo, s, t)
    corte = corte_minimo(grafo, s, t)

    return ResultadoConfiguracion(
        nombre=nombre,
        existe_camino=camino is not None,
        camino_minimo=camino,
        longitud_minima=longitud,
        cantidad_caminos_disjuntos=cantidad,
        caminos_disjuntos=caminos,
        corte_minimo=corte,
    )


def formatear_camino(camino: Optional[List[str]]) -> str:
    """Convierte un camino [v0, ..., vk] en el texto "v0 → v1 → ... → vk".

    Parámetros:
        camino: lista de vértices, o None si no existe camino.

    Retorna:
        Texto del camino, o "No existe" si camino es None.
    """
    if camino is None:
        return "No existe"
    return " → ".join(camino)


def formatear_corte(corte: List[Tuple[str, str]]) -> str:
    """Convierte una lista de arcos en el texto "{u→v, ...}".

    Parámetros:
        corte: lista de arcos (u, v).

    Retorna:
        Texto del conjunto; "∅ (conjunto vacío)" si la lista está vacía.
    """
    if not corte:
        return "∅ (conjunto vacío)"
    return "{" + ", ".join(f"{u}→{v}" for u, v in corte) + "}"


def comparar_configuraciones(resultados: List[ResultadoConfiguracion]) -> List[dict]:
    """Arma la tabla comparativa de varias configuraciones.

    Genera una fila por configuración; si no hay camino muestra "No existe"
    en lugar de un número.

    Parámetros:
        resultados: lista de ResultadoConfiguracion a comparar.

    Retorna:
        Lista de diccionarios, uno por fila de la tabla.
    """
    filas = []
    for resultado in resultados:
        filas.append({
            "Configuración": resultado.nombre,
            "¿Existe camino s→t?": "Sí" if resultado.existe_camino else "No",
            "Camino mínimo": formatear_camino(resultado.camino_minimo),
            "Longitud mínima d(s,t)": (
                str(resultado.longitud_minima) if resultado.existe_camino else "No existe"
            ),
            "Máx. caminos sin arcos compartidos": resultado.cantidad_caminos_disjuntos,
            "Caminos sin arcos compartidos": (
                "; ".join(formatear_camino(c) for c in resultado.caminos_disjuntos)
                if resultado.caminos_disjuntos else "Ninguno (0 caminos)"
            ),
            "Corte mínimo": formatear_corte(resultado.corte_minimo),
            "|Corte mínimo|": len(resultado.corte_minimo),
        })
    return filas
