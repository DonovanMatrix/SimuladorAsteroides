
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

    # Configuracion de proyectiles
    proyectiles = []
    velocidad_proyectil = 500
    radio_proyectil = 5

    fuente_game_over = pygame.font.SysFont("Arial", 60)

    while jugando:
        delta_tiempo = reloj.tick(60) / 1000

        # Procesar eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                jugando = False

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    proyectiles.append({
                        "x": nave.x,
                        "y": nave.y - nave.radio
                    })

        # Movimiento de la nave
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

        # Actualizar asteroides
        asteroides = actualizar_asteroides(
            asteroides,
            delta_tiempo,
            ancho,
            alto
        )

        # Mover proyectiles
        for proyectil in proyectiles:
            proyectil["y"] -= velocidad_proyectil * delta_tiempo

        # Eliminar proyectiles fuera de la pantalla
        proyectiles = [
            p for p in proyectiles
            if p["y"] + radio_proyectil > 0
        ]

        # Detectar impactos entre proyectiles y asteroides
        asteroides_lista = list(asteroides)
        proyectiles_restantes = []

        for proyectil in proyectiles:
            impacto = False

            for asteroide in asteroides_lista:
                distancia = (
                    (proyectil["x"] - asteroide.x) ** 2 +
                    (proyectil["y"] - asteroide.y) ** 2
                ) ** 0.5

                if distancia <= radio_proyectil + asteroide.radio:
                    asteroides_lista.remove(asteroide)
                    puntuacion += 10
                    impacto = True
                    break

            if not impacto:
                proyectiles_restantes.append(proyectil)

        proyectiles = proyectiles_restantes
        asteroides = tuple(asteroides_lista)

        # Detectar colision de la nave
        colisiones = detectar_colisiones_nave(nave, asteroides)

        if colisiones:
            jugando = False

        # Dibujar elementos
        renderer.dibujar_fondo()
        renderer.dibujar_asteroides(asteroides)
        renderer.dibujar_nave(nave)
        renderer.dibujar_puntuacion(puntuacion)

        # Dibujar proyectiles
        for proyectil in proyectiles:
            pygame.draw.circle(
                pantalla,
                (255, 220, 50),
                (int(proyectil["x"]), int(proyectil["y"])),
                radio_proyectil
            )

        renderer.actualizar_pantalla()

    # Mostrar GAME OVER solamente si hubo colision
    if colisiones:
        texto = fuente_game_over.render(
            "GAME OVER",
            True,
            (255, 50, 50)
        )

        rectangulo = texto.get_rect(
            center=(ancho // 2, alto // 2)
        )

        pantalla.blit(texto, rectangulo)
        pygame.display.flip()
        pygame.time.wait(2000)

    pygame.quit()


if __name__ == "__main__":
    main()
