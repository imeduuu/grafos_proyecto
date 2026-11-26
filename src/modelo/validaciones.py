"""Restricciones que debe cumplir la configuración inicial del laberinto.

La red inicial del grupo debe tener:
- entre 10 y 12 vértices y entre 14 y 20 arcos (contando los bloqueados),
- una entrada s y una salida t definidas, existentes y distintas,
- ningún lazo, ningún par de arcos recíprocos y ningún vértice aislado,
- al menos 2 caminos s -> t que no comparten arcos (sobre los arcos activos).

Los arcos repetidos no se revisan aquí porque la lista de adyacencia de
``GrafoDirigido`` los rechaza al agregarlos.
"""

from typing import List

from src.modelo.grafo import GrafoDirigido

MIN_VERTICES = 10
MAX_VERTICES = 12
MIN_ARCOS = 14
MAX_ARCOS = 20
MIN_CAMINOS_DISJUNTOS = 2


def tiene_lazos(grafo: GrafoDirigido) -> bool:
    """Indica si existe algún arco (v, v) en el grafo, incluidos los bloqueados.

    Con la API de ``GrafoDirigido`` esto nunca ocurre, porque ``agregar_arco``
    rechaza los lazos. Se deja como comprobación explícita de la restricción
    para el informe y por si la lista de adyacencia se modifica directamente.

    Parámetros:
        grafo: laberinto cuyos arcos se revisarán.

    Retorna:
        True si hay al menos un lazo; False en caso contrario.
    """
    return any(origen == destino for origen, destino in grafo.arcos())


def tiene_arcos_reciprocos(grafo: GrafoDirigido) -> bool:
    """Indica si existen a la vez los arcos (u, v) y (v, u), incluidos los bloqueados.

    Con la API de ``GrafoDirigido`` esto nunca ocurre, porque ``agregar_arco``
    rechaza el arco recíproco de uno existente. Se deja como comprobación
    explícita de la restricción para el informe y por si la lista de
    adyacencia se modifica directamente. Los lazos no cuentan como recíprocos.

    Parámetros:
        grafo: laberinto cuyos arcos se revisarán.

    Retorna:
        True si existe al menos un par de arcos recíprocos; False si no.
    """
    arcos = set(grafo.arcos())
    return any(origen != destino and (destino, origen) in arcos for origen, destino in arcos)


def vertices_aislados(grafo: GrafoDirigido) -> List[str]:
    """Vértices que no son origen ni destino de ningún arco.

    Se consideran TODOS los arcos, incluidos los bloqueados: un pasillo
    bloqueado sigue existiendo en el laberinto. La lista respeta el orden de
    inserción de los vértices (``grafo.adyacencia``), para que el resultado
    sea reproducible.

    Parámetros:
        grafo: laberinto cuyos vértices se revisarán.

    Retorna:
        Lista ordenada de vértices que no participan en ningún arco.
    """
    con_arcos = set()
    for origen, destino in grafo.arcos():
        con_arcos.add(origen)
        con_arcos.add(destino)
    return [vertice for vertice in grafo.adyacencia if vertice not in con_arcos]


def validar_configuracion_inicial(grafo: GrafoDirigido) -> List[str]:
    """Revisa todas las restricciones de la red inicial y retorna los errores.

    No lanza excepciones por incumplimientos: acumula un mensaje por cada
    restricción que falla. Una lista vacía significa que la red es válida.

    Orden de revisión:
    1. 10 <= |V| <= 12.
    2. 14 <= |E| <= 20 (contando también los arcos bloqueados).
    3. Entrada y salida definidas, existentes y distintas.
    4. Sin lazos.
    5. Sin arcos recíprocos.
    6. Sin vértices aislados.
    7. Al menos 2 caminos s -> t sin arcos compartidos, calculados sobre los
       arcos activos con ``maximo_caminos_disjuntos``. Solo se revisa si la
       entrada y la salida son válidas.

    Parámetros:
        grafo: configuración inicial del laberinto que se validará.

    Retorna:
        Lista de mensajes descriptivos de los incumplimientos; lista vacía
        si se satisfacen todas las restricciones.
    """
    errores: List[str] = []

    cantidad_vertices = grafo.cantidad_vertices()
    if not MIN_VERTICES <= cantidad_vertices <= MAX_VERTICES:
        errores.append(
            f"La red debe tener entre {MIN_VERTICES} y {MAX_VERTICES} vértices "
            f"(tiene {cantidad_vertices})."
        )

    cantidad_arcos = grafo.cantidad_arcos()
    if not MIN_ARCOS <= cantidad_arcos <= MAX_ARCOS:
        errores.append(
            f"La red debe tener entre {MIN_ARCOS} y {MAX_ARCOS} arcos "
            f"(tiene {cantidad_arcos})."
        )

    entrada_salida_validas = True
    if grafo.entrada is None or grafo.salida is None:
        errores.append("La entrada y la salida deben estar definidas.")
        entrada_salida_validas = False
    else:
        for nombre, vertice in (("entrada", grafo.entrada), ("salida", grafo.salida)):
            if vertice not in grafo.vertices:
                errores.append(f"La {nombre} '{vertice}' no existe en el grafo.")
                entrada_salida_validas = False
        if grafo.entrada == grafo.salida:
            errores.append(
                f"La entrada y la salida deben ser distintas (ambas son '{grafo.entrada}')."
            )
            entrada_salida_validas = False

    if tiene_lazos(grafo):
        errores.append("La red no debe tener lazos (arcos de un vértice a sí mismo).")

    if tiene_arcos_reciprocos(grafo):
        errores.append("La red no debe tener arcos recíprocos (u, v) y (v, u).")

    aislados = vertices_aislados(grafo)
    if aislados:
        errores.append(f"La red no debe tener vértices aislados: {', '.join(aislados)}.")

    if entrada_salida_validas:
        # Importación local: flujo_maximo depende de este paquete y así se
        # evita una importación circular; además permite reemplazarla en pruebas.
        from src.algoritmos import flujo_maximo

        cantidad_caminos, _ = flujo_maximo.maximo_caminos_disjuntos(
            grafo, grafo.entrada, grafo.salida
        )
        if cantidad_caminos < MIN_CAMINOS_DISJUNTOS:
            errores.append(
                f"Debe haber al menos {MIN_CAMINOS_DISJUNTOS} caminos de "
                f"'{grafo.entrada}' a '{grafo.salida}' sin arcos compartidos "
                f"usando los arcos activos (hay {cantidad_caminos})."
            )

    return errores
