"""Pruebas del verificador independiente (tarea 5).

Los caminos y cortes se escriben a mano: no se usan los algoritmos de
``src.algoritmos`` para no verificar un algoritmo consigo mismo.
"""

import os

import pytest

from src.modelo.cargador import cargar_grafo_json
from src.simulacion.configuraciones import ResultadoConfiguracion
from src.verificacion.verificador import (
    _es_alcanzable,
    verificar_camino_valido,
    verificar_corte_desconecta,
    verificar_igualdad_menger,
    verificar_sin_arcos_compartidos,
    verificar_todo,
)

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAMINO_1 = ["s", "A", "B", "E", "t"]
CAMINO_2 = ["s", "C", "F", "G", "t"]
CORTE_FIGURA1 = [("E", "t"), ("G", "t")]


@pytest.fixture
def grafo_inicial():
    return cargar_grafo_json(os.path.join(RAIZ, "datos", "grafo_inicial.json"))


def _resultado_correcto_figura1():
    return ResultadoConfiguracion(
        nombre="Figura 1",
        existe_camino=True,
        camino_minimo=["s", "A", "D", "G", "t"],
        longitud_minima=4,
        cantidad_caminos_disjuntos=2,
        caminos_disjuntos=[CAMINO_1, CAMINO_2],
        corte_minimo=list(CORTE_FIGURA1),
    )


# ----------------------------------------------------------------------
# _es_alcanzable
# ----------------------------------------------------------------------

def test_es_alcanzable_basico(grafo_figura1):
    assert _es_alcanzable(grafo_figura1, "s", "t")
    assert not _es_alcanzable(grafo_figura1, "t", "s")
    assert _es_alcanzable(grafo_figura1, "s", "s")
    assert not _es_alcanzable(grafo_figura1, "s", "Z")


def test_es_alcanzable_respeta_bloqueos(grafo_figura1):
    grafo_figura1.bloquear_arco("E", "t")
    grafo_figura1.bloquear_arco("G", "t")
    assert not _es_alcanzable(grafo_figura1, "s", "t")


# ----------------------------------------------------------------------
# verificar_camino_valido
# ----------------------------------------------------------------------

def test_camino_valido_figura1(grafo_figura1):
    assert verificar_camino_valido(grafo_figura1, CAMINO_1, "s", "t")


def test_camino_con_arco_inexistente_es_invalido(grafo_figura1):
    assert not verificar_camino_valido(grafo_figura1, ["s", "B", "E", "t"], "s", "t")


def test_camino_en_sentido_contrario_es_invalido(grafo_figura1):
    # B -> A no existe (solo A -> B)
    assert not verificar_camino_valido(grafo_figura1, ["s", "A", "B", "A", "D", "G", "t"], "s", "t")


def test_camino_por_arco_bloqueado_es_invalido(grafo_figura1):
    grafo_figura1.bloquear_arco("B", "E")
    assert not verificar_camino_valido(grafo_figura1, CAMINO_1, "s", "t")


def test_camino_extremos_incorrectos(grafo_figura1):
    assert not verificar_camino_valido(grafo_figura1, ["A", "B", "E", "t"], "s", "t")
    assert not verificar_camino_valido(grafo_figura1, ["s", "A", "B", "E"], "s", "t")


def test_camino_vacio_o_none(grafo_figura1):
    assert not verificar_camino_valido(grafo_figura1, [], "s", "t")
    assert not verificar_camino_valido(grafo_figura1, None, "s", "t")


def test_camino_de_un_vertice(grafo_figura1):
    assert verificar_camino_valido(grafo_figura1, ["s"], "s", "s")
    assert not verificar_camino_valido(grafo_figura1, ["s"], "s", "t")


# ----------------------------------------------------------------------
# verificar_sin_arcos_compartidos
# ----------------------------------------------------------------------

def test_caminos_sin_arcos_compartidos():
    assert verificar_sin_arcos_compartidos([CAMINO_1, CAMINO_2])


def test_caminos_que_comparten_arco():
    # Ambos usan el arco A -> B
    assert not verificar_sin_arcos_compartidos([CAMINO_1, ["s", "A", "B", "E", "t"]])
    assert not verificar_sin_arcos_compartidos([["s", "A", "B", "E", "t"], ["s", "C", "D", "A", "B", "E", "t"]])


