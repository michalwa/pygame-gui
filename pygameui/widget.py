import pygame
from pygameui import Drawable, events
from pygameui.events.dispatcher import Dispatcher
from pygameui.utils import Rect, event_code


WIDGET_MOUSE_DOWN = event_code()
WIDGET_MOUSE_UP = event_code()


class WidgetEvent:
    def __init__(self, widget, code: int):
        self.widget = widget
        self.type = code


class Widget(Drawable, Dispatcher):
    """ A drawable, interactive GUI widget """
    def __init__(self, rect):
        super(__class__, self).__init__()

        self.rect = rect

        events.subscribe(self.__on_mouse_down, lambda event: event.type == pygame.MOUSEBUTTONDOWN)
        events.subscribe(self.__on_mouse_up, lambda event: event.type == pygame.MOUSEBUTTONUP)

    def draw(self, surface):
        """ Draws the widget on the given surface """
        pygame.draw.rect(surface, (255, 255, 255), self.rect, 1)

    def is_hovered(self):
        """ Whether this widget is hovered with the mouse cursor """
        return pygame.mouse.get_pos() in Rect(self.rect)

    def __on_mouse_down(self):
        if self.is_hovered():
            self.dispatch(WidgetEvent(self, WIDGET_MOUSE_DOWN))

    def __on_mouse_up(self):
        if self.is_hovered():
            self.dispatch(WidgetEvent(self, WIDGET_MOUSE_UP))
