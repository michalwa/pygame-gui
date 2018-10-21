import pygame


class Rect:
    """ Represents a rectangle """
    def __init__(self, dim):
        (self.x, self.y, self.width, self.height) = dim

    def dim(self):
        """ Returns a tuple with 4 elements being the dimensions of this rectangle """
        return self.x, self.y, self.width, self.height

    def __add__(self, other):
        (x, y) = other
        return Rect((self.x + float(x), self.y + float(y), self.width, self.height))

    def __sub__(self, other):
        (x, y) = other
        return Rect((self.x - float(x), self.y - float(y), self.width, self.height))

    def __mul__(self, other):
        return Rect((self.x, self.y, self.width * float(other), self.height * float(other)))

    def __rdiv__(self, other):
        return Rect((self.x, self.y, self.width / float(other), self.height / float(other)))

    def __contains__(self, item: list):
        (x, y) = item
        if type(y) in (int, float) and type(y) in (int, float):
            return self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height
        return False
