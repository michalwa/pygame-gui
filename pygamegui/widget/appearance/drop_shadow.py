import pygame.gfxdraw
from pygamegui.widget.appearance.appearance import Appearance


class DropShadow(Appearance):
    """ A shadow behind the widget """
    def __init__(self, x_offset, y_offset, color):
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.color = color

    def before_draw(self, surface: pygame.Surface, widget):
        rect = widget.rect + (self.x_offset, self.y_offset)
        pygame.gfxdraw.box(surface, rect.dim(), self.color)

    def after_draw(self, surface: pygame.Surface, widget):
        pass
