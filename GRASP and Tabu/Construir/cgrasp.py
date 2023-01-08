import numpy as np
import random
from Clases.Solucion import Solucion
from Clases.Instancia import Instancia


def construir(instancia: Instancia, alfa: float):
    solucion = Solucion(instancia)

    nodo1 = random.randint(0, instancia.n - 1)
    solucion.inicializarNodo(0, nodo1)

    listaDeCandidatos = inicializarListaDeCandidatos(solucion.instancia.n)

    for posicion in range(instancia.m):
        entra, contribucion = encontrarRestringido(listaDeCandidatos, alfa)
        solucion.inicializarNodo(posicion, entra, contribucion)
        actualizarListaDeCandidatos(solucion, listaDeCandidatos, entra)

    return solucion


def inicializarListaDeCandidatos(n: int):
    return np.vstack((np.arange(n), np.zeros(n)))


def actualizarListaDeCandidatos(
    solucion: Solucion, listaDeCandidatos: list, entra: int = -1
):
    for nodo in range(solucion.instancia.n):
        if solucion.estaEnSolucion(nodo):
            listaDeCandidatos[1, nodo] = 0
            continue

        if entra == -1:
            listaDeCandidatos[1, nodo] = solucion.computarContribucion(nodo)
        else:
            listaDeCandidatos[1, nodo] += solucion.instancia.distancias[entra, nodo]


def encontrarRestringido(listaDeCandidatos: list, alfa: float):
    contribuciones = listaDeCandidatos[1, :]
    tolerancia = np.max(contribuciones) - alfa * np.ptp(contribuciones)

    entra = random.randint(0, len(contribuciones) - 1)
    while contribuciones[entra] < tolerancia:
        entra = random.randint(0, len(contribuciones) - 1)

    return entra, listaDeCandidatos[1, entra]
