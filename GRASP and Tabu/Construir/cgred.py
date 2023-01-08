import numpy as np
from Clases.Instancia import Instancia
from Clases.Solucion import Solucion


def construir(instancia: Instancia):
    solucion = Solucion(instancia)

    nodo1, nodo2, contribucion = masGrandes(solucion)
    solucion.inicializarNodo(0, nodo1, 0)
    solucion.inicializarNodo(1, nodo2, contribucion)

    for posicion in range(instancia.m - 2):
        entra, contribucion = solucion.contribucionMasGrandeFuera()
        solucion.inicializarNodo(posicion + 2, entra, contribucion)

    return solucion


def masGrandes(solucion: Solucion):
    matriz = solucion.instancia.distancias

    fila, columna = np.unravel_index(np.argmax(matriz, axis=None), matriz.shape)
    contribucion = matriz[fila, columna]

    return fila, columna, contribucion
