import pygame
from pygamegui import Drawable, renderer, updater
from pygamegui.events import events, Dispatcher
from pygamegui.utils import Rect, event_code


WIDGET_MOUSE_DOWN = event_code()
""" When any mouse button is pressed while a widget is hovered """
WIDGET_MOUSE_UP = event_code()
""" When any mouse button is released while a widget is hovered """
WIDGET_HOVER_ENTER = event_code()
""" When the mouse cursor enters a widget's rect  """
WIDGET_HOVER_EXIT = event_code()
""" When the mouse cursor leaves a widget's rect  """


class WidgetGroup(Drawable):
    """ Stores widgets that are meant to be displayed and interacted with in the same scene.
    Allows determining which widget should be clicked, hovered, etc."""
    def __init__(self):
        self.__widgets = []
        renderer.add(self)

    def draw(self, surface: pygame.Surface):
        for widget in self.__widgets:
            widget.draw(surface)

    def add(self, widget):
        """ Adds a widget to the group """
        if widget not in self:
            self.__widgets.append(widget)

    def move_to_top(self, widget):
        """ Moves the specified widget to the top of the group """
        if widget in self:
            self.__widgets.remove(widget)
            self.__widgets.append(widget)

    def move_to_bottom(self, widget):
        """ Moves the specified widget to the bottom of the group """
        if widget in self:
            self.__widgets.remove(widget)
            self.__widgets.insert(0, widget)

    def move_up(self, widget):
        """ Moves the specified widget above the widget that is currently above it """
        if widget in self:
            index = self.__widgets.index(widget)
            if not index == len(self.__widgets) - 1:
                self.__widgets.remove(widget)
                self.__widgets.insert(index, widget)

    def move_down(self, widget):
        """ Moves the specified widget below the widget that is currently below it """
        if widget in self:
            index = self.__widgets.index(widget)
            if not index == 0:
                self.__widgets.remove(widget)
                self.__widgets.insert(index - 1, widget)

    def is_hovered(self, widget) -> bool:
        """ Checks, if the specified widget is hovered with the mouse cursor
        and if no elements in this group are covering it """
        if widget in self:
            if not widget.is_hovered(covering=False):
                return False

            top_hovered = widget
            for w in self.__widgets:
                if w.is_hovered(covering=False):
                    top_hovered = w

            return top_hovered == widget
        else:
            return False

    def __len__(self):
        return len(self.__widgets)

    def __contains__(self, item):
        return item in self.__widgets


default_group = WidgetGroup()


class WidgetEvent:
    def __init__(self, widget, code: int):
        self.widget = widget
        self.type = code


class WidgetMouseButtonEvent(WidgetEvent):
    def __init__(self, widget, code: int, button):
        super(__class__, self).__init__(widget, code)
        self.button = button


next_widget_id = 0


class Widget(Drawable, Dispatcher):
    """ A drawable, interactive GUI widget """
    def __init__(self, rect: list, group: WidgetGroup = default_group):
        super(__class__, self).__init__()

        self.rect = rect
        self.group = group
        self.__was_hovered = False

        global next_widget_id
        self.id = next_widget_id
        next_widget_id += 1

        events.subscribe(self.__on_mouse_down, pygame.MOUSEBUTTONDOWN)
        events.subscribe(self.__on_mouse_up, pygame.MOUSEBUTTONUP)

        group.add(self)
        updater.add(self.__update)

    def draw(self, surface):
        """ Draws the widget on the given surface """
        pygame.draw.rect(surface, (0, 0, 0), self.rect)
        pygame.draw.rect(surface, (255, 255, 255), self.rect, 2)

    def is_hovered(self, covering: bool = True) -> bool:
        """ Whether this widget is hovered with the mouse cursor. If the `covering` parameter is
        set to true, a check for widgets from this widget's group covering this widget will be performed """
        if covering:
            return self.group.is_hovered(self)
        else:
            return pygame.mouse.get_pos() in Rect(self.rect)

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
