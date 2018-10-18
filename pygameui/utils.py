class Rect:
    """ Represents a rectangle """
    def __init__(self, dim: list):
        (self.x, self.y, self.width, self.height) = dim

    def __contains__(self, item: list):
        (x, y) = item
        if type(x) == int and type(y) == int:
            return self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height
        return False


__next_event_code = 128


def event_code() -> int:
    """ Returns an event code that is ensured to be unique """
    global __next_event_code
    __next_event_code += 1
    return __next_event_code - 1
