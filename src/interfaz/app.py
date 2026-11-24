"""Aplicación Streamlit del laberinto (se ejecuta con ``streamlit run main.py``).

Permite, sin tocar código: ver el grafo, elegir entrada y salida,
bloquear/restablecer y agregar pasillos, recalcular resultados y comparar
las 3 configuraciones. El grafo vive en ``st.session_state["grafo"]``.
"""

import os
from typing import List, Optional, Tuple

import matplotlib.pyplot as plt
import streamlit as st

from src.modelo.cargador import cargar_configuracion, cargar_grafo_json
from src.modelo.grafo import GrafoDirigido
from src.modelo.validaciones import validar_configuracion_inicial
from src.simulacion.configuraciones import (
    ResultadoConfiguracion,
    calcular_resultados,
    comparar_configuraciones,
    formatear_camino,
    formatear_corte,
)
from src.verificacion.verificador import verificar_todo
from src.interfaz.visualizacion import COLORES, dibujar_grafo

# Rutas de los archivos de datos (relativas a la raíz del proyecto).
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RUTA_GRAFO_INICIAL = os.path.join(RAIZ, "datos", "grafo_inicial.json")
RUTAS_MODIFICACIONES = [
    ("Modificación 1", os.path.join(RAIZ, "datos", "configuraciones", "modificacion_1.json")),
    ("Modificación 2", os.path.join(RAIZ, "datos", "configuraciones", "modificacion_2.json")),
]

# Texto legible de cada verificación de verificar_todo.
NOMBRES_VERIFICACIONES = {
    "camino_minimo_valido": "El camino mínimo respeta el sentido de los arcos activos (o de verdad no hay camino)",
    "caminos_disjuntos_validos": "Cada camino disjunto va de s a t por arcos activos",
    "sin_arcos_compartidos": "Los caminos declarados independientes no comparten arcos",
    "cantidad_coincide": "La cantidad informada coincide con los caminos mostrados",
    "corte_desconecta": "Al bloquear el corte no queda camino de s a t",
    "igualdad_menger": "|caminos sin arcos compartidos| = |corte mínimo| (Menger)",
}

MODOS_VISTA = {
    "Todo": "todo",
    "Camino mínimo": "camino_minimo",
    "Caminos sin arcos compartidos": "disjuntos",
    "Corte mínimo": "corte",
}


# ----------------------------------------------------------------------
# Auxiliares
# ----------------------------------------------------------------------

def _firma(grafo: GrafoDirigido) -> Tuple:
    """Resume el estado del grafo para detectar si cambió desde el último cálculo.

    Parámetros:
        grafo: laberinto actual.

    Retorna:
        Tupla con los arcos, los bloqueados, la entrada y la salida.
    """
    return (tuple(grafo.arcos()), tuple(sorted(grafo.bloqueados)), grafo.entrada, grafo.salida)


def _orden_vertices(grafo: GrafoDirigido) -> List[str]:
    """Lista los vértices en el orden en que fueron agregados (s primero en los datos).

    Parámetros:
        grafo: laberinto actual.

    Retorna:
        Lista de vértices.
    """
    return list(grafo.adyacencia)


def _texto_arco(arco: Tuple[str, str]) -> str:
    """Convierte (u, v) en "u → v" para los selectores.

    Parámetros:
        arco: tupla (origen, destino).

    Retorna:
        Texto del arco.
    """
    return f"{arco[0]} → {arco[1]}"


def _avisar(tipo: str, texto: str) -> None:
    """Guarda un mensaje para mostrarlo después de recargar la página.

    Parámetros:
        tipo: "success", "error", "warning" o "info".
        texto: contenido del mensaje.

    Retorna:
        None.
    """
    st.session_state["mensaje"] = (tipo, texto)


