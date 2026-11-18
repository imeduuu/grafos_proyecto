import json
import os
import pytest

from src.algoritmos.busqueda_anchura import camino_minimo
from src.algoritmos.corte_minimo import corte_minimo
from src.algoritmos.flujo_maximo import maximo_caminos_disjuntos
from src.modelo.cargador import cargar_grafo_json

RUTA = os.path.join(os.path.dirname(os.path.dirname(__file__)), "datos", "caso_verificacion.json")


@pytest.mark.skip(reason="TODO: completar datos/caso_verificacion.json y quitar este skip")
def test_caso_manual_coincide_con_codigo():
    with open(RUTA, encoding="utf-8") as f:
        esperado = json.load(f)["resultado_manual_esperado"]
    grafo = cargar_grafo_json(RUTA)
    s, t = grafo.entrada, grafo.salida

    _, longitud = camino_minimo(grafo, s, t)
    cantidad, _ = maximo_caminos_disjuntos(grafo, s, t)
    corte = corte_minimo(grafo, s, t)

    assert longitud == esperado["longitud_minima"]
    assert cantidad == esperado["max_caminos_sin_arcos_compartidos"]
    assert len(corte) == cantidad
