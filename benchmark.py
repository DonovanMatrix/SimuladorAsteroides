
import time
import random

from models import Nave, Asteroide
from parallel import detectar_colisiones_paralelo
from game_logic import detectar_colision


def generar_asteroides(cantidad):
    random.seed(42)

    return tuple(
        Asteroide(
            id=i,
            x=random.uniform(-1000, 1000),
            y=random.uniform(-1000, 1000),
            velocidad_x=random.uniform(-5, 5),
            velocidad_y=random.uniform(-5, 5),
            radio=random.uniform(2, 10)
        )
        for i in range(cantidad)
    )


def detectar_colisiones_secuencial(nave, asteroides):
    resultados = []

    for asteroide in asteroides:
        if detectar_colision(
            (nave.x, nave.y),
            nave.radio,
            (asteroide.x, asteroide.y),
            asteroide.radio
        ):
            resultados.append(asteroide.id)

    return resultados


def ejecutar_benchmark(cantidades=(1000, 3000, 5000),
                       num_procesos=4):

    nave = Nave(0, 0, 10, 2)

    print("\n===== BENCHMARK DE ASTEROIDES =====")

    for cantidad in cantidades:
        asteroides = generar_asteroides(cantidad)

        inicio = time.perf_counter()
        resultado_secuencial = detectar_colisiones_secuencial(
            nave, asteroides
        )
        tiempo_secuencial = time.perf_counter() - inicio

        inicio = time.perf_counter()
        resultado_paralelo = detectar_colisiones_paralelo(
            nave, asteroides, num_procesos
        )
        tiempo_paralelo = time.perf_counter() - inicio

        if resultado_secuencial != resultado_paralelo:
            raise AssertionError(
                "Los resultados secuenciales y paralelos no coinciden"
            )

        aceleracion = (
            tiempo_secuencial / tiempo_paralelo
            if tiempo_paralelo > 0 else 0
        )

        print(f"\nAsteroides: {cantidad}")
        print(f"Secuencial: {tiempo_secuencial:.6f} segundos")
        print(f"Paralelo:   {tiempo_paralelo:.6f} segundos")
        print(f"Aceleración: {aceleracion:.2f}x")


if __name__ == "__main__":
    ejecutar_benchmark()
