import numpy as np


def initInstancia(ruta):
    instancia = {
        "n": 500,
        "m": 25,
        "distancias": [],
    }
    # [line.strip() for line in open("cosa.txt", "r")]
    with open(ruta, "r") as fichero:
        instancia["distancias"] = np.zeros((instancia["n"], instancia["n"]))
        # for line in lines:
        #     line = line.strip()
        #     for el in line:
        #         if re.match(val, el):
        i = 0
        for line in fichero:
            line = line.strip("ï»¿")
            instancia["distancias"][i] = np.array(line.split(";"))

            i += 1

    return instancia
