import pygame
from pygamegui import Drawable, updater
from pygamegui.events import events, Dispatcher
from pygamegui.utils import Rect
from pygamegui.widget.appearance.appearance import Appearance
from pygamegui.widget.group import WidgetGroup
from pygamegui.widget.event import *


default_group = WidgetGroup()
next_widget_id = 0


class Widget(Drawable, Dispatcher):
    """ A drawable, interactive GUI widget """
    def __init__(self, rect, group: WidgetGroup = default_group):
        super(__class__, self).__init__()

        self.rect = Rect(rect)
        """ The bounding rectangle of this widget """
        self.group = group
        """ The widget group this widget belongs to """
        self.__was_hovered = False
        self.__appearance = []

        global next_widget_id
        self.id = next_widget_id
        next_widget_id += 1

        events.subscribe(self.__on_mouse_down, pygame.MOUSEBUTTONDOWN)
        events.subscribe(self.__on_mouse_up, pygame.MOUSEBUTTONUP)

        group.add(self)
        updater.add(self.__update)

    def draw(self, surface):
        """ Draws the widget on the given surface """
        for appearance in self.__appearance:
            appearance.before_draw(surface, self)
        self.__appearance.reverse()

        self.__draw_self(surface)

        for appearance in self.__appearance:
            appearance.after_draw(surface, self)
        self.__appearance.reverse()

    def __draw_self(self, surface):
        """ To be overridden by subclasses - draws this widget """
        pygame.draw.rect(surface, (255, 255, 255), self.rect.dim())

    def is_hovered(self, covering: bool = True) -> bool:
        """ Whether this widget is hovered with the mouse cursor. If the `covering` parameter is
        set to true, a check for widgets from this widget's group covering this widget will be performed """
        if covering:
            return self.group.is_hovered(self)
        else:
            return pygame.mouse.get_pos() in self.rect

    def move_to_top(self):
        """ Moves the specified widget to the top of the group """
        self.group.move_to_top(self)

    def move_to_bottom(self):
        """ Moves the specified widget to the bottom of the group """
        self.group.move_to_bottom(self)

    def move_up(self):
        """ Moves the specified widget above the widget that is currently above it in its group """
        self.group.move_up(self)

    def move_down(self):
        """ Moves the specified widget below the widget that is currently below it in its group """
        self.group.move_down(self)

    def add(self, appearance: Appearance):
        """ Adds the given appearance to this widget """
        self.__appearance.append(appearance)

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
