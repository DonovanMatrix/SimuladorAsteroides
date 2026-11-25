
import pygame


def main():
    pygame.init()

    screen = pygame.display.set_mode((1000, 700))
    pygame.display.set_caption("Simulador de Asteroides")

    clock = pygame.time.Clock()
    running = True

    while running:
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                running = False

        screen.fill((8, 10, 25))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
