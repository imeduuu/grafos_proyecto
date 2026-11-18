import pytest
from src.modelo.grafo import GrafoDirigido

def test_rechaza_lazo():
    g = GrafoDirigido()
    g.agregar_vertice("a")
    with pytest.raises(ValueError):
        g.agregar_arco("a", "a")

def test_rechaza_reciproco():
    g = GrafoDirigido()
    g.agregar_vertice("a")
    g.agregar_vertice("b")
    g.agregar_arco("a", "b")
    with pytest.raises(ValueError):
        g.agregar_arco("b", "a")

def test_bloquear_y_restablecer(grafo_figura1):
    grafo_figura1.bloquear_arco("s", "C")
    assert "C" not in grafo_figura1.sucesores("s")
    grafo_figura1.restablecer_arco("s", "C")
    assert "C" in grafo_figura1.sucesores("s")