def _mostrar_mensaje_pendiente() -> None:
    """Muestra (una sola vez) el mensaje guardado por la última acción.

    Parámetros:
        Ninguno.

    Retorna:
        None.
    """
    mensaje = st.session_state.pop("mensaje", None)
    if mensaje is not None:
        tipo, texto = mensaje
        getattr(st, tipo)(texto)


def _mostrar_figura(grafo: GrafoDirigido, resultado: Optional[ResultadoConfiguracion], modo: str) -> None:
    """Dibuja el grafo con la solución (si hay) y libera la figura.

    Parámetros:
        grafo: laberinto a dibujar.
        resultado: resultados a destacar, o None para dibujar solo la red.
        modo: "todo", "camino_minimo", "disjuntos" o "corte".

    Retorna:
        None.
    """
    if resultado is None:
        fig = dibujar_grafo(grafo)
    else:
        fig = dibujar_grafo(
            grafo,
            camino_minimo=resultado.camino_minimo,
            caminos_disjuntos=resultado.caminos_disjuntos,
            corte=resultado.corte_minimo,
            modo=modo,
        )
    st.pyplot(fig)
    plt.close(fig)


def _mostrar_detalle_resultado(grafo: GrafoDirigido, resultado: ResultadoConfiguracion) -> None:
    """Muestra el texto de los resultados y las verificaciones de una configuración.

    Parámetros:
        grafo: laberinto sobre el que se calculó el resultado.
        resultado: resultados de la configuración.

    Retorna:
        None.
    """
    s, t = grafo.entrada, grafo.salida
    st.markdown("**Camino mínimo (BFS)**")
    if resultado.existe_camino:
        st.write(f"{formatear_camino(resultado.camino_minimo)}  —  d({s},{t}) = **{resultado.longitud_minima}** arcos")
    else:
        st.error(f"No existe camino dirigido de {s} a {t}. No se asigna longitud.")

    st.markdown(f"**Máximo de caminos sin arcos compartidos (flujo máximo unitario): {resultado.cantidad_caminos_disjuntos}**")
    if resultado.caminos_disjuntos:
        paleta = COLORES["caminos_disjuntos"]
        for i, camino in enumerate(resultado.caminos_disjuntos):
            color = paleta[i % len(paleta)]
            st.markdown(
                f"<span style='color:{color}; font-weight:bold'>Camino {i + 1}:</span> "
                f"{formatear_camino(camino)} ({len(camino) - 1} arcos)",
                unsafe_allow_html=True,
            )
    else:
        st.write("0 caminos disponibles.")

    st.markdown(f"**Corte mínimo de pasillos: {len(resultado.corte_minimo)}**")
    if resultado.corte_minimo:
        st.write(formatear_corte(resultado.corte_minimo))
    else:
        st.write("∅ — el conjunto vacío ya impide llegar de la entrada a la salida.")

    with st.expander("Verificaciones automáticas", expanded=True):
        verificaciones = verificar_todo(grafo, resultado)
        for clave, valor in verificaciones.items():
            icono = "✅" if valor else "❌"
            st.write(f"{icono} {NOMBRES_VERIFICACIONES.get(clave, clave)}")


# ----------------------------------------------------------------------
# Paneles
# ----------------------------------------------------------------------

def inicializar_estado() -> None:
    """Carga datos/grafo_inicial.json en session_state la primera vez.

    Parámetros:
        Ninguno.

    Retorna:
        None.
    """
    if "grafo" not in st.session_state:
        st.session_state["grafo"] = cargar_grafo_json(RUTA_GRAFO_INICIAL)
        st.session_state["resultado"] = None
        st.session_state["firma_resultado"] = None


