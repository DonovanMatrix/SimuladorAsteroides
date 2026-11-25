
from dataclasses import FrozenInstanceError

from models import Asteroide, Nave, GameState


asteroide = Asteroide(
    id=1,
    x=100.0,
    y=150.0,
    velocidad_x=2.0,
    velocidad_y=3.0,
    radio=15.0
)

nave = Nave(
    x=500.0,
    y=350.0,
    radio=20.0,
    velocidad=5.0
)

estado = GameState(
    nave=nave,
    asteroides=(asteroide,),
    puntuacion=0,
    jugando=True,
    tiempo=0.0,
    ancho=1000,
    alto=700
)

print("Estado inicial:")
print(estado)

print("\nProbando inmutabilidad:")

try:
    asteroide.x = 200.0
except FrozenInstanceError:
    print("Correcto: no se puede modificar el asteroide.")

try:
    estado.puntuacion = 100
except FrozenInstanceError:
    print("Correcto: no se puede modificar GameState.")

print("\nPruebas finalizadas correctamente.")   