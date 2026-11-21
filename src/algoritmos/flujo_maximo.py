"""Edmonds-Karp con capacidad unitaria: caminos dirigidos sin arcos compartidos."""
from collections import deque
from typing import Dict, List, Optional, Tuple
from src.modelo.grafo import GrafoDirigido

RedResidual = Dict[str, Dict[str, int]]


def construir_red_residual(grafo: GrafoDirigido) -> RedResidual:
    """Crea capacidades 1 en arcos activos y 0 en sus inversos."""
    residual = {vertice: {} for vertice in grafo.vertices}
    for u, v in grafo.arcos_activos():
        residual[u][v] = 1
        residual[v].setdefault(u, 0)
    return residual


def buscar_camino_aumentante(residual: RedResidual, origen: str, destino: str) -> Optional[List[str]]:
    """BFS de capacidades residuales positivas; retorna camino o None."""
    if origen == destino:
        return None
    cola = deque([origen])
    padres = {origen: None}
    while cola:
        u = cola.popleft()
        for v, capacidad in residual[u].items():
            if capacidad > 0 and v not in padres:
                padres[v] = u
                if v == destino:
                    camino = [destino]
                    while camino[-1] != origen:
                        camino.append(padres[camino[-1]])
                    camino.reverse()
                    return camino
                cola.append(v)
    return None


def aumentar_flujo(residual: RedResidual, camino: List[str]) -> None:
    """Envía una unidad por el camino, actualizando arcos directos e inversos."""
    for u, v in zip(camino, camino[1:]):
        if residual[u][v] <= 0:
            raise ValueError(f"No queda capacidad residual para {u}->{v}.")
        residual[u][v] -= 1
        residual[v][u] += 1


def flujo_maximo_unitario(grafo: GrafoDirigido, origen: str, destino: str) -> Tuple[int, RedResidual]:
    """Devuelve valor máximo del flujo y red residual final."""
    grafo._exigir_vertice(origen)
    grafo._exigir_vertice(destino)
    if origen == destino:
        raise ValueError("La entrada y la salida deben ser distintas.")
    residual = construir_red_residual(grafo)
    valor = 0
    while True:
        camino = buscar_camino_aumentante(residual, origen, destino)
        if camino is None:
            break
        aumentar_flujo(residual, camino)
        valor += 1
    return valor, residual


def descomponer_en_caminos(grafo: GrafoDirigido, residual: RedResidual, origen: str, destino: str) -> List[List[str]]:
    """Extrae caminos s-t del flujo final evitando ciclos y reutilización de arcos."""
    # En capacidades unitarias, capacidad residual 0 en un arco original
    # significa que circula una unidad de flujo por él.
    arcos_con_flujo = {(u, v) for u, v in grafo.arcos_activos() if residual[u][v] == 0}
    caminos = []
    while True:
        pila = [(origen, [origen])]
        encontrado = None
        while pila:
            u, camino = pila.pop()
            if u == destino:
                encontrado = camino
                break
            for v in grafo.sucesores(u):
                if (u, v) in arcos_con_flujo and v not in camino:
                    pila.append((v, camino + [v]))
        if encontrado is None:
            break
        caminos.append(encontrado)
        for arco in zip(encontrado, encontrado[1:]):
            arcos_con_flujo.remove(arco)
    return caminos


def maximo_caminos_disjuntos(grafo: GrafoDirigido, origen: str, destino: str) -> Tuple[int, List[List[str]]]:
    """Obtiene máxima cantidad y caminos concretos sin arcos comunes."""
    valor, residual = flujo_maximo_unitario(grafo, origen, destino)
    if valor == 0:
        return 0, []
    caminos = descomponer_en_caminos(grafo, residual, origen, destino)
    if len(caminos) != valor:
        raise RuntimeError("No fue posible descomponer completamente el flujo máximo.")
    return valor, caminos
