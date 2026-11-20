"""Comprobaciones de la sección 5 de la pauta.

Verifican los resultados de forma independiente: no deben usar los
algoritmos que verifican.
"""

from typing import List, Tuple
from src.modelo.grafo import GrafoDirigido

def verificar_camino_valido(grafo: GrafoDirigido, camino: List[str], origen: str, destino: str) -> bool:
    """Comprueba que un camino sea válido en el grafo.

    El camino debe empezar en origen, terminar en destino y cada par de
    vértices consecutivos debe ser un arco activo.

    Parámetros:
        grafo: laberinto sobre el que se verifica.
        camino: lista de vértices a revisar.
        origen: vértice de entrada s.
        destino: vértice de salida t.

    Retorna:
        True si el camino es válido; False en caso contrario.
    """
    raise NotImplementedError("TODO: implementar verificar_camino_valido")


def verificar_sin_arcos_compartidos(caminos: List[List[str]]) -> bool:
    """Comprueba que ningún arco aparezca en más de un camino.

    Los vértices sí pueden repetirse entre caminos.

    Parámetros:
        caminos: lista de caminos (listas de vértices).

    Retorna:
        True si los caminos no comparten arcos; False en caso contrario.
    """
    raise NotImplementedError("TODO: implementar verificar_sin_arcos_compartidos")


def verificar_corte_desconecta(grafo: GrafoDirigido, corte: List[Tuple[str, str]], origen: str, destino: str) -> bool:
    """Comprueba que el corte desconecte el origen del destino.

    Bloquea los arcos del corte en una COPIA del grafo y revisa que ya no
    exista camino de origen a destino.

    Parámetros:
        grafo: laberinto original (no se modifica).
        corte: lista de arcos (u, v) del corte.
        origen: vértice de entrada s.
        destino: vértice de salida t.

    Retorna:
        True si el corte desconecta s de t; False en caso contrario.
    """
    raise NotImplementedError("TODO: implementar verificar_corte_desconecta")


def verificar_igualdad_menger(cantidad_caminos: int, corte: List[Tuple[str, str]]) -> bool:
    """Comprueba Menger: caminos sin arcos compartidos = tamaño del corte.

    Parámetros:
        cantidad_caminos: máximo número de caminos sin arcos compartidos.
        corte: lista de arcos del corte mínimo.

    Retorna:
        True si cantidad_caminos == len(corte); False en caso contrario.
    """
    raise NotImplementedError("TODO: implementar verificar_igualdad_menger")


def verificar_todo(grafo: GrafoDirigido, resultado) -> dict:
    """Ejecuta todas las comprobaciones sobre los resultados de una configuración.

    Parámetros:
        grafo: laberinto sobre el que se calcularon los resultados.
        resultado: ResultadoConfiguracion a verificar.

    Retorna:
        Diccionario {nombre_verificacion: bool}.
    """
    raise NotImplementedError("TODO: implementar verificar_todo")
