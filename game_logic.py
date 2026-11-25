import math


def detectar_colision(pos1, radio1, pos2, radio2):
    distancia = math.sqrt(
        (pos2[0] - pos1[0]) ** 2 +
        (pos2[1] - pos1[1]) ** 2
    )

    return distancia <= radio1 + radio2