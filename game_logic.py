
import math
from dataclasses import replace


def detectar_colision(pos1, radio1, pos2, radio2):
    distancia = math.sqrt(
        (pos2[0] - pos1[0]) ** 2 +
        (pos2[1] - pos1[1]) ** 2
    )

    return distancia <= radio1 + radio2


def actualizar_asteroides(asteroides, delta_tiempo, ancho, alto):
    if ancho <= 0 or alto <= 0:
        raise ValueError("Las dimensiones deben ser positivas")

    if delta_tiempo < 0:
        raise ValueError("El tiempo no puede ser negativo")

    nuevos_asteroides = []

    for asteroide in asteroides:
        nueva_x = (
            asteroide.x + asteroide.velocidad_x * delta_tiempo
        ) % ancho

        nueva_y = (
            asteroide.y + asteroide.velocidad_y * delta_tiempo
        ) % alto

        nuevo = replace(
            asteroide,
            x=nueva_x,
            y=nueva_y
        )

        nuevos_asteroides.append(nuevo)

    return tuple(nuevos_asteroides)


def detectar_colisiones_nave(nave, asteroides):
    colisiones = []

    for asteroide in asteroides:
        hay_colision = detectar_colision(
            (nave.x, nave.y),
            nave.radio,
            (asteroide.x, asteroide.y),
            asteroide.radio
        )

        if hay_colision:
            colisiones.append(asteroide.id)

    return tuple(colisiones)
