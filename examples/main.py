import pygame
from pygameui import events, renderer
from pygameui.widget import Widget, WIDGET_MOUSE_DOWN, WIDGET_MOUSE_UP


def on_quit():
    """ Handles the pygame.QUIT event """
    pygame.quit()
    exit(0)


def on_widget_mouse_down(event):
    event.widget.rect[0] += 5


def on_widget_mouse_up(event):
    event.widget.rect[1] += 5


if __name__ == '__main__':
    pygame.init()
    window = pygame.display.set_mode((800, 800))

    events.subscribe(on_quit, pygame.QUIT)

    example_widget = Widget([100, 100, 200, 150])
    renderer.add(example_widget)
    example_widget.subscribe(on_widget_mouse_down, WIDGET_MOUSE_DOWN)
    example_widget.subscribe(on_widget_mouse_up, WIDGET_MOUSE_UP)

    while True:
        for e in pygame.event.get():
            events.dispatch(e)

        window.fill((33, 33, 36))
        renderer.draw(window)
        pygame.display.update()
