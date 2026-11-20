"""Máximo número de caminos s-t sin arcos compartidos mediante flujo máximo.

Cada arco activo recibe capacidad 1 y se aplica Edmonds-Karp (caminos
aumentantes encontrados con BFS). El valor del flujo máximo es igual al
número máximo de caminos sin arcos compartidos. Como el grafo no permite
arcos recíprocos, el arco inverso de la red residual nunca choca con un
arco real.
"""

from typing import Dict, List, Optional, Tuple
from src.modelo.grafo import GrafoDirigido

RedResidual = Dict[str, Dict[str, int]]

def construir_red_residual(grafo: GrafoDirigido) -> RedResidual:
    """Construye la red residual inicial con capacidad unitaria.

    Asigna capacidad 1 a cada arco activo (u, v) y 0 a su inverso (v, u).

    Parámetros:
        grafo: laberinto del que se toman los arcos activos.

    Retorna:
        Diccionario residual[u][v] con la capacidad residual de cada arco.
    """
    raise NotImplementedError("TODO: implementar construir_red_residual")


def buscar_camino_aumentante(residual: RedResidual, origen: str, destino: str) -> Optional[List[str]]:
    """Busca un camino aumentante con BFS en la red residual.

    Solo recorre arcos con capacidad residual mayor que 0.

    Parámetros:
        residual: red residual actual.
        origen: vértice fuente s.
        destino: vértice sumidero t.

    Retorna:
        Lista de vértices del camino aumentante, o None si no existe.
    """
    raise NotImplementedError("TODO: implementar buscar_camino_aumentante")


def aumentar_flujo(residual: RedResidual, camino: List[str]) -> None:
    """Envía una unidad de flujo por el camino aumentante.

    Resta 1 a la capacidad de cada arco (u, v) del camino y suma 1 a su
    inverso (v, u). Modifica ``residual`` en el lugar.

    Parámetros:
        residual: red residual que se actualiza.
        camino: lista de vértices del camino aumentante.

    Retorna:
        None.
    """
    raise NotImplementedError("TODO: implementar aumentar_flujo")


def flujo_maximo_unitario(grafo: GrafoDirigido, origen: str, destino: str) -> Tuple[int, RedResidual]:
    """Calcula el flujo máximo con capacidad 1 por arco (Edmonds-Karp).

    Repite buscar un camino aumentante y aumentar el flujo hasta que no
    quede ninguno.

    Parámetros:
        grafo: laberinto (solo arcos activos).
        origen: vértice fuente s.
        destino: vértice sumidero t.

    Retorna:
        Tupla (valor_flujo, residual_final).
    """
    raise NotImplementedError("TODO: implementar flujo_maximo_unitario")


def descomponer_en_caminos(grafo: GrafoDirigido, residual: RedResidual, origen: str, destino: str) -> List[List[str]]:
    """Descompone el flujo máximo en caminos s-t.

    Un arco original activo lleva flujo si su capacidad residual quedó en 0.
    Desde el origen se siguen arcos con flujo aún no usados hasta llegar al
    destino.

    Parámetros:
        grafo: laberinto original (para saber qué arcos son reales y activos).
        residual: red residual final del flujo máximo.
        origen: vértice fuente s.
        destino: vértice sumidero t.

    Retorna:
        Lista de caminos (listas de vértices) que no comparten arcos.
    """
    raise NotImplementedError("TODO: implementar descomponer_en_caminos")


def maximo_caminos_disjuntos(grafo: GrafoDirigido, origen: str, destino: str) -> Tuple[int, List[List[str]]]:
    """Función principal: máximo número de caminos s-t sin arcos compartidos.

    Usa solo arcos activos.

    Parámetros:
        grafo: laberinto sobre el que se calcula.
        origen: vértice de entrada s.
        destino: vértice de salida t.

    Retorna:
        Tupla (cantidad, caminos); (0, []) si no existe camino.
    """
    raise NotImplementedError("TODO: implementar maximo_caminos_disjuntos")
