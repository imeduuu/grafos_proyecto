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
        """Agrega un vértice. Si ya existe, no hace nada."""
        if vertice not in self.vertices:
            self.vertices.add(vertice)
            self.adyacencia[vertice] = []

    def agregar_arco(self, origen: str, destino: str) -> None:
        """Agrega el pasillo dirigido origen -> destino.

        Lanza ValueError si:
        - es un lazo (origen == destino),
        - origen o destino no existen como vértices,
        - el arco origen -> destino ya existe (arco repetido),
        - ya existe el arco recíproco destino -> origen.
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

        Lanza ValueError si alguno de los vértices no existe o si son iguales.
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

        Bloquear un arco ya bloqueado no tiene efecto.
        Lanza ValueError si el arco no existe.
        """
        self._exigir_arco(origen, destino)
        self.bloqueados.add((origen, destino))

    def restablecer_arco(self, origen: str, destino: str) -> None:
        """Quita el bloqueo del pasillo origen -> destino.

        Restablecer un arco que no estaba bloqueado no tiene efecto.
        Lanza ValueError si el arco no existe.
        """
        self._exigir_arco(origen, destino)
        self.bloqueados.discard((origen, destino))

    def esta_bloqueado(self, origen: str, destino: str) -> bool:
        """Indica si el arco origen -> destino está bloqueado."""
        return (origen, destino) in self.bloqueados

    # ------------------------------------------------------------------
    # Consultas
    # ------------------------------------------------------------------

    def sucesores(self, vertice: str) -> List[str]:
        """Vecinos alcanzables desde ``vertice`` por arcos NO bloqueados.

        Respeta el orden de inserción de los arcos para que los algoritmos
        entreguen resultados reproducibles. Retorna una lista nueva, que se
        puede modificar sin afectar al grafo.
        Lanza ValueError si el vértice no existe.
        """
        self._exigir_vertice(vertice)
        return [v for v in self.adyacencia[vertice] if (vertice, v) not in self.bloqueados]

    def arcos(self) -> List[Arco]:
        """Todos los arcos (incluidos los bloqueados) como lista de tuplas (u, v).

        Orden: por vértice de origen según su orden de inserción y, dentro de
        cada origen, según el orden en que se agregaron sus arcos.
        """
        return [(u, v) for u, destinos in self.adyacencia.items() for v in destinos]

    def arcos_activos(self) -> List[Arco]:
        """Arcos no bloqueados, en el mismo orden que ``arcos()``."""
        return [arco for arco in self.arcos() if arco not in self.bloqueados]

    def existe_arco(self, origen: str, destino: str) -> bool:
        """Indica si el arco origen -> destino existe (esté bloqueado o no)."""
        return destino in self.adyacencia.get(origen, [])

    def cantidad_vertices(self) -> int:
        """Retorna |V|."""
        return len(self.vertices)

    def cantidad_arcos(self) -> int:
        """Retorna |E|, contando también los arcos bloqueados."""
        return sum(len(destinos) for destinos in self.adyacencia.values())

    def copiar(self) -> "GrafoDirigido":
        """Retorna una copia profunda e independiente del grafo.

        Sirve para comparar configuraciones: modificar la copia (agregar,
        bloquear o restablecer arcos) no afecta al original.
        """
        return copy.deepcopy(self)

    # ------------------------------------------------------------------
    # Auxiliares internos
    # ------------------------------------------------------------------

    def _exigir_vertice(self, vertice: str) -> None:
        """Lanza ValueError si el vértice no existe."""
        if vertice not in self.vertices:
            raise ValueError(f"El vértice '{vertice}' no existe en el grafo.")

    def _exigir_arco(self, origen: str, destino: str) -> None:
        """Lanza ValueError si el arco origen -> destino no existe."""
        if not self.existe_arco(origen, destino):
            raise ValueError(f"El arco ({origen}, {destino}) no existe en el grafo.")
