import pygame
from ..renderer import Drawable, renderer


class WidgetGroup(Drawable):
    """ Stores widgets that are meant to be displayed and interacted with in the same scene.
    Allows determining which widget should be clicked, hovered, etc. """

    def __init__(self):
        self.__widgets = []
        renderer.add(self)

    def draw(self, surface: pygame.Surface):
        """ Draws all widgets in this group in the correct order """
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
