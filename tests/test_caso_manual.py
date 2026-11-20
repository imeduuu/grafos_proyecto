"""Caso pequeño resuelto a mano (datos/caso_verificacion.json).

- Las pruebas del resultado manual usan solo el verificador independiente,
  así que funcionan aunque los algoritmos aún no estén implementados.
- La comparación con el código se omite automáticamente mientras algún
  algoritmo de ``src.algoritmos`` lance NotImplementedError.
"""

import json
import os

import pytest

from src.algoritmos.busqueda_anchura import camino_minimo
from src.algoritmos.corte_minimo import corte_minimo
from src.algoritmos.flujo_maximo import maximo_caminos_disjuntos
from src.modelo.cargador import cargar_grafo_json
from src.verificacion.verificador import (
    verificar_camino_valido,
    verificar_corte_desconecta,
    verificar_igualdad_menger,
    verificar_sin_arcos_compartidos,
)

RUTA = os.path.join(os.path.dirname(os.path.dirname(__file__)), "datos", "caso_verificacion.json")


@pytest.fixture
def esperado():
    with open(RUTA, encoding="utf-8") as f:
        return json.load(f)["resultado_manual_esperado"]


@pytest.fixture
def grafo_caso():
    return cargar_grafo_json(RUTA)


# ----------------------------------------------------------------------
# Resultado manual vs. verificador (no depende de los algoritmos)
# ----------------------------------------------------------------------

def test_camino_minimo_manual_es_valido(grafo_caso, esperado):
    camino = esperado["camino_minimo_ejemplo"]
    assert verificar_camino_valido(grafo_caso, camino, grafo_caso.entrada, grafo_caso.salida)
    assert len(camino) - 1 == esperado["longitud_minima"]


def test_caminos_disjuntos_manuales_son_validos(grafo_caso, esperado):
    caminos = esperado["caminos_disjuntos_ejemplo"]
    assert len(caminos) == esperado["max_caminos_sin_arcos_compartidos"]
    for camino in caminos:
        assert verificar_camino_valido(grafo_caso, camino, grafo_caso.entrada, grafo_caso.salida)
    assert verificar_sin_arcos_compartidos(caminos)


def test_corte_minimo_manual_desconecta_y_cumple_menger(grafo_caso, esperado):
    corte = [tuple(arco) for arco in esperado["corte_minimo_ejemplo"]]
    assert verificar_corte_desconecta(grafo_caso, corte, grafo_caso.entrada, grafo_caso.salida)
    assert verificar_igualdad_menger(esperado["max_caminos_sin_arcos_compartidos"], corte)


# ----------------------------------------------------------------------
# Resultado del código vs. resultado manual (se activa con los algoritmos)
# ----------------------------------------------------------------------

def test_caso_manual_coincide_con_codigo(grafo_caso, esperado):
    s, t = grafo_caso.entrada, grafo_caso.salida
    try:
        camino, longitud = camino_minimo(grafo_caso, s, t)
        cantidad, caminos = maximo_caminos_disjuntos(grafo_caso, s, t)
        corte = corte_minimo(grafo_caso, s, t)
    except NotImplementedError as error:
        pytest.skip(f"Algoritmos aún no implementados: {error}")

    assert longitud == esperado["longitud_minima"]
    assert cantidad == esperado["max_caminos_sin_arcos_compartidos"]
    assert len(corte) == cantidad

    # Además, lo que entrega el código debe pasar el verificador independiente.
    assert verificar_camino_valido(grafo_caso, camino, s, t)
    assert all(verificar_camino_valido(grafo_caso, c, s, t) for c in caminos)
    assert verificar_sin_arcos_compartidos(caminos)
    assert verificar_corte_desconecta(grafo_caso, corte, s, t)
