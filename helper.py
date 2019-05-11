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
    Creates an text object to display text to the screen.
    Args:
        text (str): string that is text to be displayed (e.g. "Hello World")
        path: path to .ttf file for font selection (e.g. path.join(path.join(path.dirname(__file__), 'image'), 'CuteFont-Reuglar.ttf'))
        size (int): size of font to be displayed (int)
        color: rgb value of color of text. e.g. (0, 0, 0)
        x (int): horizontal coordinate of text, use manipulation of WIDTH value (e.g. WIDTH / 2)
        y (int): vertical coordinate, use manipulation of HEIGHT value (e.g. HEIGHT / 2)
        align (str): alignment of text in rectangle, default to center
"""
class TextObject():
    def __init__(self, text, path, size, color, x=0, y=0, align="center"):
    	font = pygame.freetype.Font(path, size)
    	self.surface, self.rect = font.render(text, color)

    	if align == "center":
    		self.rect.center = (x, y)
    	else:
    		self.rect.left = x
    		self.rect.top = y

    """
    Renders the text object to the screen
    Args:
        screen: the display the object will be rendered to
    """
    def render(self, screen):
    	 screen.blit(self.surface, self.rect)

    """
    Draw transparent pbject to screen
    """
    def blit_alpha(self, screen, opacity):
        x = self.rect.x
        y = self.rect.y
        temp = pygame.Surface((self.surface.get_width(), self.surface.get_height())).convert()
        temp.blit(screen, (-x, -y))
        temp.blit(self.surface, (0, 0))
        temp.set_alpha(opacity)
        screen.blit(temp, [x, y])

"""
This class is used to draw instructions to the screen using text objects
Args:
    screen: the display the object will be rendered to
"""
class Instructions():
    def __init__(self, size, color):
        self.path = CUTEFONT
        self.size = size
        self.color = color
        self.x = WIDTH/2
        self.start_ticks=pygame.time.get_ticks() #get the time to only display the instructions on screen for a few second
        self.rows = [] #Holds the instruction text objects
        self.opacity = 255

    def add(self, text, y=0):
        self.rows.append(TextObject(text, self.path, self.size, BLACK, self.x+1, y+1, "center")) #add a shadow to make text easier to read
        self.rows.append(TextObject(text, self.path, self.size, self.color, self.x, y, "center")) # add text on top of shadow

    def draw(self, screen):
        if self.opacity > 0: #only execute these instructions if the object has not disappered
            seconds=(pygame.time.get_ticks()-self.start_ticks)/1000 #calculate how many seconds
            if seconds > 1:
                for text in self.rows:
                    text.blit_alpha(screen, self.opacity)

    def update(self):
        if self.opacity > 0:
            seconds=(pygame.time.get_ticks()-self.start_ticks)/1000 #calculate how many seconds
            if seconds > 3:
                self.opacity -= 5
