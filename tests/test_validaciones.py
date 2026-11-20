"""Pruebas de las restricciones de la configuración inicial (tarea 3).

``maximo_caminos_disjuntos`` se reemplaza con monkeypatch para que estas
pruebas no dependan de la implementación de flujo máximo.
"""

import pytest

from src.algoritmos import flujo_maximo
from src.modelo.grafo import GrafoDirigido
from src.modelo.validaciones import (
    tiene_arcos_reciprocos,
    tiene_lazos,
    validar_configuracion_inicial,
    vertices_aislados,
)

ARCOS_VALIDOS = [
    ("s", "a"), ("s", "b"),
    ("a", "c"), ("b", "d"),
    ("c", "e"), ("d", "f"),
    ("e", "t"), ("f", "t"),
    ("a", "g"), ("b", "g"),
    ("g", "h"), ("h", "t"),
    ("c", "d"), ("e", "f"),
]


def construir_red_valida() -> GrafoDirigido:
    """Red de 10 vértices y 14 arcos, sin lazos, recíprocos ni aislados."""
    grafo = GrafoDirigido()
    for vertice in ["s", "a", "b", "c", "d", "e", "f", "g", "h", "t"]:
        grafo.agregar_vertice(vertice)
    for origen, destino in ARCOS_VALIDOS:
        grafo.agregar_arco(origen, destino)
    grafo.definir_entrada_salida("s", "t")
    return grafo


def simular_caminos(monkeypatch, cantidad):
    """Reemplaza maximo_caminos_disjuntos y registra las llamadas recibidas."""
    llamadas = []

    def falso(grafo, origen, destino):
        llamadas.append((origen, destino))
        return cantidad, [["s", "t"]] * cantidad

    monkeypatch.setattr(flujo_maximo, "maximo_caminos_disjuntos", falso)
    return llamadas


# ----------------------------------------------------------------------
# tiene_lazos / tiene_arcos_reciprocos / vertices_aislados
# ----------------------------------------------------------------------

def test_grafo_normal_sin_lazos_ni_reciprocos():
    grafo = construir_red_valida()
    assert tiene_lazos(grafo) is False
    assert tiene_arcos_reciprocos(grafo) is False


def test_detecta_lazo_insertado_directamente():
    grafo = construir_red_valida()
    grafo.adyacencia["a"].append("a")  # la API lo impediría
    assert tiene_lazos(grafo) is True
    assert tiene_arcos_reciprocos(grafo) is False


def test_detecta_reciproco_insertado_directamente():
    grafo = construir_red_valida()
    grafo.adyacencia["a"].append("s")  # (s, a) ya existe
    assert tiene_arcos_reciprocos(grafo) is True


def test_vertices_aislados_respeta_orden_y_cuenta_bloqueados():
    grafo = construir_red_valida()
    grafo.agregar_vertice("z")
    grafo.agregar_vertice("y")
    grafo.bloquear_arco("g", "h")
    assert vertices_aislados(grafo) == ["z", "y"]


# ----------------------------------------------------------------------
# validar_configuracion_inicial
# ----------------------------------------------------------------------

def test_figura1_incumple_cantidades(grafo_figura1, monkeypatch):
    simular_caminos(monkeypatch, 2)
    errores = validar_configuracion_inicial(grafo_figura1)
    assert len(errores) == 2
    assert "vértices" in errores[0] and "(tiene 9)" in errores[0]
    assert "arcos" in errores[1] and "(tiene 12)" in errores[1]


def test_red_valida_con_dos_caminos(monkeypatch):
    llamadas = simular_caminos(monkeypatch, 2)
    assert validar_configuracion_inicial(construir_red_valida()) == []
    assert llamadas == [("s", "t")]


def test_red_valida_con_un_solo_camino(monkeypatch):
    simular_caminos(monkeypatch, 1)
    errores = validar_configuracion_inicial(construir_red_valida())
    assert len(errores) == 1
    assert "sin arcos compartidos" in errores[0]
    assert "(hay 1)" in errores[0]


def test_vertice_aislado_aparece_en_mensaje(monkeypatch):
    simular_caminos(monkeypatch, 2)
    grafo = construir_red_valida()
    grafo.agregar_vertice("z")  # 11 vértices: sigue en rango
    errores = validar_configuracion_inicial(grafo)
    assert len(errores) == 1
    assert "aislados" in errores[0] and "z" in errores[0]


def test_entrada_igual_a_salida_no_llama_flujo(monkeypatch):
    llamadas = simular_caminos(monkeypatch, 2)
    grafo = construir_red_valida()
    grafo.salida = "s"  # definir_entrada_salida lo impediría
    errores = validar_configuracion_inicial(grafo)
    assert len(errores) == 1
    assert "distintas" in errores[0]
    assert llamadas == []


@pytest.mark.parametrize("entrada, salida", [(None, "t"), ("s", None), ("x", "t")])
def test_entrada_o_salida_invalida_no_llama_flujo(monkeypatch, entrada, salida):
    llamadas = simular_caminos(monkeypatch, 2)
    grafo = construir_red_valida()
    grafo.entrada = entrada
    grafo.salida = salida
    errores = validar_configuracion_inicial(grafo)
    assert len(errores) == 1
    assert "entrada" in errores[0]
    assert llamadas == []


def test_no_lanza_excepcion_con_multiples_errores(monkeypatch):
    simular_caminos(monkeypatch, 0)
    grafo = GrafoDirigido()
    errores = validar_configuracion_inicial(grafo)
    assert len(errores) == 3  # vértices, arcos, entrada/salida
