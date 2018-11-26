import pygame
import pygame.gfxdraw
from .. import Drawable, updater
from ..events import events, Dispatcher
from ..utils import Rect
from .group import WidgetGroup, default_group
from .event import *


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

        global next_widget_id
        self.id = next_widget_id
        next_widget_id += 1

        events.subscribe(pygame.MOUSEBUTTONDOWN, self.__on_mouse_down)
        events.subscribe(pygame.MOUSEBUTTONUP, self.__on_mouse_up)

        group.add(self)
        updater.add(self.__update)

    def draw(self, surface):
        """ Draws the widget on the given surface """
        pygame.gfxdraw.box(surface, self.rect.dim(), (255, 255, 255))
        pygame.gfxdraw.rectangle(surface, self.rect.dim(), (0, 0, 0))

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
