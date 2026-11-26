"""Verifica restricciones de imports y documentación con el AST de Python."""

import ast
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
SRC = RAIZ / "src"
PAQUETES_SIN_BIBLIOTECAS_DE_GRAFOS = (
    "algoritmos",
    "modelo",
    "simulacion",
    "verificacion",
)
BIBLIOTECAS_PROHIBIDAS = {"networkx", "igraph", "scipy", "graph_tool"}


def _archivos_python(directorio):
    """Entrega todos los archivos Python de un directorio y sus subdirectorios."""
    return sorted(directorio.rglob("*.py"))


def test_modulos_de_calculo_no_importan_bibliotecas_de_grafos():
    hallazgos = []
    for paquete in PAQUETES_SIN_BIBLIOTECAS_DE_GRAFOS:
        for ruta in _archivos_python(SRC / paquete):
            arbol = ast.parse(ruta.read_text(encoding="utf-8"), filename=str(ruta))
            for nodo in ast.walk(arbol):
                if isinstance(nodo, ast.Import):
                    modulos = [alias.name for alias in nodo.names]
                elif isinstance(nodo, ast.ImportFrom) and nodo.module:
                    modulos = [nodo.module]
                else:
                    continue
                for modulo in modulos:
                    raiz_modulo = modulo.split(".", 1)[0]
                    if raiz_modulo in BIBLIOTECAS_PROHIBIDAS:
                        hallazgos.append(f"{ruta.relative_to(RAIZ)}:{nodo.lineno}: {modulo}")

    assert not hallazgos, "Imports de bibliotecas de grafos detectados:\n" + "\n".join(hallazgos)


def test_toda_funcion_y_clase_publica_tiene_docstring():
    faltantes = []
    for ruta in _archivos_python(SRC):
        arbol = ast.parse(ruta.read_text(encoding="utf-8"), filename=str(ruta))
        for nodo in ast.walk(arbol):
            if isinstance(nodo, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                if not nodo.name.startswith("_") and ast.get_docstring(nodo) is None:
                    faltantes.append(f"{ruta.relative_to(RAIZ)}:{nodo.lineno}: {nodo.name}")

    assert not faltantes, "Definiciones públicas sin docstring:\n" + "\n".join(faltantes)
