"""Representación y operaciones de un laberinto como grafo dirigido."""

import copy
from typing import Dict, List, Optional, Set, Tuple

Arco = Tuple[str, str]

class GrafoDirigido:
    """Laberinto de pasillos de sentido único modelado como grafo dirigido G = (V, E).

    Se representa con una lista de adyacencia y un conjunto de arcos bloqueados.
    Un arco bloqueado sigue existiendo en el grafo (aparece en ``arcos()`` y en
    ``adyacencia``), pero no se puede recorrer: ``sucesores()`` y
    ``arcos_activos()`` lo omiten.
    """

    def __init__(self) -> None:
        """Inicializa un grafo sin vértices, arcos ni extremos definidos.

        Parámetros:
            Ninguno.

        Retorna:
            None. Inicializa las colecciones y atributos del grafo.
        """
        self.vertices: Set[str] = set()
        self.adyacencia: Dict[str, List[str]] = {}
        self.bloqueados: Set[Arco] = set()
        self.entrada: Optional[str] = None
        self.salida: Optional[str] = None
        self.posiciones: Dict[str, Tuple[float, float]] = {}

    # ------------------------------------------------------------------
    # Construcción
    # ------------------------------------------------------------------

    def agregar_vertice(self, vertice: str) -> None:
        """Agrega un vértice nuevo, sin alterar el grafo si ya estaba registrado.

        Parámetros:
            vertice: identificador del vértice que se incorporará.

        Retorna:
            None.
        """
        if vertice not in self.vertices:
            self.vertices.add(vertice)
            self.adyacencia[vertice] = []

    def agregar_arco(self, origen: str, destino: str) -> None:
        """Agrega el pasillo dirigido origen -> destino.

        Parámetros:
            origen: vértice desde el que parte el pasillo.
            destino: vértice al que llega el pasillo.

        Retorna:
            None.

        Errores:
            ValueError si el arco es un lazo, si algún extremo no existe,
            si ya existe el mismo arco o si existe el arco recíproco.
        """
        if origen == destino:
            raise ValueError(f"No se permiten lazos: el arco ({origen}, {destino}) empieza y termina en el mismo vértice.")
        self._exigir_vertice(origen)
        self._exigir_vertice(destino)
        if self.existe_arco(origen, destino):
            raise ValueError(f"El arco ({origen}, {destino}) ya existe: no se permiten arcos repetidos.")
        if self.existe_arco(destino, origen):
            raise ValueError(
                f"No se puede agregar ({origen}, {destino}): ya existe el arco recíproco ({destino}, {origen})."
            )
        self.adyacencia[origen].append(destino)

    def definir_entrada_salida(self, entrada: str, salida: str) -> None:
        """Define la entrada s y la salida t del laberinto.

        Parámetros:
            entrada: vértice existente que será el origen de las rutas.
            salida: vértice existente y distinto que será el destino.

        Retorna:
            None.

        Errores:
            ValueError si algún vértice no existe o si ambos extremos son iguales.
        """
        self._exigir_vertice(entrada)
        self._exigir_vertice(salida)
        if entrada == salida:
            raise ValueError(f"La entrada y la salida deben ser distintas (se recibió '{entrada}' para ambas).")
        self.entrada = entrada
        self.salida = salida

    # ------------------------------------------------------------------
    # Bloqueos
    # ------------------------------------------------------------------

    def bloquear_arco(self, origen: str, destino: str) -> None:
        """Bloquea el pasillo origen -> destino sin borrarlo.

        Parámetros:
            origen: vértice de salida del arco que se bloqueará.
            destino: vértice de llegada del arco que se bloqueará.

        Retorna:
            None.

        Errores:
            ValueError si el arco no existe. Bloquear uno ya bloqueado no
            produce cambios.
        """
        self._exigir_arco(origen, destino)
        self.bloqueados.add((origen, destino))

    def restablecer_arco(self, origen: str, destino: str) -> None:
        """Quita el bloqueo del pasillo origen -> destino.

        Parámetros:
            origen: vértice de salida del arco que se restablecerá.
            destino: vértice de llegada del arco que se restablecerá.

        Retorna:
            None.

        Errores:
            ValueError si el arco no existe. Restablecer uno activo no
            produce cambios.
        """
        self._exigir_arco(origen, destino)
        self.bloqueados.discard((origen, destino))

    def esta_bloqueado(self, origen: str, destino: str) -> bool:
        """Indica si el arco dirigido está actualmente bloqueado.

        Parámetros:
            origen: vértice desde el que parte el arco.
            destino: vértice al que llega el arco.

        Retorna:
            True si el arco está bloqueado; False en caso contrario.
        """
        return (origen, destino) in self.bloqueados

    # ------------------------------------------------------------------
    # Consultas
    # ------------------------------------------------------------------

    def sucesores(self, vertice: str) -> List[str]:
        """Obtiene los vecinos alcanzables por arcos no bloqueados.

        Respeta el orden de inserción de los arcos para que los algoritmos
        entreguen resultados reproducibles.

        Parámetros:
            vertice: vértice cuyos sucesores se consultan.

        Retorna:
            Lista nueva de vértices destino de sus arcos activos.

        Errores:
            ValueError si el vértice no existe.
        """
        self._exigir_vertice(vertice)
        return [v for v in self.adyacencia[vertice] if (vertice, v) not in self.bloqueados]

    def arcos(self) -> List[Arco]:
        """Todos los arcos (incluidos los bloqueados) como lista de tuplas (u, v).

        Orden: por vértice de origen según su orden de inserción y, dentro de
        cada origen, según el orden en que se agregaron sus arcos.

        Parámetros:
            Ninguno.

        Retorna:
            Lista de todos los arcos dirigidos del grafo.
        """
        return [(u, v) for u, destinos in self.adyacencia.items() for v in destinos]

    def arcos_activos(self) -> List[Arco]:
        """Obtiene los arcos no bloqueados en el orden de ``arcos()``.

        Parámetros:
            Ninguno.

        Retorna:
            Lista de arcos dirigidos que se pueden recorrer actualmente.
        """
        return [arco for arco in self.arcos() if arco not in self.bloqueados]

    def existe_arco(self, origen: str, destino: str) -> bool:
        """Comprueba si existe el arco, esté activo o bloqueado.

        Parámetros:
            origen: vértice desde el que parte el arco.
            destino: vértice al que llega el arco.

        Retorna:
            True si el arco está registrado; False si no existe.
        """
        return destino in self.adyacencia.get(origen, [])

    def cantidad_vertices(self) -> int:
        """Cuenta los vértices registrados en el grafo.

        Parámetros:
            Ninguno.

        Retorna:
            Cantidad de vértices, |V|.
        """
        return len(self.vertices)

    def cantidad_arcos(self) -> int:
        """Cuenta todos los arcos, incluidos los bloqueados.

        Parámetros:
            Ninguno.

        Retorna:
            Cantidad total de arcos, |E|.
        """
        return sum(len(destinos) for destinos in self.adyacencia.values())

    def copiar(self) -> "GrafoDirigido":
        """Retorna una copia profunda e independiente del grafo.

        Sirve para comparar configuraciones: modificar la copia (agregar,
        bloquear o restablecer arcos) no afecta al original.

        Parámetros:
            Ninguno.

        Retorna:
            Nuevo GrafoDirigido con los mismos vértices, arcos y atributos.
        """
        return copy.deepcopy(self)

    # ------------------------------------------------------------------
    # Auxiliares internos
    # ------------------------------------------------------------------

    def _exigir_vertice(self, vertice: str) -> None:
        """Valida que un vértice esté registrado en el grafo.

        Parámetros:
            vertice: identificador que se validará.

        Retorna:
            None si existe.

        Errores:
            ValueError si el vértice no pertenece al grafo.
        """
        if vertice not in self.vertices:
            raise ValueError(f"El vértice '{vertice}' no existe en el grafo.")

    def _exigir_arco(self, origen: str, destino: str) -> None:
        """Valida que exista el arco dirigido indicado.

        Parámetros:
            origen: vértice desde el que parte el arco.
            destino: vértice al que llega el arco.

        Retorna:
            None si el arco existe.

        Errores:
            ValueError si el arco no está registrado.
        """
        if not self.existe_arco(origen, destino):
            raise ValueError(f"El arco ({origen}, {destino}) no existe en el grafo.")
