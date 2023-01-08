import os, time

import numpy as np

from Clases.Instancia import Instancia
from Mejorar import TabuSearch


def calibrarTenencias():
    tenencias = np.array([10, 13, 15, 20])
    nInstancias = 8
    tiempoMax = 61

    tabla = np.zeros((nInstancias, tenencias.size), dtype=int)

    for indice, tenencia in zip(range(tenencias.size), tenencias):
        objetivosTenencia = ejectuarDirectorio(tenencia, tiempoMax=tiempoMax)
        print(f"Objetivos tenencia = {tenencia}: {objetivosTenencia}")
        tabla[:, indice] = objetivosTenencia

    print(tabla)

    separador = ";"
    with open(f"Resultados TS 1s {tiempoMax}s 0.5e.csv", "w") as resultados:
        resultados.write(separador.join(str(tenencia) for tenencia in tenencias) + "\n")

        for fila in range(nInstancias):
            resultados.write(
                separador.join(str(valor) for valor in tabla[fila, :]) + "\n"
            )


def calibrarMixtoSalida():
    salidas = np.array([0.2, 0.3, 0.5, 0.7, 0.8, 0.9])
    nInstancias = 8
    tiempoMax = 3 * 60
    tenencia = 15

    tabla = np.zeros((nInstancias, salidas.size), dtype=int)

    for indice, salida in zip(range(salidas.size), salidas):
        objetivosSalida = ejectuarDirectorio(
            tenencia=tenencia, mixtoSalir=salida, tiempoMax=tiempoMax
        )
        print(f"Objetivos salida = {salida}: {objetivosSalida}")
        tabla[:, indice] = objetivosSalida

    print(tabla)

    separador = ";"
    with open(
        f"Resultados TS {tiempoMax}s t{tenencia}  Salidas 0.5e.csv", "w"
    ) as resultados:
        resultados.write(separador.join(str(salida) for salida in salidas) + "\n")

        for fila in range(nInstancias):
            resultados.write(
                separador.join(str(valor) for valor in tabla[fila, :]) + "\n"
            )


def calibrarMixtoEntrada():
    entradas = np.array([0.1, 0.15, 0.25])
    nInstancias = 8
    tiempoMax = 1 * 61
    tenencia = 15
    salida = 0.3

    tabla = np.zeros((nInstancias, entradas.size), dtype=int)

    for indice, entrada in zip(range(entradas.size), entradas):
        objetivosEntrada = ejectuarDirectorio(
            tenencia=tenencia,
            mixtoSalir=salida,
            mixtoEntrar=entrada,
            tiempoMax=tiempoMax,
        )
        print(f"Objetivos entrada = {entrada}: {objetivosEntrada}")
        tabla[:, indice] = objetivosEntrada

    print(tabla)

    separador = ";"
    with open(
        f"Resultados TS {tiempoMax}s t{tenencia}  S{salida} Entradas.csv", "w"
    ) as resultados:
        resultados.write(separador.join(str(entrada) for entrada in entradas) + "\n")

        for fila in range(nInstancias):
            resultados.write(
                separador.join(str(valor) for valor in tabla[fila, :]) + "\n"
            )


# ruta = "Instancias\Amparo.csv"

# inst = Instancia()
# inst.rellenar(ruta)

# solucion = TabuSearch.TabuMixto(inst, 240, tenencia=10, mixtoEntrar=0.3, mixtoSalir=0.5)
# print(solucion)


def ejectuarDirectorio(
    tenencia: int = 20,
    mixtoSalir: float = 0.5,
    mixtoEntrar: float = 0.5,
    tiempoMax: float = 10,
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
    calibrarTenencias()
    # calibrarMixtoSalida()
    # calibrarMixtoEntrada()
    pass
