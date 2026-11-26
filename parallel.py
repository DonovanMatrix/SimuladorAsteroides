
from concurrent.futures import ProcessPoolExecutor
from game_logic import detectar_colision


def procesar_grupo(datos):
    nave, asteroides = datos

    resultados = []

    for asteroide in asteroides:
        colision = detectar_colision(
            (nave.x, nave.y),
            nave.radio,
            (asteroide.x, asteroide.y),
            asteroide.radio
        )

        if colision:
            resultados.append(asteroide.id)

    return resultados


class ProcesadorParalelo:
    
    def __init__(self, num_procesos=4):
        if num_procesos <= 0:
            raise ValueError("El número de procesos debe ser positivo")

        self.num_procesos = num_procesos
        self.executor = ProcessPoolExecutor(
            max_workers=num_procesos
        )

    def detectar_colisiones(self, nave, asteroides):
        asteroides = tuple(asteroides)

        if not asteroides:
            return []

        cantidad_procesos = min(
            self.num_procesos,
            len(asteroides)
        )

        tamano_grupo = (
            len(asteroides) + cantidad_procesos - 1
        ) // cantidad_procesos

        grupos = [
            asteroides[i:i + tamano_grupo]
            for i in range(0, len(asteroides), tamano_grupo)
        ]

        tareas = [
            (nave, grupo)
            for grupo in grupos
        ]

        resultados = self.executor.map(
            procesar_grupo,
            tareas
        )

        return [
            identificador
            for grupo in resultados
            for identificador in grupo
        ]

    def cerrar(self):
        self.executor.shutdown(wait=True)

    def __enter__(self):
        return self

    def __exit__(self, tipo, valor, traceback):
        self.cerrar()

def detectar_colisiones_paralelo(
    nave,
    asteroides,
    num_procesos=None
):
    procesos = num_procesos or 4

    with ProcesadorParalelo(procesos) as procesador:
        return procesador.detectar_colisiones(nave, asteroides)
