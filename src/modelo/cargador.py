"""Carga y guardado de laberintos (grafos dirigidos) en formato JSON.

Formato del archivo de un grafo::

    {
      "vertices": ["s", "A", "t"],
      "arcos": [["s", "A"], ["A", "t"]],
      "bloqueados": [["A", "t"]],          # opcional
      "entrada": "s",
      "salida": "t",
      "posiciones": {"s": [0, 0], "A": [1, 0], "t": [2, 0]}
    }

Las claves extra (por ejemplo "descripcion" o "resultado_manual_esperado")
se ignoran. El grafo se construye siempre con la API de ``GrafoDirigido``
para que se apliquen todas sus validaciones.
"""

import json
import os
from typing import Any, Dict, List, Tuple

from src.modelo.grafo import GrafoDirigido


# ----------------------------------------------------------------------
# Auxiliares internos
# ----------------------------------------------------------------------

def _leer_json(ruta: str) -> Dict[str, Any]:
    """Lee un archivo JSON y verifica que su contenido sea un objeto.

    Parámetros:
        ruta: ruta del archivo JSON que se leerá.

    Retorna:
        Diccionario con las claves y valores del archivo.

    Errores:
        FileNotFoundError si el archivo no existe; ValueError si el JSON
        está mal formado o su raíz no es un objeto.
    """
    nombre = os.path.basename(ruta)
    with open(ruta, encoding="utf-8") as archivo:
        try:
            datos = json.load(archivo)
        except json.JSONDecodeError as error:
            raise ValueError(f"El archivo '{nombre}' no contiene un JSON válido: {error}") from error
    if not isinstance(datos, dict):
        raise ValueError(f"El archivo '{nombre}' debe contener un objeto JSON (diccionario) en la raíz.")
    return datos


def _como_arco(arco: Any, nombre: str, clave: str) -> Tuple[Any, Any]:
    """Convierte un elemento [u, v] del JSON en la tupla (u, v).

    Parámetros:
        arco: valor JSON que representa un arco.
        nombre: nombre del archivo para contextualizar errores.
        clave: clave del objeto JSON donde se encontró el arco.

    Retorna:
        Tupla (origen, destino).

    Errores:
        ValueError si el elemento no contiene exactamente dos valores.
    """
    if not isinstance(arco, (list, tuple)) or len(arco) != 2:
        raise ValueError(
            f"Arco inválido en '{nombre}' (clave '{clave}'): {arco!r}. "
            "Cada arco debe ser una lista [origen, destino]."
        )
    return arco[0], arco[1]


def _lista_de_arcos(datos: Dict[str, Any], clave: str, nombre: str) -> List[Any]:
    """Obtiene una lista de arcos de una clave opcional del JSON.

    Parámetros:
        datos: objeto JSON leído del archivo.
        clave: nombre de la clave que contiene los arcos.
        nombre: nombre del archivo para contextualizar errores.

    Retorna:
        Lista asociada a la clave, o una lista vacía si no existe.

    Errores:
        ValueError si el valor asociado no es una lista.
    """
    valor = datos.get(clave, [])
    if not isinstance(valor, list):
        raise ValueError(f"En '{nombre}', la clave '{clave}' debe ser una lista de arcos [origen, destino].")
    return valor


def _agregar_arcos(grafo: GrafoDirigido, arcos: List[Any], nombre: str, clave: str) -> None:
    """Agrega al grafo los arcos declarados en los datos JSON.

    Parámetros:
        grafo: grafo al que se incorporarán los arcos.
        arcos: elementos JSON que representan arcos.
        nombre: nombre del archivo para contextualizar errores.
        clave: clave JSON de origen de la lista.

    Retorna:
        None.

    Errores:
        ValueError si un arco tiene formato inválido o el grafo lo rechaza.
    """
    for arco in arcos:
        origen, destino = _como_arco(arco, nombre, clave)
        try:
            grafo.agregar_arco(origen, destino)
        except ValueError as error:
            raise ValueError(
                f"Arco inválido en '{nombre}' (clave '{clave}'): [{origen}, {destino}]. {error}"
            ) from error


