import random, time
import numpy as np
from Clases.Solucion import Solucion, SolucionTabu
from Clases.Instancia import Instancia
from Mejorar import LocalSearch
from Construir import cgred


def TabuMixto(
    instancia: Instancia,
    tiempoMax: float = 1,
    tenencia: int = 10,
    mixtoSalir: int = 0.5,
    mixtoEntrar: int = 0.5,
):
    inicio = time.time()
    mejorSolucion = None

    solucionGreedy = cgred.construir(instancia)
    solucion = SolucionTabu(instancia, tenencia)
    solucion.volcar(solucionGreedy)
    # solucion = solucionGreedy.copia()

    indiceTabu = 0
    indiceSolucion = 0
    bin = 1
    while time.time() - inicio < tiempoMax:

        np.random.shuffle(solucion.nodos)
        listaSalida = np.concatenate(
            [solucion.nodos[indiceSolucion:], solucion.nodos[:indiceSolucion]]
        )
        listaSalida = parteDeLista(listaSalida, porcentaje=mixtoSalir)

        listaEntrada = np.arange(solucion.instancia.n)
        np.random.shuffle(listaEntrada)
        listaEntrada = parteDeLista(listaEntrada, porcentaje=mixtoEntrar)

        nodoSale, contrSale, nodoEntra, contrEntra, diferencia = encontrarCambioMixto(
            solucion, listaSalida, listaEntrada=listaEntrada
        )

        # nodoSale, nodoEntra, diferencia = encontrarCambioMixtoV2(
        #     solucion, listaSalida, listaEntrada=listaEntrada
        # )

        indiceSolucion = solucion.encontrarIndiceDelNodo(nodoSale)
        solucion.cambiarNodos(
            nodoSale, nodoEntra, diferencia=diferencia, iSale=indiceSolucion
        )

        if diferencia <= 0 and bin == 1:
            bin = 0
            solucion.listaTabu[indiceTabu] = nodoSale

            # solucionAMejorar = solucion.copia()
            # LocalSearch.busqueda(solucionAMejorar)
            # mejorSolucion = chequearMejor(
            #     mejorSolucion=mejorSolucion, solucion=solucionAMejorar
            # )

            indiceTabu += 1
            indiceTabu %= tenencia
        else:
            bin = 1
        # print(solucion.objetivo)

        mejorSolucion = chequearMejor(mejorSolucion=mejorSolucion, solucion=solucion)

        indiceSolucion += 1
        indiceSolucion %= solucion.instancia.m

    return mejorSolucion


def encontrarCambioMixto(
    solucion: SolucionTabu, listaSalida: np.ndarray, listaEntrada: np.ndarray
):

    matrizPeores = np.zeros(listaSalida.size)

    for indice, nodo in enumerate(listaSalida):
        matrizPeores[indice] = solucion.computarContribucionDentro(nodo)

    indice = np.argmin(matrizPeores)
    nodo = listaSalida[indice]

    peorSalida, contribucionPeorSalida = nodo, matrizPeores[indice]

    matrizMejores = np.zeros(listaEntrada.size)

    for indice, nodo in enumerate(listaEntrada):
        if nodo not in solucion.listaTabu and nodo not in solucion.nodos:
            matrizMejores[indice] = solucion.computarContribucion(
                nodo, sinElNodo=peorSalida
            )

    indice = np.argmax(matrizMejores)
    nodo = listaEntrada[indice]

    mejorEntrada, contribucionMejorEntrada = nodo, matrizMejores[indice]

    return (
        peorSalida,
        contribucionPeorSalida,
        mejorEntrada,
        contribucionMejorEntrada,
        contribucionMejorEntrada - contribucionPeorSalida,
    )


def parteDeLista(lista: np.ndarray, porcentaje: float):
    return lista[: int(np.floor(lista.size * porcentaje)) + 1]


def encontrarCambioMixtoV2(
    solucion: SolucionTabu, listaSalida: np.ndarray, listaEntrada: np.ndarray
):

    matrizDiferencias = (-1 << 10) * np.ones([listaSalida.size, listaEntrada.size])

    for indiceSale, nodoSale in enumerate(listaSalida):
        for indiceEntra, nodoEntra in enumerate(listaEntrada):
            if nodoEntra not in solucion.listaTabu and nodoEntra not in solucion.nodos:
                matrizDiferencias[
                    indiceSale, indiceEntra
                ] = solucion.computarDiferencia(nodoSale, nodoEntra)

    indiceSale, indiceEntra = np.unravel_index(
        np.argmax(matrizDiferencias, axis=None), matrizDiferencias.shape
    )
    peorSalida = listaSalida[indiceSale]
    mejorEntrada = listaEntrada[indiceEntra]
    diferencia = matrizDiferencias[indiceSale, indiceEntra]

    return (peorSalida, mejorEntrada, diferencia)


def chequearMejor(mejorSolucion: SolucionTabu, solucion: SolucionTabu):
    if mejorSolucion is None or mejorSolucion.objetivo < solucion.objetivo:
        mejorSolucion = solucion.copia()
        # print(mejorSolucion)

    return mejorSolucion