def panel_seleccion_extremos() -> None:
    """Muestra los selectores de entrada y salida.

    Valida que ambos vértices existan y sean distintos.

    Parámetros:
        Ninguno.

    Retorna:
        None.
    """
    grafo: GrafoDirigido = st.session_state["grafo"]
    vertices = _orden_vertices(grafo)
    st.subheader("Entrada y salida")
    with st.form("form_extremos"):
        entrada = st.selectbox("Entrada (s)", vertices, index=vertices.index(grafo.entrada))
        salida = st.selectbox("Salida (t)", vertices, index=vertices.index(grafo.salida))
        if st.form_submit_button("Aplicar entrada y salida"):
            try:
                grafo.definir_entrada_salida(entrada, salida)
                _avisar("success", f"Entrada = {entrada}, salida = {salida}. Presione Recalcular.")
            except ValueError as error:
                _avisar("error", str(error))
            st.rerun()


def panel_bloqueos() -> None:
    """Permite bloquear un pasillo activo o restablecer uno bloqueado.

    Parámetros:
        Ninguno.

    Retorna:
        None.
    """
    grafo: GrafoDirigido = st.session_state["grafo"]
    st.subheader("Bloquear / restablecer pasillos")

    activos = grafo.arcos_activos()
    if activos:
        arco = st.selectbox("Pasillo activo", activos, format_func=_texto_arco, key="sel_bloquear")
        if st.button("Bloquear pasillo", width="stretch"):
            grafo.bloquear_arco(*arco)
            _avisar("warning", f"Pasillo {_texto_arco(arco)} bloqueado. Presione Recalcular.")
            st.rerun()
    else:
        st.caption("No hay pasillos activos.")

    bloqueados = [a for a in grafo.arcos() if grafo.esta_bloqueado(*a)]
    if bloqueados:
        arco = st.selectbox("Pasillo bloqueado", bloqueados, format_func=_texto_arco, key="sel_restablecer")
        if st.button("Restablecer pasillo", width="stretch"):
            grafo.restablecer_arco(*arco)
            _avisar("success", f"Pasillo {_texto_arco(arco)} restablecido. Presione Recalcular.")
            st.rerun()
    else:
        st.caption("No hay pasillos bloqueados.")


def panel_agregar_arco() -> None:
    """Muestra el formulario para agregar un pasillo nuevo.

    Si el arco es un lazo, está repetido o es recíproco, muestra el error.

    Parámetros:
        Ninguno.

    Retorna:
        None.
    """
    grafo: GrafoDirigido = st.session_state["grafo"]
    vertices = _orden_vertices(grafo)
    st.subheader("Agregar pasillo dirigido")
    with st.form("form_agregar"):
        origen = st.selectbox("Desde", vertices, key="nuevo_origen")
        destino = st.selectbox("Hacia", vertices, key="nuevo_destino")
        if st.form_submit_button("Agregar pasillo"):
            try:
                # agregar_arco rechaza lazos, repetidos y recíprocos con ValueError.
                grafo.agregar_arco(origen, destino)
                _avisar("success", f"Pasillo {origen} → {destino} agregado. Presione Recalcular.")
            except ValueError as error:
                _avisar("error", f"No se agregó el pasillo: {error}")
            st.rerun()


def panel_restaurar() -> None:
    """Botón para volver a la red original (descarta todas las modificaciones).

    Parámetros:
        Ninguno.

    Retorna:
        None.
    """
    st.subheader("Red original")
    if st.button("Restaurar red original", width="stretch"):
        st.session_state["grafo"] = cargar_grafo_json(RUTA_GRAFO_INICIAL)
        st.session_state["resultado"] = None
        st.session_state["firma_resultado"] = None
        _avisar("info", "Se restauró la red original.")
        st.rerun()


