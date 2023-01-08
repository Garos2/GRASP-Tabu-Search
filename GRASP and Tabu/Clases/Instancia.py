import numpy as np


class Instancia:
    def __init__(self):
        self.n = 500
        self.m = 25
        self.distancias = np.empty([self.n, self.n], dtype=int)

    def rellenar(self, ruta: str):
        with open(ruta, "r") as fichero:
            indice = 0
            for line in fichero:
                line = line.strip("ï»¿")
                self.distancias[indice] = np.array(line.split(";"))

                indice += 1

    def __str__(self):
        return f"n: {self.n}, m: {self.m}, distancias: {self.distancias}"
