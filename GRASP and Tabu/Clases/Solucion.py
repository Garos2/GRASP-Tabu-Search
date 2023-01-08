from Clases.Instancia import Instancia
import numpy as np


class Solucion:
    def __init__(self, instancia: Instancia):
        self.nodos = -np.ones(instancia.m, dtype=int)
        self.binario = 0b0
        self.objetivo = 0
        self.instancia = instancia

    def __str__(self) -> str:
        return f"Nodos: {self.nodos}\nObjetivo: {int(self.objetivo)}"

    def copia(self):
        copia = Solucion(self.instancia)

        copia.nodos = self.nodos.copy()
        copia.objetivo = self.objetivo
        copia.instancia = self.instancia

        return copia

    def anadirNodo(self, nodo: int, contribucion: int = -1):
        if contribucion == -1:
            contribucion = self.computarContribucion(self, nodo)

        self.objetivo += contribucion
        self.nodos.add(nodo)
        # self.binario += 1 << nodo

    def quitarNodo(self, nodo: int, contribucion: int = -1):
        if contribucion == -1:
            contribucion = self.computarContribucion(self, nodo)

        self.objetivo -= contribucion
        self.nodos.remove(nodo)
        # self.binario -= 1 << nodo

    def computarContribucion(self, nodo: int, sinElNodo: int = -1):
        contribucion = 0

        if self.estaEnSolucion(nodo):
            return 0

        for nodos in self.nodos:
            if nodos >= 0:
                contribucion += self.instancia.distancias[nodo, nodos]

        if sinElNodo != -1:
            # contribucion -= self.computarContribucionDentro(sinElNodo)
            contribucion -= self.instancia.distancias[nodo][sinElNodo]

        return contribucion

    def computarContribucionDentro(self, nodo: int):
        contribucion = 0
        for nodos in self.nodos:
            if nodos >= 0:
                contribucion += self.instancia.distancias[nodo, nodos]
        return contribucion

    def esFactible(self):
        return len(self.nodos) == self.instancia.m

    def estaEnSolucion(self, nodo: int):
        return nodo in self.nodos

    def inicializarNodo(self, posicion: int, nodo: int, contribucion: int = -1):
        if contribucion == -1:
            contribucion = self.computarContribucion(nodo)

        self.objetivo += contribucion
        self.nodos[posicion] = nodo
        self.binario += 1 << nodo

    def evaluarObjetivo(self):
        objetivo = 0

        for nodo1 in self.nodos:
            for nodo2 in self.nodos:
                if nodo1 < nodo2:
                    objetivo += self.instancia.distancias[nodo1][nodo2]

        return objetivo

    def cambiarNodos(
        self, nSale: int, nEntra: int, iSale: int = -1, diferencia: int = -1
    ):
        if iSale == -1:
            iSale = next(
                (indice for indice, nodo in enumerate(self.nodos) if nodo == nSale), -1
            )

        if diferencia == -1:
            diferencia = self.computarContribucion(
                nEntra, nSale
            ) - self.computarContribucionDentro(nSale)
        self.objetivo += diferencia

        self.nodos[iSale] = nEntra
        # self.binario -= 1 << nSale
        # self.binario += 1 << nEntra

    def contribucionMasGrande(self, sinElNodo: int = -1):
        matriz = np.zeros(self.instancia.n)
        for nodo in range(self.instancia.n):
            matriz[nodo] = self.computarContribucion(nodo, sinElNodo)
        nodo = np.argmax(matriz)

        return nodo, matriz[nodo]

    def contribucionMasGrandeFuera(self, sinElNodo: int = -1):
        matriz = np.zeros(self.instancia.n)
        for nodo in range(self.instancia.n):
            matriz[nodo] = self.computarContribucion(nodo, sinElNodo)
        nodo = np.argmax(matriz)

        return nodo, matriz[nodo]

    def contribucionMenorDentro(self):
        # Solo funciona si solución llena
        assert self.esFactible

        matriz = np.zeros(self.instancia.m)
        indice = 0
        for nodo in self.nodos:
            matriz[indice] = self.computarContribucionDentro(nodo)
            indice += 1
        indice = np.argmin(matriz)
        nodo = self.nodos[indice]

        return nodo, matriz[indice]

    def primerCambioNodo(self, nSale: int):
        for nEntra in range(self.instancia.n):
            contribucion = self.computarContribucion(nEntra, nSale)
            diferencia = contribucion - self.computarContribucionDentro(nSale)

            if diferencia > 0:
                return nEntra, diferencia

        return nEntra, diferencia

    def encontrarIndiceDelNodo(self, nodo: int):
        assert self.esFactible

        return next(
            (indice for indice, nodos in enumerate(self.nodos) if nodos == nodo), -1
        )

    def computarDiferencia(self, nodoSale: int, nodoEntra: int):
        contribucionSale = self.computarContribucionDentro(nodoSale)
        contribucionEntra = self.computarContribucion(nodoEntra, sinElNodo=nodoSale)

        return contribucionEntra - contribucionSale


class SolucionTabu(Solucion):
    def __init__(self, instancia: Instancia, tenencia: int = 10):
        super().__init__(instancia)

        self.tenencia = tenencia
        self.listaTabu = -np.ones(self.tenencia, dtype=int)

    def volcar(self, solucion: Solucion):
        self.nodos = solucion.nodos
        self.objetivo = solucion.objetivo
        self.instancia = solucion.instancia

    def copia(self):
        copia = SolucionTabu(self.instancia)

        copia.volcar(super().copia())
        copia.tenencia = self.tenencia
        copia.listaTabu = self.listaTabu.copy()

        return copia
