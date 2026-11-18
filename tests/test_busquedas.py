from src.algoritmos.busqueda_anchura import camino_minimo

def test_camino_minimo_figura1(grafo_figura1):
    camino, longitud = camino_minimo(grafo_figura1, "s", "t")
    assert longitud == 4
    assert camino[0] == "s" and camino[-1] == "t"

def test_sin_camino_no_da_longitud(grafo_figura1):
    grafo_figura1.bloquear_arco("E", "t")
    grafo_figura1.bloquear_arco("G", "t")
    camino, longitud = camino_minimo(grafo_figura1, "s", "t")
    assert camino is None and longitud is None
