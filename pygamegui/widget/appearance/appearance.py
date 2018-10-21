import pygame


class Appearance:
    """ Changes the appearance of any widget """

    def before_draw(self, surface: pygame.Surface, widget):
        """ Called before the widget is drawn """
        raise NotImplementedError

    def after_draw(self, surface: pygame.Surface, widget):
        """ Called after the widget is drawn """
        raise NotImplementedError
