import pygame


class Drawable:
    """ Something drawable """

    def draw(self, surface: pygame.Surface):
        """ Draws this drawable on the given surface """
        raise NotImplementedError


class Renderer:
    """ Manages rendering on the display surface in a cleaner way """

    def __init__(self):
        self.__drawables = []

    def add(self, drawable: Drawable):
        """ Registers a drawable to draw in the draw cycle """
        self.__drawables.append(drawable)

    def draw(self, surface: pygame.Surface):
        """ Draws all the drawables to the given surface """
        for drawable in self.__drawables:
            drawable.draw(surface)


renderer = Renderer()
""" The main singleton renderer instance """
