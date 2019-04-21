import pygame
from settings import *


"""
    Display text on the screen.
    Args:
        text (str): string that is text to be displayed (e.g. "Hello World")
        path: path to .ttf file for font selection (e.g. path.join(path.join(path.dirname(__file__), 'image'), 'CuteFont-Reuglar.ttf'))
        size (int): size of font to be displayed (int)
        color: rgb value of color of text. e.g. (0, 0, 0)
        x (int): horizontal coordinate of text, use manipulation of WIDTH value (e.g. WIDTH / 2)
        y (int): vertical coordinate, use manipulation of HEIGHT value (e.g. HEIGHT / 2)
        align (str): alignment of text in rectangle, default to center
"""
def text_to_screen(screen, text, path, size, color, x=0, y=0, align="center"):
    font = pygame.freetype.Font(path, size)
    text_surface, rect = font.render(text, color)
    text_rect = text_surface.get_rect()

    if align == "center":
        text_rect.center = (x, y)

    screen.blit(text_surface, text_rect)

def text_objects(message, font_path, font_size, font_color):
    text_font = pygame.freetype.Font(font_path, font_size)
    textSurface, rect = text_font.render(message, font_color)
    return textSurface, rect
