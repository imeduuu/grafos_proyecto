"""DFS iterativo: encuentra un camino válido, pero no garantiza el más corto."""
from typing import List, Optional
from src.modelo.grafo import GrafoDirigido


def busqueda_en_profundidad(grafo: GrafoDirigido, origen: str, destino: str) -> Optional[List[str]]:
    """Busca un camino dirigido activo con pila; None si no hay conexión."""
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
    """Indica si el destino es alcanzable mediante arcos activos."""
    return busqueda_en_profundidad(grafo, origen, destino) is not None


# Ejemplo donde DFS no garantiza camino mínimo:
# V = {s, a, b, c, t}; E insertados en este orden:
# s->t, s->a, a->b, b->c, c->t.
# DFS usa pila LIFO y encuentra s->a->b->c->t (4 arcos),
# mientras BFS encuentra s->t (1 arco).
