import pygame
from pygamegui import events, renderer, updater
from pygamegui.widget import Widget, WidgetMouseButtonEvent, WIDGET_MOUSE_DOWN, WIDGET_MOUSE_UP, WIDGET_HOVER_ENTER, WIDGET_HOVER_EXIT
import pygamegui.mouse_buttons as mouse_buttons


background_color = (33, 33, 36)


def on_quit():
    """ Handles the pygame.QUIT event """
    pygame.quit()
    exit(0)


def on_widget_mouse_down(event: WidgetMouseButtonEvent):
    if event.button == mouse_buttons.LEFT:
        event.widget.rect[0] += 5


def on_widget_mouse_up(event: WidgetMouseButtonEvent):
    if event.button == mouse_buttons.LEFT:
        event.widget.rect[1] += 5


def on_widget_hover_enter():
    global background_color
    background_color = (33, 50, 36)


def on_widget_hover_exit():
    global background_color
    background_color = (33, 33, 36)


if __name__ == '__main__':
    pygame.init()
    window = pygame.display.set_mode((800, 800))

    events.subscribe(on_quit, pygame.QUIT)

    example_widget = Widget([100, 100, 200, 150])
    example_widget.subscribe(on_widget_mouse_down, WIDGET_MOUSE_DOWN)
    example_widget.subscribe(on_widget_mouse_up, WIDGET_MOUSE_UP)
    example_widget.subscribe(on_widget_hover_enter, WIDGET_HOVER_ENTER)
    example_widget.subscribe(on_widget_hover_exit, WIDGET_HOVER_EXIT)

    while True:
        for e in pygame.event.get():
            events.dispatch(e)

        updater.update()
        window.fill(background_color)
        renderer.draw(window)
        pygame.display.update()