def _bloquear_arcos(grafo: GrafoDirigido, arcos: List[Any], nombre: str, clave: str) -> None:
    """Bloquea en el grafo los arcos declarados en los datos JSON.

    Parámetros:
        grafo: grafo cuyos arcos se bloquearán.
        arcos: elementos JSON que representan arcos existentes.
        nombre: nombre del archivo para contextualizar errores.
        clave: clave JSON de origen de la lista.

    Retorna:
        None.

    Errores:
        ValueError si un elemento es inválido o el arco no existe.
    """
    for arco in arcos:
        origen, destino = _como_arco(arco, nombre, clave)
        try:
            grafo.bloquear_arco(origen, destino)
        except ValueError as error:
            raise ValueError(
                f"No se puede bloquear el arco [{origen}, {destino}] de '{nombre}' (clave '{clave}'). {error}"
            ) from error


def _definir_extremos(grafo: GrafoDirigido, entrada: Any, salida: Any, nombre: str) -> None:
    """Asigna los vértices de entrada y salida e informa errores de datos.

    Parámetros:
        grafo: grafo cuyos extremos se configurarán.
        entrada: identificador del vértice de entrada.
        salida: identificador del vértice de salida.
        nombre: nombre del archivo para contextualizar errores.

    Retorna:
        None.

    Errores:
        ValueError si faltan extremos, no existen o son iguales.
    """
    if entrada is None or salida is None:
        raise ValueError(f"En '{nombre}' faltan las claves 'entrada' y/o 'salida'.")
    try:
        grafo.definir_entrada_salida(entrada, salida)
    except ValueError as error:
        raise ValueError(f"Entrada/salida inválidas en '{nombre}': {error}") from error


# ----------------------------------------------------------------------
# API pública
# ----------------------------------------------------------------------

def cargar_grafo_json(ruta: str) -> GrafoDirigido:
    """Lee un laberinto desde un archivo JSON y retorna un ``GrafoDirigido``.

    Usa ``agregar_vertice``, ``agregar_arco``, ``bloquear_arco`` (si existe la
    clave opcional "bloqueados") y ``definir_entrada_salida``. Las posiciones
    [x, y] se convierten en tuplas (float, float). Las claves extra se ignoran.

    Parámetros:
        ruta: ruta del archivo JSON que contiene la configuración.

    Retorna:
        GrafoDirigido construido y validado a partir del archivo.

    Errores:
        FileNotFoundError si el archivo no existe. ValueError, con el nombre
        del archivo en el mensaje, si el JSON es inválido, faltan vértices,
        arcos o extremos, algún arco incumple las reglas del modelo o una
        posición no es numérica o corresponde a un vértice inexistente.
    """
    nombre = os.path.basename(ruta)
    datos = _leer_json(ruta)

    vertices = datos.get("vertices") or []
    arcos = datos.get("arcos") or []
    if not isinstance(vertices, list) or not vertices:
        raise ValueError(
            f"El archivo '{nombre}' no tiene vértices: la lista 'vertices' está vacía o falta "
            "(¿plantilla sin completar?)."
        )
    if not isinstance(arcos, list) or not arcos:
        raise ValueError(
            f"El archivo '{nombre}' no tiene arcos: la lista 'arcos' está vacía o falta "
            "(¿plantilla sin completar?)."
        )

    grafo = GrafoDirigido()
    for vertice in vertices:
        grafo.agregar_vertice(vertice)

    _agregar_arcos(grafo, arcos, nombre, "arcos")
    _bloquear_arcos(grafo, _lista_de_arcos(datos, "bloqueados", nombre), nombre, "bloqueados")
    _definir_extremos(grafo, datos.get("entrada"), datos.get("salida"), nombre)

    posiciones = datos.get("posiciones") or {}
    if not isinstance(posiciones, dict):
        raise ValueError(f"En '{nombre}', 'posiciones' debe ser un objeto {{vertice: [x, y]}}.")
    for vertice, posicion in posiciones.items():
        if vertice not in grafo.vertices:
            raise ValueError(f"En '{nombre}' hay una posición para el vértice inexistente '{vertice}'.")
        try:
            x, y = posicion
            grafo.posiciones[vertice] = (float(x), float(y))
        except (TypeError, ValueError) as error:
            raise ValueError(
                f"Posición inválida en '{nombre}' para el vértice '{vertice}': {posicion!r}. "
                "Debe ser una lista [x, y] de números."
            ) from error

    return grafo


