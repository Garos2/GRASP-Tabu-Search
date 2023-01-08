import numpy as np


def initSolucion(instancia):
    solucion = {
        "nodos": set(),
        "binario": 0b0,
        "objetivo": 0,
        "instancia": instancia,
    }

    return solucion


def anadirNodo(solucion, nodo, contribucion=-1):
    if contribucion == -1:
        contribucion = computarContribucion(solucion, nodo)

    solucion["objetivo"] += contribucion
    solucion["nodos"].add(nodo)
    solucion["binario"] += 1 << nodo


def quitarNodo(solucion, nodo, contribucion=-1):
    if contribucion == -1:
        contribucion = computarContribucion(solucion, nodo)

    solucion["objetivo"] -= contribucion
    solucion["nodos"].remove(nodo)
    solucion["binario"] -= 1 << nodo


def computarContribucion(solucion, nodo):
    contribucion = 0

    for nodos in solucion["nodos"]:
        if nodos == nodo:
            continue
        contribucion += solucion["instancia"]["distancias"][nodo, nodos]

    return contribucion


def esFactible(solucion):
    return len(solucion["nodos"]) == solucion["instancia"]["m"]


def estaEnSolucion(solucion, nodo):
    binario = 1 << nodo
    return np.int(binario) & ~np.int(solucion["binario"]) == 0


def evaluarObjetivo(solucion):
    objetivo = 0

    for nodo1 in solucion["nodos"]:
        for nodo2 in solucion["nodos"]:
            if nodo1 < nodo2:
                objetivo += solucion["instancia"]["distancias"][nodo1][nodo2]

    return objetivo
