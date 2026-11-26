
import time
import random
import os

from models import Nave, Asteroide
from parallel import ProcesadorParalelo
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
    cantidades=(1000, 3000, 5000, 10000, 50000, 100000, 250000),
    num_procesos=4,
    repeticiones=10
):
    nave = Nave(0, 0, 10, 2)

    print("\n===== BENCHMARK DE ASTEROIDES =====")
    print(f"Nucleos logicos disponibles: {os.cpu_count()}")
    print(f"Workers configurados: {num_procesos}")
    print(f"Repeticiones: {repeticiones}")

    print("\nRESULTADOS DE RENDIMIENTO")
    print("-" * 75)
    print(
        f"{'Entidades':<15}"
        f"{'Secuencial FPS':<20}"
        f"{'Paralelo FPS':<20}"
        f"{'Aceleracion':<15}"
    )
    print("-" * 75)

    with ProcesadorParalelo(num_procesos) as procesador:

        for cantidad in cantidades:
            asteroides = generar_asteroides(cantidad)

            # Calentamiento inicial del procesamiento paralelo
            procesador.detectar_colisiones(nave, asteroides)

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

                resultado_paralelo = procesador.detectar_colisiones(
                    nave, asteroides
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

            fps_secuencial = 1 / promedio_secuencial
            fps_paralelo = 1 / promedio_paralelo

            aceleracion = promedio_secuencial / promedio_paralelo

            print(
                f"{cantidad:<15}"
                f"{fps_secuencial:<20.2f}"
                f"{fps_paralelo:<20.2f}"
                f"{aceleracion:.2f}x"
            )

            print(
                f"  Tiempo secuencial: {promedio_secuencial:.6f} segundos"
            )
            print(
                f"  Tiempo paralelo:   {promedio_paralelo:.6f} segundos"
            )

    print("-" * 75)
    print("Todas las comparaciones obtuvieron resultados equivalentes.")
    print("FPS calculados como 1 / tiempo promedio de procesamiento.")


if __name__ == "__main__":
    ejecutar_benchmark()
