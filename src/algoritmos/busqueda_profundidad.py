"""DFS iterativo: encuentra un camino válido, pero no garantiza el más corto."""
from typing import List, Optional
from src.modelo.grafo import GrafoDirigido


def busqueda_en_profundidad(grafo: GrafoDirigido, origen: str, destino: str) -> Optional[List[str]]:
    """Busca un camino dirigido activo utilizando DFS iterativo con una pila.

    Explora una rama antes de retroceder; por esa razón encuentra una
    ruta válida cuando existe, pero NO garantiza que sea la más corta.
    El recorrido de vértices es O(|V| + |E|); copiar las rutas parciales
    puede añadir trabajo proporcional a su longitud.

    Parámetros:
        grafo: grafo dirigido cuyos sucesores excluyen arcos bloqueados.
        origen: vértice de partida existente en el grafo.
        destino: vértice de llegada existente en el grafo.

    Retorna:
        Lista con los vértices del primer camino encontrado desde origen
        hasta destino, o None si el destino no es alcanzable. Si ambos
        extremos coinciden, retorna una lista con ese único vértice.

    Errores:
        ValueError si origen o destino no existe.
    """
    grafo._exigir_vertice(origen)
    grafo._exigir_vertice(destino)
    pila = [(origen, [origen])]
    visitados = set()
    while pila:
        actual, camino = pila.pop()
        if actual in visitados:
            continue
        visitados.add(actual)
        if actual == destino:
            return camino
        # La pila LIFO procesa primero el último sucesor insertado.
        for vecino in grafo.sucesores(actual):
            if vecino not in visitados:
                pila.append((vecino, camino + [vecino]))
    return None


def existe_camino(grafo: GrafoDirigido, origen: str, destino: str) -> bool:
    """Comprueba la alcanzabilidad de destino mediante una búsqueda DFS.

    No busca una distancia mínima: reutiliza la búsqueda en profundidad
    para determinar únicamente si existe una ruta con arcos activos.

    Parámetros:
        grafo: grafo dirigido que contiene los vértices y arcos activos.
        origen: vértice existente desde donde comienza el recorrido.
        destino: vértice existente cuya alcanzabilidad se comprueba.

    Retorna:
        True si hay al menos un camino dirigido de origen a destino;
        False si no existe ninguno.

    Errores:
        ValueError si origen o destino no existe.
    """
    return busqueda_en_profundidad(grafo, origen, destino) is not None


# Ejemplo donde DFS no garantiza camino minimo:
# V = {s, a, b, c, t}; E insertados en el orden:
# s->t, s->a, a->b, b->c, c->t.
# DFS usa pila LIFO y encuentra s->a->b->c->t (4 arcos),
# mientras BFS encuentra s->t (1 arco).
