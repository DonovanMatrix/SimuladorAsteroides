
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


def detectar_colisiones_paralelo(nave, asteroides, num_procesos=None):
    asteroides = tuple(asteroides)

    if not asteroides:
        return []

    if num_procesos is not None and num_procesos <= 0:
        raise ValueError("El número de procesos debe ser positivo")

    if num_procesos == 1:
        return procesar_grupo((nave, asteroides))

    cantidad_procesos = num_procesos or 2
    cantidad_procesos = min(cantidad_procesos, len(asteroides))

    tamano_grupo = (
        len(asteroides) + cantidad_procesos - 1
    ) // cantidad_procesos

    grupos = [
        asteroides[i:i + tamano_grupo]
        for i in range(0, len(asteroides), tamano_grupo)
    ]

    tareas = [(nave, grupo) for grupo in grupos]

    with ProcessPoolExecutor(
        max_workers=cantidad_procesos
    ) as executor:
        resultados = executor.map(procesar_grupo, tareas)

    return [
        identificador
        for grupo in resultados
        for identificador in grupo
    ]
