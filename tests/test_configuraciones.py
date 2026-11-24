"""Pruebas de calcular_resultados y comparar_configuraciones."""

import os

from src.modelo.cargador import cargar_configuracion, cargar_grafo_json
from src.simulacion.configuraciones import calcular_resultados, comparar_configuraciones
from src.verificacion.verificador import verificar_todo

DATOS = os.path.join(os.path.dirname(os.path.dirname(__file__)), "datos")
BASE = os.path.join(DATOS, "grafo_inicial.json")


def test_figura1(grafo_figura1):
    r = calcular_resultados(grafo_figura1, "Figura 1")
    assert r.existe_camino and r.longitud_minima == 4
    assert r.cantidad_caminos_disjuntos == 2 == len(r.corte_minimo)
    assert all(verificar_todo(grafo_figura1, r).values())


def test_sin_camino_no_asigna_longitud(grafo_figura1):
    grafo_figura1.bloquear_arco("s", "A")
    grafo_figura1.bloquear_arco("s", "C")
    r = calcular_resultados(grafo_figura1, "Bloqueada")
    assert not r.existe_camino
    assert r.camino_minimo is None and r.longitud_minima is None
    assert r.cantidad_caminos_disjuntos == 0 and r.caminos_disjuntos == []
    assert r.corte_minimo == []
    assert all(verificar_todo(grafo_figura1, r).values())
    fila = comparar_configuraciones([r])[0]
    assert fila["Longitud mínima d(s,t)"] == "No existe"
    assert fila["Corte mínimo"].startswith("∅")


def test_tres_configuraciones_del_grupo():
    grafos = [cargar_grafo_json(BASE)] + [
        cargar_configuracion(BASE, os.path.join(DATOS, "configuraciones", f"modificacion_{i}.json"))
        for i in (1, 2)
    ]
    resultados = [calcular_resultados(g, str(i)) for i, g in enumerate(grafos)]
    for g, r in zip(grafos, resultados):
        assert (g.entrada, g.salida) == ("s", "t")
        assert all(verificar_todo(g, r).values())
    filas = comparar_configuraciones(resultados)
    assert len(filas) == 3
    assert all(f["Máx. caminos sin arcos compartidos"] == f["|Corte mínimo|"] for f in filas)