def panel_resultados() -> None:
    """Muestra el botón Recalcular, el dibujo y los resultados.

    Incluye el camino mínimo (o "no existe camino"), los caminos sin arcos
    compartidos, el corte mínimo y las verificaciones.

    Parámetros:
        Ninguno.

    Retorna:
        None.
    """
    grafo: GrafoDirigido = st.session_state["grafo"]

    activos = len(grafo.arcos_activos())
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("|V|", grafo.cantidad_vertices())
    c2.metric("|E| (total)", grafo.cantidad_arcos())
    c3.metric("Pasillos activos", activos)
    c4.metric("Pasillos bloqueados", grafo.cantidad_arcos() - activos)

    if st.button("🔄 Recalcular", type="primary"):
        st.session_state["resultado"] = calcular_resultados(grafo, "Configuración actual")
        st.session_state["firma_resultado"] = _firma(grafo)

    resultado: Optional[ResultadoConfiguracion] = st.session_state.get("resultado")
    vigente = resultado is not None and st.session_state.get("firma_resultado") == _firma(grafo)

    if resultado is None:
        st.info("Presione **Recalcular** para ejecutar los algoritmos sobre la red actual.")
    elif not vigente:
        st.warning("La red cambió desde el último cálculo. Presione **Recalcular** para actualizar los resultados.")

    columna_dibujo, columna_texto = st.columns([3, 2])
    with columna_dibujo:
        etiqueta = st.radio("Destacar", list(MODOS_VISTA), horizontal=True, disabled=not vigente)
        _mostrar_figura(grafo, resultado if vigente else None, MODOS_VISTA[etiqueta])
    with columna_texto:
        if vigente:
            _mostrar_detalle_resultado(grafo, resultado)


def panel_comparacion() -> None:
    """Muestra la tabla comparativa de la red original y las 2 modificaciones.

    Parámetros:
        Ninguno.

    Retorna:
        None.
    """
    st.markdown(
        "Comparación de la red original con las dos modificaciones definidas en "
        "`datos/configuraciones/`, manteniendo la misma entrada y salida."
    )
    try:
        configuraciones = [("Original", cargar_grafo_json(RUTA_GRAFO_INICIAL))]
        for nombre, ruta in RUTAS_MODIFICACIONES:
            configuraciones.append((nombre, cargar_configuracion(RUTA_GRAFO_INICIAL, ruta)))
    except (OSError, ValueError) as error:
        st.error(f"No se pudieron cargar las configuraciones: {error}")
        return

    errores = validar_configuracion_inicial(configuraciones[0][1])
    if errores:
        st.error("La red original no cumple las restricciones:\n- " + "\n- ".join(errores))
    else:
        st.success("La red original cumple las restricciones de la configuración inicial "
                   "(10–12 vértices, 14–20 arcos, sin lazos/repetidos/recíprocos/aislados, ≥ 2 caminos sin arcos compartidos).")

    resultados = [calcular_resultados(grafo, nombre) for nombre, grafo in configuraciones]
    st.dataframe(comparar_configuraciones(resultados), width="stretch", hide_index=True)

    pestañas = st.tabs([nombre for nombre, _ in configuraciones])
    for pestaña, (nombre, grafo), resultado in zip(pestañas, configuraciones, resultados):
        with pestaña:
            columna_dibujo, columna_texto = st.columns([3, 2])
            with columna_dibujo:
                _mostrar_figura(grafo, resultado, "todo")
            with columna_texto:
                _mostrar_detalle_resultado(grafo, resultado)


def ejecutar_aplicacion() -> None:
    """Arma la página completa de la aplicación con todos los paneles.

    Parámetros:
        Ninguno.

    Retorna:
        None.
    """
    st.set_page_config(page_title="Laberintos y rutas alternativas", layout="wide")
    inicializar_estado()

    st.title("Simulador de laberintos y rutas alternativas")
    st.caption("Teoría de Grafos – INFO1158 · Camino mínimo (BFS), caminos sin arcos compartidos "
               "(flujo máximo unitario) y corte mínimo.")

    with st.sidebar:
        panel_seleccion_extremos()
        st.divider()
        panel_bloqueos()
        st.divider()
        panel_agregar_arco()
        st.divider()
        panel_restaurar()

    _mostrar_mensaje_pendiente()

    pestaña_simulacion, pestaña_comparacion = st.tabs(["Simulación interactiva", "Comparación de configuraciones"])
    with pestaña_simulacion:
        panel_resultados()
    with pestaña_comparacion:
        panel_comparacion()
