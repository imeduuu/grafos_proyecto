"""Comprobaciones de los resultados de la pauta con datos del proyecto."""

from pathlib import Path

import pytest

from src.algoritmos.busqueda_profundidad import existe_camino
from src.modelo.cargador import cargar_configuracion, cargar_grafo_json
from src.modelo.validaciones import validar_configuracion_inicial
from src.simulacion.configuraciones import calcular_resultados
from src.verificacion.verificador import verificar_todo

DATOS = Path(__file__).resolve().parents[1] / "datos"
GRAFO_INICIAL = DATOS / "grafo_inicial.json"


def _cargar_configuracion(nombre):
    """Carga la configuración solicitada a partir de los datos del proyecto."""
    if nombre == "Original":
        return cargar_grafo_json(str(GRAFO_INICIAL))
    indice = 1 if nombre == "Modificación 1" else 2
    ruta = DATOS / "configuraciones" / f"modificacion_{indice}.json"
    return cargar_configuracion(str(GRAFO_INICIAL), str(ruta))


def _resumen(resultado):
    """Construye una tupla comparable con todos los resultados calculados."""
    return (
        resultado.existe_camino,
        resultado.camino_minimo,
        resultado.longitud_minima,
        resultado.cantidad_caminos_disjuntos,
        tuple(tuple(camino) for camino in resultado.caminos_disjuntos),
        tuple(resultado.corte_minimo),
    )


def test_grafo_inicial_cumple_modelacion():
    grafo = cargar_grafo_json(str(GRAFO_INICIAL))

    assert grafo.cantidad_vertices() == 11
    assert grafo.cantidad_arcos() == 16
    assert validar_configuracion_inicial(grafo) == []


@pytest.mark.parametrize(
    ("nombre", "distancia", "cantidad_caminos", "cantidad_corte"),
    [
        ("Original", 4, 2, 2),
        ("Modificación 1", 5, 1, 1),
        ("Modificación 2", 2, 3, 3),
    ],
)
def test_configuraciones_de_pauta(nombre, distancia, cantidad_caminos, cantidad_corte):
    grafo = _cargar_configuracion(nombre)
    resultado = calcular_resultados(grafo, nombre)

    assert (grafo.entrada, grafo.salida) == ("s", "t")
    assert resultado.existe_camino
    assert resultado.longitud_minima == distancia
    assert resultado.cantidad_caminos_disjuntos == cantidad_caminos
    assert len(resultado.caminos_disjuntos) == cantidad_caminos
    assert len(resultado.corte_minimo) == cantidad_corte
    verificaciones = verificar_todo(grafo, resultado)
    assert all(verificaciones.values()), verificaciones


def test_bloquear_todos_los_arcos_finales_produce_resultado_sin_camino():
    grafo = cargar_grafo_json(str(GRAFO_INICIAL))
    grafo.bloquear_arco("G", "t")
    grafo.bloquear_arco("I", "t")

    resultado = calcular_resultados(grafo)

    assert not existe_camino(grafo, grafo.entrada, grafo.salida)
    assert resultado.existe_camino is False
    assert resultado.camino_minimo is None
    assert resultado.longitud_minima is None
    assert resultado.cantidad_caminos_disjuntos == 0
    assert resultado.caminos_disjuntos == []
    assert resultado.corte_minimo == []
    verificaciones = verificar_todo(grafo, resultado)
    assert all(verificaciones.values()), verificaciones


def test_cambiar_extremos_recalcula_resultados_y_verifica():
    grafo = cargar_grafo_json(str(GRAFO_INICIAL))
    grafo.definir_entrada_salida("A", "I")

    resultado = calcular_resultados(grafo)

    assert resultado.existe_camino
    assert resultado.longitud_minima == 4
    assert resultado.cantidad_caminos_disjuntos == 1
    assert len(resultado.corte_minimo) == 1
    verificaciones = verificar_todo(grafo, resultado)
    assert all(verificaciones.values()), verificaciones


def test_agregar_bloquear_y_restablecer_pasillo_conserva_resultados():
    grafo = cargar_grafo_json(str(GRAFO_INICIAL))
    inicial = calcular_resultados(grafo)

    grafo.agregar_arco("H", "A")
    agregado = calcular_resultados(grafo)
    assert grafo.existe_arco("H", "A")
    assert _resumen(agregado) == _resumen(inicial)

    grafo.bloquear_arco("H", "A")
    bloqueado = calcular_resultados(grafo)
    assert grafo.esta_bloqueado("H", "A")
    assert _resumen(bloqueado) == _resumen(inicial)

    grafo.restablecer_arco("H", "A")
    restablecido = calcular_resultados(grafo)
    assert not grafo.esta_bloqueado("H", "A")
    assert _resumen(restablecido) == _resumen(inicial)
    verificaciones = verificar_todo(grafo, restablecido)
    assert all(verificaciones.values()), verificaciones
