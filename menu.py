import pygame
import pygame.freetype
import sys
from os import path
from settings import *
from sprites import *
import scenes
from scenes import *
from helper import *
from os import listdir #for file handling
from os.path import isfile, join #for file handling

#Source: https://stackoverflow.com/questions/28005641/how-to-add-a-background-image-into-pygame
class Background(pygame.sprite.Sprite):
	def __init__(self, image_file, location):
		pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
		self.image = pygame.image.load(image_file)
		self.rect = self.image.get_rect()
		self.rect.left, self.rect.top = location

class TextObject():
	def __init__(self, text, path, size, color, x=0, y=0, align="center"):
		font = pygame.freetype.Font(path, size)
		self.surface, self.rect = font.render(text, color)

		if align == "center":
			self.rect.center = (x, y)
		else:
			self.rect.left = x
			self.rect.top = y

	def render(self,screen):
		 screen.blit(self.surface, self.rect)

class MenuButton():
	def __init__(self, game, msg, location, action=None, optional_argument=None):
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
		self.optional_argument = optional_argument

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
Display the main menu screen.

Allow the user to perform the following options:
1. Start the game from level 1
2. Load a saved file
3. Exit the game
"""
class MainMenuScene():
	def __init__(self, game):
		#self.show_main_menu = True
		self.game = game
		self.text_logo = TextObject("DELVE", 'image/CuteFont-Regular.ttf', 175, WHITE, WIDTH / 2, HEIGHT / 4)
		self.textObjects = [self.text_logo]
		self.all_buttons = []
		self.background = Background('image/menuback.jpg', [0,0])
		self.button1 = MenuButton(self.game, "Play", [140,400], self.playgame)
		self.button2 = MenuButton(self.game, "Load", [270,400], self.loadgame)
		self.button3 = MenuButton(self.game, "Quit", [400,400], self.quitgame)
		self.all_buttons.append(self.button1)
		self.all_buttons.append(self.button2)
		self.all_buttons.append(self.button3)

	def quitgame(self):
		pygame.quit()
		quit()

	def playgame(self):
		#self.show_main_menu = False
		self.game.go_to(scenes.Level1Scene())

	def loadgame(self):
		self.game.go_to(LoadGameScene(self.game))

	def mainmenu(self):
		self.game.go_to(MainMenuScene(self.game))

	def render(self, screen):
		self.dt = self.game.clock.tick(FPS) / 1000
		#self.game.screen.fill(BLACK)
		self.game.screen.blit(self.background.image, self.background.rect)
		for t in self.textObjects:
			t.render(self.game.screen)

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
				if p.optional_argument == None:
					p.action()
				else: #this is used to load a level
					p.action(p.optional_argument)

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
Display the game over screen

Ask the user if they would like to continue and prompt with "yes" or "no"

    1. Yes (reload current level)
    2. No (exit to main menu)

"""
class GameOverScene(MainMenuScene):
	def __init__(self, game):
		#super().__init__(game)
		self.game = game
		self.background = Background('image/gameoverback.jpg', [0,0])
		self.text_logo = TextObject("GAME OVER", 'image/CuteFont-Regular.ttf', 100, WHITE, WIDTH / 2, HEIGHT / 4)
		self.text_message = TextObject("Would you like to continue?", 'image/CuteFont-Regular.ttf', 50, WHITE, WIDTH / 2, (HEIGHT / 3)+50)
		self.textObjects = [self.text_logo, self.text_message]
		self.button1 = MenuButton(self.game, "Yes", [270,350], self.playgame)
		self.button2 = MenuButton(self.game, "No", [270,425], self.mainmenu)
		self.all_buttons = [self.button1, self.button2]

class LoadGameScene(MainMenuScene):
	def __init__(self, game):
		#super().__init__(game)
		self.game = game
		self.background = Background('image/menuback.jpg', [0,0])
		self.text_logo = TextObject("Load Game", 'image/CuteFont-Regular.ttf', 100, WHITE, WIDTH / 2, HEIGHT / 4)
		self.textObjects = [self.text_logo]
		self.button1 = MenuButton(self.game, "Back", [270,450], self.mainmenu)
		self.all_buttons = [self.button1]
		save_path = 'save'
		#Source: https://stackoverflow.com/questions/3207219/how-do-i-list-all-files-of-a-directory
		#gets only files not any directories
		y = 250
		count = 0
		files = [f for f in listdir(save_path) if isfile(join(save_path, f))]
		for o in files:
			f = open(join(save_path, o), "r")
			if f.mode == 'r':
				try:
					number = int(f.readline().strip())
				except:
					number = "Not an integer"
				if isinstance(number, int) and count < 3: #to do: make sure number is an actual level
					date = f.readline().strip()
					if (number < 10):
						save_text = "Level:   " + str(number) + " Time: " + date
					else:
						save_text = "Level: " + str(number) + " Time: " + date
					self.textObjects.append(TextObject(save_text, 'image/CuteFont-Regular.ttf', 40, WHITE, 210, y+14, "left"))
					self.all_buttons.append(MenuButton(self.game, "Load", [100, y], self.loadlevel, number))
					y += 60
					count += 1
				f.close()

	def loadlevel(self, level):
		#Source: https://jaxenter.com/implement-switch-case-statement-python-138315.html
		switcher = {
	        1: scenes.Level1Scene,
	        2: GameOverScene,
	        3: GameOverScene,
	        4: GameOverScene,
	        5: GameOverScene,
	        6: GameOverScene,
	        7: GameOverScene,
	        8: GameOverScene,
	        9: GameOverScene,
	        10: GameOverScene,
		}
	    # Get the function from switcher dictionary
		func = switcher.get(level, lambda: "Invalid level")
		# Execute the function
		if level > 1: #this is just here until we implement the other levels, becuase GameOverScene requires the game be passed to it
			self.game.go_to(func(self.game))
		else:
			self.game.go_to(func())
