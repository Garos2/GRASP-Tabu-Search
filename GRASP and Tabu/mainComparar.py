import os, time
import numpy as np

from Mejorar import TabuSearch, grasp
from Clases.Solucion import Solucion
from Clases.Instancia import Instancia


def main():
    alfa = 0.2

    tenencia = 15
    beta = 0.3
    gamma = 0.2

    nInstancias = 8

    tiempos = 60 * np.array([0.5, 1, 2, 5, 10, 15])
    tiempos = 60 * np.array([1, 15])

    tablaGrasp = np.zeros((nInstancias, tiempos.size), dtype=int)
    tablaTabu = np.zeros((nInstancias, tiempos.size), dtype=int)

    for indice, tiempo in zip(range(tiempos.size), tiempos):
        objetivosGrasp = ejecutarDirectorioGrasp(alfa=alfa, tiempoMax=tiempo)
        objetivosTabu = ejecutarDirectorioTabu(
            tenencia=tenencia, mixtoSalir=beta, mixtoEntrar=gamma, tiempoMax=tiempo
        )
        print(f"Objetivos grasp = {tiempo}: {objetivosGrasp}")
        print(f"Objetivos tabu = {tiempo}: {objetivosTabu}")
        tablaGrasp[:, indice] = objetivosGrasp
        tablaTabu[:, indice] = objetivosTabu

    print(tablaGrasp)
    print(tablaTabu)

    separador = ";"
    with open(f"Comprar Grasp.csv", "w") as resultados:
        resultados.write(separador.join(str(tiempo) for tiempo in tiempos) + "\n")

        for fila in range(nInstancias):
            resultados.write(
                separador.join(str(valor) for valor in tablaGrasp[fila, :]) + "\n"
            )

    with open(f"Comprar Tabu.csv", "w") as resultados:
        resultados.write(separador.join(str(tiempo) for tiempo in tiempos) + "\n")

        for fila in range(nInstancias):
            resultados.write(
                separador.join(str(valor) for valor in tablaTabu[fila, :]) + "\n"
            )


def ejecutarDirectorioGrasp(alfa: float = 0.5, tiempoMax: float = 1):
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


def ejecutarDirectorioTabu(
    tenencia: int = 10,
    mixtoSalir: float = 0.5,
    mixtoEntrar: float = 0.5,
    tiempoMax: float = 1,
):
    directorio = "Instancias"

    with os.scandir(directorio) as archivos:
        archivos = [
            archivo.name
            for archivo in archivos
            if archivo.is_file() and archivo.name.endswith(".csv")
        ]
        objetivos = []

    with open("Resultados TS" + str(tenencia) + ".csv", "w") as resultados:
        for fichero in archivos:
            ruta = directorio + "/" + fichero
            print("Resolviendo " + fichero + ": ", end="")

            instancia = Instancia()
            instancia.rellenar(ruta)
            resultados.write(fichero + "\t")

            inicio = time.time()
            solucion = TabuSearch.TabuMixto(
                instancia,
                tiempoMax=tiempoMax,
                tenencia=tenencia,
                mixtoSalir=mixtoSalir,
                mixtoEntrar=mixtoEntrar,
            )
            tiempo = time.time() - inicio

            objetivo = int(solucion.objetivo)
            objetivos.append(objetivo)
            print(str(objetivo) + "\t" + str(tiempo))
            resultados.write(str(objetivo) + "\t" + str(tiempo) + "\n")

    return objetivos


if __name__ == "__main__":
    main()
