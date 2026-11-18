from typing import Dict, List, Optional, Set, Tuple

Arco = Tuple[str, str]

class GrafoDirigido:

    def __init__(self) -> None:
        self.vertices: Set[str] = set()
        self.adyacencia: Dict[str, List[str]] = {}
        self.bloqueados: Set[Arco] = set()
        self.entrada: Optional[str] = None
        self.salida: Optional[str] = None
        self.posiciones: Dict[str, Tuple[float, float]] = {}




    def agregar_vertice(self, vertice: str) -> None:
        raise NotImplementedError("TODO: implementar agregar_vertice")

    def agregar_arco(self, origen: str, destino: str) -> None:
        raise NotImplementedError("TODO: implementar agregar_arco")

    def bloquear_arco(self, origen: str, destino: str) -> None:
        raise NotImplementedError("TODO: implementar bloquear_arco")

    def restablecer_arco(self, origen: str, destino: str) -> None:
        raise NotImplementedError("TODO: implementar restablecer_arco")

    def esta_bloqueado(self, origen: str, destino: str) -> bool:
        raise NotImplementedError("TODO: implementar esta_bloqueado")

    def definir_entrada_salida(self, entrada: str, salida: str) -> None:
        raise NotImplementedError("TODO: implementar definir_entrada_salida")

    def sucesores(self, vertice: str) -> List[str]:
        raise NotImplementedError("TODO: implementar sucesores")

    def arcos(self) -> List[Arco]:
        raise NotImplementedError("TODO: implementar arcos")

    def arcos_activos(self) -> List[Arco]:
        raise NotImplementedError("TODO: implementar arcos_activos")

    def existe_arco(self, origen: str, destino: str) -> bool:
        raise NotImplementedError("TODO: implementar existe_arco")

    def cantidad_vertices(self) -> int:
        raise NotImplementedError("TODO: implementar cantidad_vertices")

    def cantidad_arcos(self) -> int:
        raise NotImplementedError("TODO: implementar cantidad_arcos")

    def copiar(self) -> "GrafoDirigido":
        raise NotImplementedError("TODO: implementar copiar")