def test_arco_repetido_en_un_mismo_camino():
    assert not verificar_sin_arcos_compartidos([["s", "A", "B", "A", "B", "t"]])


def test_lista_vacia_de_caminos():
    assert verificar_sin_arcos_compartidos([])


def test_vertices_compartidos_estan_permitidos():
    assert verificar_sin_arcos_compartidos([["s", "A", "D", "G", "t"], ["s", "C", "D", "E", "t"]])


# ----------------------------------------------------------------------
# verificar_corte_desconecta
# ----------------------------------------------------------------------

def test_corte_desconecta_y_no_modifica_original(grafo_figura1):
    arcos_antes = grafo_figura1.arcos()
    bloqueados_antes = set(grafo_figura1.bloqueados)
    assert verificar_corte_desconecta(grafo_figura1, CORTE_FIGURA1, "s", "t")
    assert grafo_figura1.arcos() == arcos_antes
    assert grafo_figura1.bloqueados == bloqueados_antes
    assert _es_alcanzable(grafo_figura1, "s", "t")


def test_corte_incompleto_no_desconecta(grafo_figura1):
    assert not verificar_corte_desconecta(grafo_figura1, [("E", "t")], "s", "t")


def test_corte_con_arco_inexistente(grafo_figura1):
    assert not verificar_corte_desconecta(grafo_figura1, [("E", "t"), ("G", "t"), ("t", "s")], "s", "t")


def test_corte_acepta_arcos_como_listas(grafo_figura1):
    assert verificar_corte_desconecta(grafo_figura1, [["E", "t"], ["G", "t"]], "s", "t")


def test_corte_en_grafo_inicial(grafo_inicial):
    assert verificar_corte_desconecta(grafo_inicial, [("D", "G"), ("E", "H")], "s", "t")
    assert not verificar_corte_desconecta(grafo_inicial, [("D", "G")], "s", "t")


# ----------------------------------------------------------------------
# verificar_igualdad_menger
# ----------------------------------------------------------------------

def test_igualdad_menger():
    assert verificar_igualdad_menger(2, CORTE_FIGURA1)
    assert not verificar_igualdad_menger(3, CORTE_FIGURA1)
    assert verificar_igualdad_menger(0, [])


# ----------------------------------------------------------------------
# verificar_todo
# ----------------------------------------------------------------------

CLAVES = {
    "camino_minimo_valido",
    "caminos_disjuntos_validos",
    "sin_arcos_compartidos",
    "cantidad_coincide",
    "corte_desconecta",
    "igualdad_menger",
}


def test_verificar_todo_resultado_correcto(grafo_figura1):
    informe = verificar_todo(grafo_figura1, _resultado_correcto_figura1())
    assert set(informe) == CLAVES
    assert all(informe.values()), informe


def test_verificar_todo_corte_erroneo(grafo_figura1):
    resultado = _resultado_correcto_figura1()
    resultado.corte_minimo = [("E", "t"), ("F", "G")]
    informe = verificar_todo(grafo_figura1, resultado)
    assert informe["corte_desconecta"] is False
    assert informe["igualdad_menger"] is True
    assert informe["camino_minimo_valido"] is True


def test_verificar_todo_detecta_caminos_que_comparten(grafo_figura1):
    resultado = _resultado_correcto_figura1()
    resultado.caminos_disjuntos = [CAMINO_1, ["s", "A", "B", "E", "t"]]
    informe = verificar_todo(grafo_figura1, resultado)
    assert informe["sin_arcos_compartidos"] is False
    assert informe["caminos_disjuntos_validos"] is True


def test_verificar_todo_sin_camino(grafo_figura1):
    grafo_figura1.bloquear_arco("E", "t")
    grafo_figura1.bloquear_arco("G", "t")
    resultado = ResultadoConfiguracion(nombre="Sin salida")
    informe = verificar_todo(grafo_figura1, resultado)
    assert all(informe.values()), informe


def test_verificar_todo_camino_none_pero_alcanzable(grafo_figura1):
    resultado = ResultadoConfiguracion(nombre="Mal calculado")
    informe = verificar_todo(grafo_figura1, resultado)
    assert informe["camino_minimo_valido"] is False
    assert informe["corte_desconecta"] is False
