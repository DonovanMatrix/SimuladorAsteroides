
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Asteroide:
    id: int
    x: float
    y: float
    velocidad_x: float
    velocidad_y: float
    radio: float


@dataclass(frozen=True, slots=True)
class Nave:
    x: float
    y: float
    radio: float
    velocidad: float


@dataclass(frozen=True, slots=True)
class GameState:
    nave: Nave
    asteroides: tuple[Asteroide, ...]
    puntuacion: int
    jugando: bool
    tiempo: float
    ancho: int
    alto: int
