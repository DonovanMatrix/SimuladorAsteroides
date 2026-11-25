
import pygame


class Renderer:

    def __init__(self, pantalla):
        self.pantalla = pantalla

    def dibujar_fondo(self):
        self.pantalla.fill((8, 10, 25))

    def dibujar_nave(self, nave):
        pygame.draw.polygon(
            self.pantalla,
            (50, 200, 255),
            [
                (int(nave.x), int(nave.y - nave.radio)),
                (int(nave.x - nave.radio), int(nave.y + nave.radio)),
                (int(nave.x + nave.radio), int(nave.y + nave.radio))
            ]
        )

    def dibujar_asteroides(self, asteroides):
        for asteroide in asteroides:
            pygame.draw.circle(
                self.pantalla,
                (180, 180, 190),
                (int(asteroide.x), int(asteroide.y)),
                int(asteroide.radio)
            )

    def dibujar_puntuacion(self, puntuacion):
        fuente = pygame.font.SysFont("Arial", 24)

        texto = fuente.render(
            f"Puntuacion: {puntuacion}",
            True,
            (255, 255, 255)
        )

        self.pantalla.blit(texto, (15, 15))

    def actualizar_pantalla(self):
        pygame.display.flip()
