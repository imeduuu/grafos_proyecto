from src.algoritmos.corte_minimo import corte_minimo
from src.algoritmos.flujo_maximo import maximo_caminos_disjuntos
from src.verificacion.verificador import (
    verificar_corte_desconecta,
    verificar_sin_arcos_compartidos,
)

def test_dos_caminos_disjuntos_figura1(grafo_figura1):
    cantidad, caminos = maximo_caminos_disjuntos(grafo_figura1, "s", "t")
    assert cantidad == 2
    assert verificar_sin_arcos_compartidos(caminos)

def test_corte_coincide_con_flujo(grafo_figura1):
    cantidad, _ = maximo_caminos_disjuntos(grafo_figura1, "s", "t")
    corte = corte_minimo(grafo_figura1, "s", "t")
    assert len(corte) == cantidad
    assert verificar_corte_desconecta(grafo_figura1, corte, "s", "t")
