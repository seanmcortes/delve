import pygame
import pygame.freetype
import sys
from os import path
from settings import *
from sprites import *
import scenes
from scenes import *
from helper import *

#Source: https://stackoverflow.com/questions/28005641/how-to-add-a-background-image-into-pygame
class Background(pygame.sprite.Sprite):
	def __init__(self, image_file, location):
		pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
		self.image = pygame.image.load(image_file)
		self.rect = self.image.get_rect()
		self.rect.left, self.rect.top = location

class MenuButton():
    def __init__(self, game, msg, location, action=None):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.msg = msg
        self.img = self.img_holder()
        self.image = self.img.normal
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        self.x = self.rect.left
        self.y = self.rect.top
        self.h = 50
        self.w = 100
        self.screen = game.screen
        self.action = action
        self.textSurf, self.textRect = text_objects(self.msg, 'image/CuteFont-Regular.ttf',20, BLACK)
        self.textRect.center = ( (self.x+(self.w/2)), (self.y+(self.h/2)) )
        self.NORMAL = True
        self.CLICKED = False

        

    class img_holder():
        def __init__(self):
            self.normal = pygame.image.load('image/button_normal.png')
            self.hover = pygame.image.load('image/button_hover.png')
            self.click = pygame.image.load('image/button_click.png')

    def handle_events(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if self.x + self.w > mouse[0] > self.x and self.y + self.h > mouse[1] > self.y:
            self.image = self.img.hover

            if click[0] == 1 and self.action != None:
                self.image = self.img.click
                self.CLICKED = True
                self.NORMAL = False

        else:
            self.image = self.img.normal

        return None

    def update(self):
            if self.CLICKED == True:
                if self.NORMAL == False:
                    self.y += 1
                    self.textRect.center = ( (self.x+(self.w/2)), (self.y+(self.h/2)) )
                    self.NORMAL = True
                elif self.NORMAL == True:
                    self.y -= 1
                    self.textRect.center = ( (self.x+(self.w/2)), (self.y+(self.h/2)) )
                    self.image = self.img.normal
                    self.CLICKED = False
    def draw(self):
            #self.textSurf, self.textRect = text_objects(self.msg, 'image/CuteFont-Regular.ttf',50, BLACK)
            #self.textRect.center = ( (self.x+(self.w/2)), (self.y+(self.h/2)) )
            self.screen.blit(self.image, self.rect)
            self.screen.blit(self.textSurf, self.textRect)

    """
    Helper functions for main menu
    """
class MainMenuScene():
    def __init__(self, game):
        self.show_main_menu = True
        self.game = game
        self.all_buttons = []
        self.background = Background('image/menuback.jpg', [0,0])
        self.button1 = MenuButton(self.game, "Play", [140,400], self.playgame)
        self.button2 = MenuButton(self.game, "Quit", [400,400], self.quitgame)
        self.all_buttons.append(self.button1)
        self.all_buttons.append(self.button2)

    def quitgame(self):
        pygame.quit()
        quit()

    def playgame(self):
        self.show_main_menu = False
        self.game.go_to(scenes.Level1Scene())

    """
    Display the main menu screen.

    Allow the user to perform the following options:
    1. Start the game from level 1
    2. Load a saved file
    3. Exit the game
    """
    def render(self, screen):
        self.dt = self.game.clock.tick(FPS) / 1000
        self.game.screen.fill(BLACK)
        self.game.screen.blit(self.background.image, self.background.rect)
        text_to_screen(self.game.screen, "DELVE", 'image/CuteFont-Regular.ttf', 100, WHITE, WIDTH / 2, HEIGHT / 4)

        for p in self.all_buttons:
            p.draw()

        for p in self.all_buttons:
            if p.CLICKED == True:
                pygame.display.flip()
                pygame.time.delay(250)
                p.update()
                p.draw()
                pygame.display.flip()
                pygame.time.delay(500)
                p.action()

    """
    Event listener for main menu.
    """
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        for p in self.all_buttons:
            p.handle_events()

    def update(self):
        for p in self.all_buttons:
            p.update()
"""
    def text_to_screen(self, text, path, size, color, x=0, y=0, align="center"):
    	self.font = pygame.freetype.Font(path, size)
    	text_surface, rect = self.font.render(text, color)
    	text_rect = text_surface.get_rect()

    	if align == "center":
    		text_rect.center = (x, y)

    	self.game.screen.blit(text_surface, text_rect)
"""
    # https://stackoverflow.com/questions/20842801/how-to-display-text-in-pygame
