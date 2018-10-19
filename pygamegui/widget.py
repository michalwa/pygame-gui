import pygame
from pygamegui import Drawable, events, renderer, updater
from pygamegui.events.dispatcher import Dispatcher
from pygamegui.utils import Rect, event_code


WIDGET_MOUSE_DOWN = event_code()
""" When any mouse button is pressed while a widget is hovered """
WIDGET_MOUSE_UP = event_code()
""" When any mouse button is released while a widget is hovered """
WIDGET_HOVER_ENTER = event_code()
""" When the mouse cursor enters a widget's rect  """
WIDGET_HOVER_EXIT = event_code()
""" When the mouse cursor leaves a widget's rect  """


class WidgetEvent:
    def __init__(self, widget, code: int):
        self.widget = widget
        self.type = code


class WidgetMouseButtonEvent(WidgetEvent):
    def __init__(self, widget, code: int, button):
        super(__class__, self).__init__(widget, code)
        self.button = button


class Widget(Drawable, Dispatcher):
    """ A drawable, interactive GUI widget """
    def __init__(self, rect):
        super(__class__, self).__init__()
        self.rect = rect
        events.subscribe(self.__on_mouse_down, pygame.MOUSEBUTTONDOWN)
        events.subscribe(self.__on_mouse_up, pygame.MOUSEBUTTONUP)
        renderer.add(self)
        updater.add(self.__update)
        self.__was_hovered = False

    def draw(self, surface):
        """ Draws the widget on the given surface """
        pygame.draw.rect(surface, (255, 255, 255), self.rect)

    def is_hovered(self):
        """ Whether this widget is hovered with the mouse cursor """
        return pygame.mouse.get_pos() in Rect(self.rect)

    def __update(self):
        is_hovered = self.is_hovered()
        if is_hovered and not self.__was_hovered:
            self.__on_hover_enter()
        elif not is_hovered and self.__was_hovered:
            self.__on_hover_exit()
        self.__was_hovered = is_hovered

    def __on_mouse_down(self, event):
        if self.is_hovered():
            self.dispatch(WidgetMouseButtonEvent(self, WIDGET_MOUSE_DOWN, event.button))

    def __on_mouse_up(self, event):
        if self.is_hovered():
            self.dispatch(WidgetMouseButtonEvent(self, WIDGET_MOUSE_UP, event.button))

    def __on_hover_enter(self):
        self.dispatch(WidgetEvent(self, WIDGET_HOVER_ENTER))

    def __on_hover_exit(self):
        self.dispatch(WidgetEvent(self, WIDGET_HOVER_EXIT))
