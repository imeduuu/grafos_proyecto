import os
import sys
import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)

from src.modelo.cargador import cargar_grafo_json

@pytest.fixture
def grafo_figura1():
    return cargar_grafo_json(os.path.join(RAIZ, "datos", "ejemplo_figura1.json"))
