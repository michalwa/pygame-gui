import pygame
from pygamegui.draw import draw_translucent_rect
from pygamegui.widget.appearance.appearance import Appearance


class DropShadow(Appearance):
    """ A shadow behind the widget """
    def __init__(self, x_offset, y_offset, color):
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.color = color

    def before_draw(self, surface: pygame.Surface, widget):
        draw_translucent_rect(surface, self.color, (widget.rect + (self.x_offset, self.y_offset)).dim())

    def after_draw(self, surface: pygame.Surface, widget):
        pass
