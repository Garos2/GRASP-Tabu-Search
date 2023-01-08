import time
from Clases.Solucion import Solucion
from Clases.Instancia import Instancia
from Construir import cgrasp
from Mejorar import LocalSearch


def grasp(instancia: Instancia, tiempoMax: float, alfa: float):
    inicio = time.time()
    mejorSolucion = None
    while time.time() - inicio < tiempoMax:
        # print("IT " + str(i + 1))
        solucion = cgrasp.construir(instancia, alfa)
        # print("\tC: "+str(sol['of']))
        # lsfirstimprove.improve(sol)
        LocalSearch.busqueda(solucion)
        # print("\tLS: " + str(sol['of']))
        if mejorSolucion is None or mejorSolucion.objetivo < solucion.objetivo:
            mejorSolucion = solucion.copia()
        # print("\tB: " + str(best['of']))
    # print(time.time() - inicio)
    return mejorSolucion
