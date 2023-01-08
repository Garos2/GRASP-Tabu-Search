import os
import random
import numpy as np

from Clases.Solucion import Solucion
from Clases.Instancia import Instancia
from Construir import cgred, cgrasp
from Mejorar import LocalSearch, grasp
import time


def main():
    alfas = np.array([0.2, 0.4, 0.6, 0.8])
    nInstancias = 8
    tiempoMax = 240

    tabla = np.zeros((nInstancias, alfas.size), dtype=int)

    for indice, alfa in zip(range(alfas.size), alfas):
        objetivosAlfa = ejectuarDirectorio(alfa, tiempoMax)
        print(f"Objetivos alfa = {alfa}: {objetivosAlfa}")
        tabla[:, indice] = objetivosAlfa

    print(tabla)

    separador = ";"
    with open("Resultados Grasp.csv", "w") as resultados:
        resultados.write(separador.join(str(alfa) for alfa in alfas) + "\n")

        for fila in range(nInstancias):
            resultados.write(
                separador.join(str(valor) for valor in tabla[fila, :]) + "\n"
            )


def ejecutarInstancia(alfa: float = 0.5, tiempoMax: float = 10):
    random.seed(1309)
    ruta = "Instancias\MariaJesus.csv"
    instancia = Instancia()
    instancia = Instancia.rellenar(ruta)

    solucion = grasp.execute(instancia, tiempoMax, alfa)
    print(solucion)


def ejectuarDirectorio(alfa: float = 0.5, tiempoMax: float = 10):
    directorio = "Instancias"

    with os.scandir(directorio) as archivos:
        archivos = [
            archivo.name
            for archivo in archivos
            if archivo.is_file() and archivo.name.endswith(".csv")
        ]
        objetivos = []

    with open("Resultados" + str(alfa) + ".csv", "w") as resultados:
        for fichero in archivos:
            ruta = directorio + "/" + fichero
            print("Resolviendo " + fichero + ": ", end="")

            instancia = Instancia()
            instancia.rellenar(ruta)
            resultados.write(fichero + "\t")

            inicio = time.time()
            solucion = grasp.grasp(instancia, tiempoMax, alfa)
            tiempo = time.time() - inicio

            objetivo = int(solucion.objetivo)
            objetivos.append(objetivo)
            print(str(objetivo) + "\t" + str(tiempo))
            resultados.write(str(objetivo) + "\t" + str(tiempo) + "\n")

    return objetivos


if __name__ == "__main__":
    main()
