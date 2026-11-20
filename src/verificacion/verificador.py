"""Comprobaciones de la sección 5 de la pauta.

Verifican los resultados de forma independiente: no deben usar los
algoritmos que verifican. Por eso este módulo NO importa nada de
``src.algoritmos``; la alcanzabilidad se revisa con una búsqueda propia
(``_es_alcanzable``) que solo usa ``grafo.sucesores`` (arcos activos).
"""

from typing import List, Tuple
from src.modelo.grafo import GrafoDirigido


def _es_alcanzable(grafo: GrafoDirigido, origen: str, destino: str) -> bool:
    """Indica si existe un camino dirigido de origen a destino por arcos activos.

    Búsqueda en profundidad iterativa (con pila), independiente de los
    algoritmos de ``src.algoritmos``. Solo recorre arcos no bloqueados,
    porque usa ``grafo.sucesores``.

    Parámetros:
        grafo: laberinto sobre el que se busca (no se modifica).
        origen: vértice de partida.
        destino: vértice que se quiere alcanzar.

    Retorna:
        True si destino es alcanzable desde origen (o si origen == destino
        y el vértice existe); False si no, o si alguno de los vértices no
        existe en el grafo.
    """
    if origen not in grafo.vertices or destino not in grafo.vertices:
        return False
    visitados = {origen}
    pila = [origen]
    while pila:
        actual = pila.pop()
        if actual == destino:
            return True
        for vecino in grafo.sucesores(actual):
            if vecino not in visitados:
                visitados.add(vecino)
                pila.append(vecino)
    return False


def verificar_camino_valido(grafo: GrafoDirigido, camino: List[str], origen: str, destino: str) -> bool:
    """Comprueba que un camino sea válido en el grafo.

    El camino debe empezar en origen, terminar en destino y cada par de
    vértices consecutivos debe ser un arco activo (existente y no bloqueado).
    Un camino de un solo vértice solo es válido si origen == destino y ese
    vértice existe en el grafo.

    Parámetros:
        grafo: laberinto sobre el que se verifica.
        camino: lista de vértices a revisar.
        origen: vértice de entrada s.
        destino: vértice de salida t.

    Retorna:
        True si el camino es válido; False en caso contrario (incluye
        camino None o vacío).
    """
    if not camino:
        return False
    if camino[0] != origen or camino[-1] != destino:
        return False
    if len(camino) == 1:
        return origen == destino and origen in grafo.vertices
    for u, v in zip(camino, camino[1:]):
        if not grafo.existe_arco(u, v) or grafo.esta_bloqueado(u, v):
            return False
    return True


def verificar_sin_arcos_compartidos(caminos: List[List[str]]) -> bool:
    """Comprueba que ningún arco aparezca en más de un camino.

    Los vértices sí pueden repetirse entre caminos. Un arco repetido dentro
    de un mismo camino también cuenta como compartido. Una lista vacía de
    caminos se considera válida.

    Parámetros:
        caminos: lista de caminos (listas de vértices).

    Retorna:
        True si los caminos no comparten arcos; False en caso contrario.
    """
    vistos = set()
    for camino in caminos:
        for arco in zip(camino, camino[1:]):
            if arco in vistos:
                return False
            vistos.add(arco)
    return True


def verificar_corte_desconecta(grafo: GrafoDirigido, corte: List[Tuple[str, str]], origen: str, destino: str) -> bool:
    """Comprueba que el corte desconecte el origen del destino.

    Bloquea los arcos del corte en una COPIA del grafo y revisa que ya no
    exista camino de origen a destino. Acepta arcos como tuplas o listas
    de dos elementos (por ejemplo, leídos desde JSON).

    Parámetros:
        grafo: laberinto original (no se modifica).
        corte: lista de arcos (u, v) del corte.
        origen: vértice de entrada s.
        destino: vértice de salida t.

    Retorna:
        True si el corte desconecta s de t; False si no lo hace o si algún
        arco del corte no existe en el grafo.
    """
    copia = grafo.copiar()
    for u, v in corte:
        if not copia.existe_arco(u, v):
            return False
        copia.bloquear_arco(u, v)
    return not _es_alcanzable(copia, origen, destino)


def verificar_igualdad_menger(cantidad_caminos: int, corte: List[Tuple[str, str]]) -> bool:
    """Comprueba Menger: caminos sin arcos compartidos = tamaño del corte.

    Parámetros:
        cantidad_caminos: máximo número de caminos sin arcos compartidos.
        corte: lista de arcos del corte mínimo.

    Retorna:
        True si cantidad_caminos == len(corte); False en caso contrario.
    """
    return cantidad_caminos == len(corte)


def verificar_todo(grafo: GrafoDirigido, resultado) -> dict:
    """Ejecuta todas las comprobaciones sobre los resultados de una configuración.

    Usa ``grafo.entrada`` y ``grafo.salida`` como s y t, y los campos
    ``camino_minimo``, ``caminos_disjuntos``, ``cantidad_caminos_disjuntos``
    y ``corte_minimo`` del resultado. Si ``camino_minimo`` es None, se
    considera válido solo si de verdad t no es alcanzable desde s.

    Parámetros:
        grafo: laberinto sobre el que se calcularon los resultados.
        resultado: ResultadoConfiguracion a verificar.

    Retorna:
        Diccionario {nombre_verificacion: bool} con las claves:
        "camino_minimo_valido", "caminos_disjuntos_validos",
        "sin_arcos_compartidos", "cantidad_coincide", "corte_desconecta",
        "igualdad_menger".
    """
    s, t = grafo.entrada, grafo.salida
    caminos = resultado.caminos_disjuntos
    corte = resultado.corte_minimo

    if resultado.camino_minimo is None:
        camino_minimo_valido = not _es_alcanzable(grafo, s, t)
    else:
        camino_minimo_valido = verificar_camino_valido(grafo, resultado.camino_minimo, s, t)

    return {
        "camino_minimo_valido": camino_minimo_valido,
        "caminos_disjuntos_validos": all(verificar_camino_valido(grafo, c, s, t) for c in caminos),
        "sin_arcos_compartidos": verificar_sin_arcos_compartidos(caminos),
        "cantidad_coincide": resultado.cantidad_caminos_disjuntos == len(caminos),
        "corte_desconecta": verificar_corte_desconecta(grafo, corte, s, t),
        "igualdad_menger": verificar_igualdad_menger(resultado.cantidad_caminos_disjuntos, corte),
    }
