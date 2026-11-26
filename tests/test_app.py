"""Pruebas headless de la interfaz con la API oficial AppTest de Streamlit."""

from pathlib import Path

import pytest

pytest.importorskip(
    "streamlit.testing.v1",
    reason="AppTest requiere una versión de Streamlit que incluya streamlit.testing.v1.",
)
from streamlit.testing.v1 import AppTest

RAIZ = Path(__file__).resolve().parents[1]
MAIN = RAIZ / "main.py"


def _ejecutar_app():
    """Inicia main.py con AppTest y amplía el límite para renderizar los gráficos."""
    return AppTest.from_file(str(MAIN)).run(timeout=30)


def _boton(app, etiqueta):
    """Busca un botón de AppTest por el texto visible que usa la interfaz."""
    return next(boton for boton in app.button if boton.label == etiqueta)


def _selector(app, clave):
    """Busca un selector de AppTest por su key real."""
    return next(selector for selector in app.selectbox if selector.key == clave)


def _assert_sin_excepciones(app):
    """Falla con los mensajes capturados si la ejecución de la aplicación falló."""
    assert not app.exception, [excepcion.message for excepcion in app.exception]


def test_main_carga_sin_excepciones():
    app = _ejecutar_app()

    _assert_sin_excepciones(app)


def test_recalcular_muestra_longitud_minima_de_cuatro():
    app = _ejecutar_app()

    _boton(app, "🔄 Recalcular").click().run(timeout=30)

    _assert_sin_excepciones(app)
    assert any("d(s,t) = **4**" in bloque.value for bloque in app.markdown)


def test_interfaz_bloquea_restablece_y_agrega_pasillo():
    app = _ejecutar_app()

    _selector(app, "sel_bloquear").select(("s", "A")).run(timeout=30)
    _boton(app, "Bloquear pasillo").click().run(timeout=30)
    _assert_sin_excepciones(app)
    assert app.session_state["grafo"].esta_bloqueado("s", "A")

    _selector(app, "sel_restablecer").select(("s", "A")).run(timeout=30)
    _boton(app, "Restablecer pasillo").click().run(timeout=30)
    _assert_sin_excepciones(app)
    assert not app.session_state["grafo"].esta_bloqueado("s", "A")

    _selector(app, "nuevo_origen").select("H")
    _selector(app, "nuevo_destino").select("A")
    _boton(app, "Agregar pasillo").click().run(timeout=30)
    _assert_sin_excepciones(app)
    assert app.session_state["grafo"].existe_arco("H", "A")


@pytest.mark.parametrize(
    ("origen", "destino", "mensaje"),
    [
        ("A", "A", "No se permiten lazos"),
        ("B", "A", "arco recíproco"),
    ],
    ids=("lazo", "arco-reciproco"),
)
def test_interfaz_rechaza_lazos_y_arcos_reciprocos_sin_cambiar_el_grafo(origen, destino, mensaje):
    app = _ejecutar_app()
    grafo = app.session_state["grafo"]
    arcos_originales = tuple(grafo.arcos())

    _selector(app, "nuevo_origen").select(origen)
    _selector(app, "nuevo_destino").select(destino)
    _boton(app, "Agregar pasillo").click().run(timeout=30)

    _assert_sin_excepciones(app)
    assert any(mensaje in error.value for error in app.error)
    assert tuple(grafo.arcos()) == arcos_originales


def test_pestana_comparacion_muestra_las_tres_configuraciones():
    app = _ejecutar_app()

    _assert_sin_excepciones(app)
    etiquetas = [pestana.label for pestana in app.tabs]
    assert "Comparación de configuraciones" in etiquetas
    assert {"Original", "Modificación 1", "Modificación 2"}.issubset(etiquetas)
    tabla = app.dataframe[0].value
    assert tabla["Configuración"].tolist() == ["Original", "Modificación 1", "Modificación 2"]
