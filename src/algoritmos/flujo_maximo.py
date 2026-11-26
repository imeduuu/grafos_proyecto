"""Flujo máximo de Edmonds-Karp con capacidad unitaria por arco.

La complejidad temporal general es O(|V|·|E|²). El algoritmo, la búsqueda
de caminos aumentantes y la descomposición del flujo se implementan con
estructuras básicas de Python, sin bibliotecas externas para el cálculo.
"""
from collections import deque
from typing import Dict, List, Optional, Tuple
from src.modelo.grafo import GrafoDirigido

RedResidual = Dict[str, Dict[str, int]]


def construir_red_residual(grafo: GrafoDirigido) -> RedResidual:
    """Construye la red residual inicial con capacidad unitaria por pasillo.

    Cada arco activo original comienza con capacidad residual 1 y su
    inverso comienza con 0. Los arcos bloqueados quedan excluidos.
    La red residual permite cancelar o redirigir flujo posteriormente.

    Parámetros:
        grafo: grafo dirigido con conjunto de vértices y arcos activos.

    Retorna:
        Diccionario anidado residual[u][v] con la capacidad disponible
        para avanzar desde u hacia v. Se incluyen todos los vértices,
        aunque no tengan arcos activos.
    """
    residual = {vertice: {} for vertice in grafo.vertices}
    for u, v in grafo.arcos_activos():
        residual[u][v] = 1
        residual[v].setdefault(u, 0)
    return residual


def buscar_camino_aumentante(residual: RedResidual, origen: str, destino: str) -> Optional[List[str]]:
    """Encuentra mediante BFS una ruta con capacidad residual positiva.

    Recorre la red residual por niveles, considerando también arcos
    inversos que permiten reajustar un flujo anterior.
    Complejidad por búsqueda: O(|V| + |E|).

    Parámetros:
        residual: capacidades residuales indexadas por origen y destino;
            los extremos consultados deben existir como claves.
        origen: vértice desde el cual se busca aumentar el flujo.
        destino: vértice al que debe llegar el camino aumentante.

    Retorna:
        Lista ordenada de vértices de un camino aumentante, o None
        si no queda camino con capacidad positiva. Si origen y destino
        son iguales también retorna None.
    """
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
    """Envía una unidad de flujo por un camino de la red residual.

    Reduce en 1 la capacidad residual en el sentido recorrido y aumenta
    en 1 la capacidad inversa. Modifica el diccionario recibido en sitio.

    Parámetros:
        residual: red residual que se actualiza directamente.
        camino: lista de vértices consecutivos cuyos arcos residuales
            deben existir y tener capacidad positiva.

    Retorna:
        None. La red residual queda actualizada con una unidad más
        de flujo a través del camino indicado.

    Errores:
        ValueError si un arco recorrido no tiene capacidad disponible.
        KeyError si un arco indicado no existe en la red residual.
    """
    for u, v in zip(camino, camino[1:]):
        if residual[u][v] <= 0:
            raise ValueError(f"No queda capacidad residual para {u}->{v}.")
        residual[u][v] -= 1
        residual[v][u] += 1


def flujo_maximo_unitario(grafo: GrafoDirigido, origen: str, destino: str) -> Tuple[int, RedResidual]:
    """Calcula el flujo máximo de origen a destino con Edmonds-Karp.

    Aplica Ford-Fulkerson eligiendo caminos aumentantes mediante BFS.
    Cada arco activo tiene capacidad 1: una unidad de flujo puede
    corresponder a un camino y dos unidades no pueden usar el mismo arco.
    La cota general de Edmonds-Karp es O(|V|·|E|²); aquí cada aumento
    es de una unidad y el número de aumentos no supera el grado de
    salida activo del origen, por lo que la ejecución también queda
    acotada por esas iteraciones de BFS.

    Parámetros:
        grafo: grafo dirigido con arcos activos de capacidad unitaria.
        origen: vértice de entrada existente.
        destino: vértice de salida existente y distinto del origen.

    Retorna:
        Tupla (valor, residual), con el flujo máximo entero y la red
        residual final. Si no hay camino, el valor es 0.

    Errores:
        ValueError si falta un extremo o si origen y destino coinciden.
    """
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
    """Extrae caminos dirigidos del flujo representado en la red residual.

    En un arco original activo, residual[u][v] == 0 indica que ese arco
    lleva una unidad de flujo. Busca rutas de origen a destino usando
    solo esos arcos, evita ciclos dentro de cada ruta y retira los arcos
    utilizados para que ninguna pareja de caminos comparta un pasillo.

    Parámetros:
        grafo: grafo dirigido con los arcos activos originales.
        residual: red residual resultante de calcular el flujo máximo.
        origen: vértice inicial de los caminos que se extraerán.
        destino: vértice final de los caminos que se extraerán.

    Retorna:
        Lista de caminos; cada camino es una lista de vértices desde
        origen hasta destino. Devuelve [] cuando no puede extraerse
        ninguno. Pueden quedar arcos con flujo que formen ciclos y no
        pertenezcan a los caminos entregados.
    """
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
    """Obtiene la cantidad máxima de caminos sin arcos compartidos.

    Calcula flujo máximo con capacidad 1 por arco y lo descompone en
    caminos. Una unidad de flujo por ruta impide reutilizar pasillos;
    por el teorema de flujo máximo-corte mínimo, el número hallado es
    máximo. Usa Edmonds-Karp, de cota general O(|V|·|E|²).

    Parámetros:
        grafo: grafo dirigido cuyos arcos activos son los permitidos.
        origen: vértice de entrada existente.
        destino: vértice de salida existente y distinto del origen.

    Retorna:
        Tupla (cantidad, caminos), con la cantidad máxima y las rutas
        concretas que la alcanzan. Si no hay conexión, retorna (0, []).

    Errores:
        ValueError si los extremos no existen o son iguales.
        RuntimeError si el flujo calculado no puede descomponerse
        completamente en la cantidad esperada de caminos.
    """
    valor, residual = flujo_maximo_unitario(grafo, origen, destino)
    if valor == 0:
        return 0, []
    caminos = descomponer_en_caminos(grafo, residual, origen, destino)
    if len(caminos) != valor:
        raise RuntimeError("No fue posible descomponer completamente el flujo máximo.")
    return valor, caminos
