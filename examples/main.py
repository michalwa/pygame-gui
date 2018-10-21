import pygame
from pygamegui import events, renderer, updater, mouse_buttons
from pygamegui.widget import Widget, WidgetEvent, WidgetMouseButtonEvent,\
    WIDGET_MOUSE_DOWN, WIDGET_MOUSE_UP, WIDGET_HOVER_ENTER, WIDGET_HOVER_EXIT
from pygamegui.widget.appearance import DropShadow


background_color = (33, 63, 146)


def on_quit():
    pygame.quit()
    exit(0)


def on_widget_mouse_down(event: WidgetMouseButtonEvent):
    if event.button == mouse_buttons.LEFT:
        event.widget.rect += (10, 0)
        event.widget.move_to_top()


def on_widget_mouse_up(event: WidgetMouseButtonEvent):
    if event.button == mouse_buttons.LEFT:
        event.widget.rect += (0, 10)


def on_widget_hover_enter(event: WidgetEvent):
    global background_color
    if event.widget.id == 0:
        background_color = (33, 103, 36)
    else:
        background_color = (123, 33, 36)


def on_widget_hover_exit():
    global background_color
    background_color = (33, 63, 146)


if __name__ == '__main__':
    pygame.init()
    window = pygame.display.set_mode((800, 800))

    events.subscribe(on_quit, pygame.QUIT)

    example_widget = Widget([100, 100, 200, 150])
    another_widget = Widget([180, 180, 200, 150])
    example_widget.move_to_top()

    for widget in (example_widget, another_widget):
        widget.add(DropShadow(5, 5, (0, 0, 0, 63)))

        widget.subscribe(on_widget_mouse_down, WIDGET_MOUSE_DOWN)
        widget.subscribe(on_widget_mouse_up, WIDGET_MOUSE_UP)
        widget.subscribe(on_widget_hover_enter, WIDGET_HOVER_ENTER)
        widget.subscribe(on_widget_hover_exit, WIDGET_HOVER_EXIT)

    while True:
        for e in pygame.event.get():
            events.dispatch(e)

        updater.update()
        window.fill(background_color)
        renderer.draw(window)
        pygame.display.update()
