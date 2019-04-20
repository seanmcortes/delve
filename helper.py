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


"""
    Render button on screen.
    Args:
        msg (str): text on button
        x: x-coord position on screen
        y: y-coord position on screen
        w: width of button
        h: height of button
        ic:
        ac:
        action: function which executes when button is pressed
"""
def button(screen, msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, ic,(x,y,w,h))
        pygame.draw.line(screen, LIGHTGREY, (x-1, y-1), (x+w, y-1))
        pygame.draw.line(screen, WHITE, (x-1, y+h+1), (x+w+1, y+h+1))
        pygame.draw.line(screen, LIGHTGREY, (x-1, y-1), (x-1, y+h))
        pygame.draw.line(screen, WHITE, (x+w+1, y-1), (x+w+1, y+h+1))
        x=x+1
        y=y+1

        if click[0] == 1 and action != None:
            action()
        else:
            pygame.draw.rect(screen, ic,(x,y,w,h))
            pygame.draw.line(screen, WHITE, (x-1, y-1), (x+w, y-1))
            pygame.draw.line(screen, DARKGREY, (x-1, y+h+1), (x+w+1, y+h+1))
            pygame.draw.line(screen, WHITE, (x-1, y-1), (x-1, y+h))
            pygame.draw.line(screen, DARKGREY, (x+w+1, y-1), (x+w+1, y+h+1))

        smallText = pygame.font.SysFont(TITLE_FONT_PATH,20)
        textSurf, textRect = text_objects(msg, smallText)
        textRect.center = ( (x+(w/2)), (y+(h/2)) )
        screen.blit(textSurf, textRect)


def text_objects(text, font):
    textSurface = font.render(text, True, BLACK)
    return textSurface, textSurface.get_rect()