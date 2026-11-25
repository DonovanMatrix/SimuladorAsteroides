
import pygame
import random

from models import Asteroide, Nave
from game_logic import actualizar_asteroides, detectar_colisiones_nave
from renderer import Renderer


def main():
    pygame.init()

    ancho = 1000
    alto = 700

    pantalla = pygame.display.set_mode((ancho, alto))
    pygame.display.set_caption("Simulador de Asteroides")

    reloj = pygame.time.Clock()
    renderer = Renderer(pantalla)

    nave = Nave(
        x=ancho / 2,
        y=alto / 2,
        radio=20,
        velocidad=300
    )

    # Crear asteroides evitando que aparezcan cerca de la nave
    asteroides_lista = []

    for i in range(15):
        while True:
            x = random.randint(30, ancho - 30)
            y = random.randint(30, alto - 30)
            radio = random.randint(12, 30)

            distancia = (
                (x - nave.x) ** 2 +
                (y - nave.y) ** 2
            ) ** 0.5

            if distancia > nave.radio + radio + 50:
                break

        asteroides_lista.append(
            Asteroide(
                id=i,
                x=x,
                y=y,
                velocidad_x=random.randint(-100, 100),
                velocidad_y=random.randint(-100, 100),
                radio=radio
            )
        )

    asteroides = tuple(asteroides_lista)

    puntuacion = 0
    jugando = True

    while jugando:
        delta_tiempo = reloj.tick(60) / 1000

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                jugando = False

        teclas = pygame.key.get_pressed()

        dx = 0
        dy = 0

        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            dx -= 1
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            dx += 1
        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            dy -= 1
        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            dy += 1

        longitud = (dx ** 2 + dy ** 2) ** 0.5

        if longitud > 0:
            dx /= longitud
            dy /= longitud

        nueva_x = max(
            nave.radio,
            min(ancho - nave.radio,
                nave.x + dx * nave.velocidad * delta_tiempo)
        )

        nueva_y = max(
            nave.radio,
            min(alto - nave.radio,
                nave.y + dy * nave.velocidad * delta_tiempo)
        )

        nave = Nave(
            nueva_x,
            nueva_y,
            nave.radio,
            nave.velocidad
        )

        asteroides = actualizar_asteroides(
            asteroides,
            delta_tiempo,
            ancho,
            alto
        )

        colisiones = detectar_colisiones_nave(nave, asteroides)
        if colisiones:
            jugando = False

        renderer.dibujar_fondo()
        renderer.dibujar_asteroides(asteroides)
        renderer.dibujar_nave(nave)
        renderer.dibujar_puntuacion(puntuacion)
        renderer.actualizar_pantalla()

    fuente = pygame.font.SysFont("Arial", 60)
    texto = fuente.render("GAME OVER", True, (255, 50, 50))

    rectangulo = texto.get_rect(
        center=(ancho // 2, alto // 2)
    )

    pantalla.blit(texto, rectangulo)
    pygame.display.flip()

    pygame.time.wait(2000)
    pygame.quit()


if __name__ == "__main__":
    main()
