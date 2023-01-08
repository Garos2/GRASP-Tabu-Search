import random
import numpy as np
from Clases.Solucion import Solucion


def busqueda(solucion: Solucion):
    sale, entra, diferencia = mejor(solucion)
    # sale, entra, diferencia = primero(solucion)
    while diferencia > 0:
        sale, entra, diferencia = mejor(solucion)
        # sale, entra, diferencia = primero(solucion)
        solucion.cambiarNodos(sale, entra, diferencia=diferencia)

    return solucion


def mejor(solucion: Solucion):
    nSale, peorSalida = solucion.contribucionMenorDentro()
    nEntra, mejorEntrada = solucion.contribucionMasGrandeFuera(nSale)

    return nSale, nEntra, mejorEntrada - peorSalida


def primero(solucion: Solucion):
    np.random.shuffle(solucion.nodos)
    for nSale in solucion.nodos:
        nEntra, diferencia = solucion.primerCambioNodo(nSale)

        if diferencia > 0:
            return nSale, nEntra, diferencia

    return nSale, nEntra, diferencia
