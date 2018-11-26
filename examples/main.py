import pygame
from pygamegui import events, renderer, updater

if __name__ == '__main__':
    pygame.init()
    window = pygame.display.set_mode((800, 800))

    @events.on(pygame.QUIT)
    def on_quit():
        pygame.quit()
        exit()

    while True:
        for e in pygame.event.get():
            events.dispatch(e)

        updater.update()
        window.fill((33, 33, 36))
        renderer.draw(window)
        pygame.display.update()