def guardar_grafo_json(grafo: GrafoDirigido, ruta: str) -> None:
    """Guarda el grafo en un archivo JSON (UTF-8, indentado, sin escapar tildes).

    Escribe "vertices" en orden de inserción, "arcos" (todos, incluidos los
    bloqueados), "bloqueados" (lista ordenada), "entrada", "salida" y
    "posiciones" como listas [x, y]. El archivo resultante se puede releer con
    ``cargar_grafo_json`` y produce el mismo grafo.

    Parámetros:
        grafo: laberinto cuyos datos se serializarán.
        ruta: ruta del archivo JSON de salida.

    Retorna:
        None. Escribe la representación del grafo en la ruta indicada.

    Errores:
        OSError si no se puede escribir el archivo. Si falta algún extremo,
        se guarda como null y el archivo será rechazado al volver a cargarlo.
    """
    datos = {
        "vertices": list(grafo.adyacencia),
        "arcos": [[u, v] for u, v in grafo.arcos()],
        "bloqueados": [[u, v] for u, v in sorted(grafo.bloqueados)],
        "entrada": grafo.entrada,
        "salida": grafo.salida,
        "posiciones": {v: [x, y] for v, (x, y) in grafo.posiciones.items()},
    }
    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, ensure_ascii=False, indent=2)
        archivo.write("\n")


def cargar_configuracion(ruta_base: str, ruta_modificacion: str) -> GrafoDirigido:
    """Carga el grafo base y le aplica una modificación descrita en JSON.

    Orden de aplicación:
    1. Carga ``ruta_base`` con ``cargar_grafo_json`` (exactamente esa ruta; la
       clave "basada_en" de la modificación no se usa para buscar el archivo).
    2. Agrega los arcos de "arcos_agregados".
    3. Bloquea los arcos de "arcos_bloqueados" (así se puede bloquear un arco
       recién agregado).
    4. Si la modificación trae "entrada" y/o "salida", las redefine (la que
       falte se mantiene igual que en la base).

    El archivo base en disco no se modifica.

    Parámetros:
        ruta_base: ruta del JSON de la red original.
        ruta_modificacion: ruta del JSON con los cambios que se aplicarán.

    Retorna:
        GrafoDirigido independiente con las modificaciones aplicadas.

    Errores:
        FileNotFoundError si falta alguno de los archivos. ValueError si la
        base o la modificación contiene JSON, arcos o extremos inválidos.
    """
    grafo = cargar_grafo_json(ruta_base)

    nombre = os.path.basename(ruta_modificacion)
    modificacion = _leer_json(ruta_modificacion)

    _agregar_arcos(grafo, _lista_de_arcos(modificacion, "arcos_agregados", nombre), nombre, "arcos_agregados")
    _bloquear_arcos(grafo, _lista_de_arcos(modificacion, "arcos_bloqueados", nombre), nombre, "arcos_bloqueados")

    if "entrada" in modificacion or "salida" in modificacion:
        entrada = modificacion.get("entrada", grafo.entrada)
        salida = modificacion.get("salida", grafo.salida)
        _definir_extremos(grafo, entrada, salida, nombre)

    return grafo
