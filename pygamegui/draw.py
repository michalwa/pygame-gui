import pygame


def draw_translucent_rect(surface: pygame.Surface, color: tuple, rect: tuple):
    """ Draws a translucent rectangle on the given surface """
    if len(rect) >= 4:
        if len(color) < 4:
            color = (color[0], color[1], color[2], 255)
        rect_surface = pygame.Surface(rect[2:4])
        rect_surface.set_alpha(color[3])
        rect_surface.fill(color[0:3])
        surface.blit(rect_surface, rect[0:2])
