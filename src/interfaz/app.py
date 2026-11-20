"""Aplicación Streamlit del laberinto (se ejecuta con ``streamlit run main.py``).

Permite, sin tocar código: ver el grafo, elegir entrada y salida,
bloquear/restablecer y agregar pasillos, recalcular resultados y comparar
las 3 configuraciones. El grafo vive en ``st.session_state["grafo"]``.
"""

def inicializar_estado() -> None:
    """Carga datos/grafo_inicial.json en session_state la primera vez.

    Parámetros:
        Ninguno.

    Retorna:
        None.
    """
    raise NotImplementedError("TODO: implementar inicializar_estado")


def panel_seleccion_extremos() -> None:
    """Muestra los selectores de entrada y salida.

    Valida que ambos vértices existan y sean distintos.

    Parámetros:
        Ninguno.

    Retorna:
        None.
    """
    raise NotImplementedError("TODO: implementar panel_seleccion_extremos")


def panel_bloqueos() -> None:
    """Permite bloquear un pasillo activo o restablecer uno bloqueado.

    Parámetros:
        Ninguno.

    Retorna:
        None.
    """
    raise NotImplementedError("TODO: implementar panel_bloqueos")


def panel_agregar_arco() -> None:
    """Muestra el formulario para agregar un pasillo nuevo.

    Si el arco es un lazo, está repetido o es recíproco, muestra el error.

    Parámetros:
        Ninguno.

    Retorna:
        None.
    """
    raise NotImplementedError("TODO: implementar panel_agregar_arco")


def panel_resultados() -> None:
    """Muestra el botón Recalcular, el dibujo y los resultados.

    Incluye el camino mínimo (o "no existe camino"), los caminos sin arcos
    compartidos, el corte mínimo y las verificaciones.

    Parámetros:
        Ninguno.

    Retorna:
        None.
    """
    raise NotImplementedError("TODO: implementar panel_resultados")


def panel_comparacion() -> None:
    """Muestra la tabla comparativa de la red original y las 2 modificaciones.

    Parámetros:
        Ninguno.

    Retorna:
        None.
    """
    raise NotImplementedError("TODO: implementar panel_comparacion")


def ejecutar_aplicacion() -> None:
    """Arma la página completa de la aplicación con todos los paneles.

    Parámetros:
        Ninguno.

    Retorna:
        None.
    """
    raise NotImplementedError("TODO: implementar ejecutar_aplicacion")
