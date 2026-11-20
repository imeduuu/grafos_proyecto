import json
import os

import pytest

from src.modelo.cargador import cargar_configuracion, cargar_grafo_json, guardar_grafo_json

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA_FIGURA1 = os.path.join(RAIZ, "datos", "ejemplo_figura1.json")


def _escribir_json(ruta, datos):
    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, ensure_ascii=False)


def test_ida_y_vuelta_con_arco_bloqueado(grafo_figura1, tmp_path):
    grafo_figura1.bloquear_arco("s", "C")
    ruta = tmp_path / "ida_vuelta.json"

    guardar_grafo_json(grafo_figura1, str(ruta))
    recargado = cargar_grafo_json(str(ruta))

    assert list(recargado.adyacencia) == list(grafo_figura1.adyacencia)
    assert recargado.arcos() == grafo_figura1.arcos()
    assert recargado.bloqueados == {("s", "C")}
    assert recargado.entrada == "s"
    assert recargado.salida == "t"
    assert recargado.posiciones == grafo_figura1.posiciones


def test_plantilla_vacia_lanza_error(tmp_path):
    ruta = tmp_path / "plantilla.json"
    _escribir_json(ruta, {"vertices": [], "arcos": [], "entrada": "s", "salida": "t", "posiciones": {}})

    with pytest.raises(ValueError, match="plantilla.json"):
        cargar_grafo_json(str(ruta))


def test_lazo_en_json_lanza_error(tmp_path):
    ruta = tmp_path / "lazo.json"
    _escribir_json(ruta, {"vertices": ["s", "t"], "arcos": [["s", "t"], ["t", "t"]], "entrada": "s", "salida": "t"})

    with pytest.raises(ValueError, match="lazo.json") as error:
        cargar_grafo_json(str(ruta))
    assert "[t, t]" in str(error.value)


def test_configuracion_agrega_y_bloquea_sin_modificar_base(tmp_path):
    with open(RUTA_FIGURA1, "rb") as archivo:
        contenido_original = archivo.read()

    ruta_mod = tmp_path / "modificacion.json"
    _escribir_json(ruta_mod, {
        "arcos_agregados": [["B", "D"]],
        "arcos_bloqueados": [["B", "D"], ["G", "t"]],
        "entrada": "s",
        "salida": "t",
    })

    grafo = cargar_configuracion(RUTA_FIGURA1, str(ruta_mod))

    assert grafo.existe_arco("B", "D")
    assert grafo.esta_bloqueado("B", "D")
    assert grafo.esta_bloqueado("G", "t")
    assert grafo.cantidad_arcos() == 13

    with open(RUTA_FIGURA1, "rb") as archivo:
        assert archivo.read() == contenido_original
    base = cargar_grafo_json(RUTA_FIGURA1)
    assert base.cantidad_arcos() == 12
    assert base.bloqueados == set()
