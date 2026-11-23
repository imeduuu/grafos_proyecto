"""Pruebas de la visualización (tarea 12): no revisan el dibujo, solo que no falle."""

import matplotlib
matplotlib.use("Agg")  # sin ventanas: las pruebas no deben abrir gráficos

import matplotlib.pyplot as plt
import pytest

from src.interfaz.visualizacion import MODOS, calcular_posiciones, dibujar_grafo


def test_posiciones_del_json(grafo_figura1):
    """Con posiciones completas en el JSON, se usan tal cual."""
    posiciones = calcular_posiciones(grafo_figura1)
    assert set(posiciones) == grafo_figura1.vertices
    for v in grafo_figura1.vertices:
        assert posiciones[v] == tuple(grafo_figura1.posiciones[v])


def test_posiciones_automaticas_reproducibles(grafo_figura1):
    """Si falta alguna posición, la distribución automática cubre todos los vértices y es estable."""
    grafo_figura1.posiciones.clear()
    primera = calcular_posiciones(grafo_figura1)
    segunda = calcular_posiciones(grafo_figura1)
    assert set(primera) == grafo_figura1.vertices
    assert primera == segunda


@pytest.mark.parametrize("modo", MODOS)
def test_dibuja_todos_los_modos(grafo_figura1, modo):
    """Cada modo retorna una figura de matplotlib."""
    camino = ["s", "A", "B", "E", "t"]
    disjuntos = [["s", "A", "B", "E", "t"], ["s", "C", "F", "G", "t"]]
    corte = [("s", "A"), ("s", "C")]
    fig = dibujar_grafo(grafo_figura1, camino, disjuntos, corte, modo)
    assert isinstance(fig, plt.Figure)
    plt.close(fig)


def test_dibuja_sin_resultados(grafo_figura1):
    """Sin camino (None) ni caminos ni corte, igual dibuja el grafo."""
    fig = dibujar_grafo(grafo_figura1, None, [], [], "todo")
    assert isinstance(fig, plt.Figure)
    plt.close(fig)


def test_modo_invalido(grafo_figura1):
    """Un modo desconocido es un error de programación: se rechaza."""
    with pytest.raises(ValueError):
        dibujar_grafo(grafo_figura1, modo="otro")
