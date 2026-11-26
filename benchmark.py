
import time
import random

from models import Nave, Asteroide
from parallel import detectar_colisiones_paralelo
from game_logic import detectar_colision


def generar_asteroides(cantidad):
    generador = random.Random(42)

    return tuple(
        Asteroide(
            id=i,
            x=generador.uniform(-1000, 1000),
            y=generador.uniform(-1000, 1000),
            velocidad_x=generador.uniform(-5, 5),
            velocidad_y=generador.uniform(-5, 5),
            radio=generador.uniform(2, 10)
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


def ejecutar_benchmark(
    cantidades=(1000, 10000, 50000, 100000),
    num_procesos=4,
    repeticiones=3
):
    if num_procesos <= 0:
        raise ValueError("El número de procesos debe ser positivo")

    if repeticiones <= 0:
        raise ValueError("El número de repeticiones debe ser positivo")

    nave = Nave(0, 0, 10, 2)

    print("\n===== BENCHMARK DE ASTEROIDES =====")
    print(f"Procesos utilizados: {num_procesos}")
    print(f"Repeticiones: {repeticiones}")

    for cantidad in cantidades:
        asteroides = generar_asteroides(cantidad)

        tiempos_secuenciales = []
        tiempos_paralelos = []

        for _ in range(repeticiones):

            inicio = time.perf_counter()

            resultado_secuencial = detectar_colisiones_secuencial(
                nave, asteroides
            )

            tiempo_secuencial = time.perf_counter() - inicio
            tiempos_secuenciales.append(tiempo_secuencial)

            inicio = time.perf_counter()

            resultado_paralelo = detectar_colisiones_paralelo(
                nave, asteroides, num_procesos
            )

            tiempo_paralelo = time.perf_counter() - inicio
            tiempos_paralelos.append(tiempo_paralelo)

            if resultado_secuencial != resultado_paralelo:
                raise AssertionError(
                    "Los resultados secuenciales y paralelos no coinciden"
                )

        promedio_secuencial = (
            sum(tiempos_secuenciales) / repeticiones
        )

        promedio_paralelo = (
            sum(tiempos_paralelos) / repeticiones
        )

        aceleracion = (
            promedio_secuencial / promedio_paralelo
            if promedio_paralelo > 0 else 0
        )

        print(f"\nAsteroides: {cantidad}")
        print(f"Secuencial: {promedio_secuencial:.6f} segundos")
        print(f"Paralelo:   {promedio_paralelo:.6f} segundos")
        print(f"Aceleración: {aceleracion:.2f}x")


if __name__ == "__main__":
    ejecutar_benchmark()
