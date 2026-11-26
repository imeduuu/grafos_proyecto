"""Corte mínimo de arcos obtenido desde el flujo máximo.

La complejidad temporal general es O(|V|·|E|²), dominada por Edmonds-Karp;
la búsqueda residual adicional es O(|V| + |E|). El cálculo es código propio
en Python y no utiliza bibliotecas externas de grafos.
"""
from collections import deque
from typing import List, Set, Tuple
from src.algoritmos.flujo_maximo import RedResidual, flujo_maximo_unitario
from src.modelo.grafo import GrafoDirigido


def alcanzables_en_residual(residual: RedResidual, origen: str) -> Set[str]:
    """Encuentra el lado S de un corte mediante capacidades residuales positivas.

    Desde el origen recorre los arcos con capacidad residual mayor que
    cero. Tras finalizar el flujo máximo, estos vértices conforman S;
    los demás pertenecen al lado opuesto del corte.
    Complejidad temporal: O(|V| + |E|).

    Parámetros:
        residual: red residual con capacidades para cada arco.
        origen: vértice inicial, que debe aparecer como clave en la red.

    Retorna:
        Conjunto de vértices alcanzables desde origen en la red
        residual, incluyendo siempre al propio origen.
    """
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
    """Identifica un conjunto mínimo de pasillos que desconecta origen y destino.

    Calcula el flujo máximo y obtiene S, los vértices alcanzables desde
    origen en la red residual final. Los arcos originales activos que
    salen de S hacia fuera de S forman el corte mínimo. Por el teorema
    de flujo máximo-corte mínimo (equivalentemente, la versión por arcos
    de Menger), su cardinalidad coincide con la cantidad máxima de
    caminos sin arcos compartidos.

    Parámetros:
        grafo: grafo dirigido con pasillos activos de capacidad 1.
        origen: vértice de entrada existente.
        destino: vértice de salida existente y distinto del origen.

    Retorna:
        Lista de tuplas (u, v) correspondientes a los arcos del corte
        mínimo. Devuelve [] si origen ya está desconectado de destino.

    Errores:
        ValueError si los extremos no existen o son iguales.
    """
    valor, residual = flujo_maximo_unitario(grafo, origen, destino)
    if valor == 0:
        return []
    alcanzables = alcanzables_en_residual(residual, origen)
    return [(u, v) for u, v in grafo.arcos_activos() if u in alcanzables and v not in alcanzables]
