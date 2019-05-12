import pygame
import pygame.freetype
import sys
from os import path
from os import remove # to delete corrupted save files
from settings import *
#from sprites import *
#import scenes
#from scenes import *
from helper import *
from os import listdir #for file handling
from os.path import isfile, join #for file handling
import datetime #for getting the time for the save files

#Source: https://stackoverflow.com/questions/28005641/how-to-add-a-background-image-into-pygame
class Background(pygame.sprite.Sprite):
	def __init__(self, image_file, location):
		pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
		self.image = pygame.image.load(image_file)
		self.rect = self.image.get_rect()
		self.rect.left, self.rect.top = location

class MenuButton():
	def __init__(self, game, msg, location, action=None, optional_argument=None):
		pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
		#self.game_folder = path.dirname(__file__)
		#self.image_folder = path.join(self.game_folder, "image")
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
		self.text = TextObject(self.msg, path.join(IMAGE_FOLDER, 'CuteFont-Regular.ttf'),20, BLACK, (self.x+(self.w/2)), (self.y+(self.h/2)) )
		self.NORMAL = True
		self.CLICKED = False
		self.optional_argument = optional_argument

	class img_holder():
		def __init__(self):
			#game_folder = path.dirname(__file__)
			#image_folder = path.join(game_folder, "image")
			self.normal = pygame.image.load(path.join(IMAGE_FOLDER,'button_normal.png'))
			self.hover = pygame.image.load(path.join(IMAGE_FOLDER,'button_hover.png'))
			self.click = pygame.image.load(path.join(IMAGE_FOLDER,'button_click.png'))

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
	                self.text.rect.center = ( (self.x+(self.w/2)), (self.y+(self.h/2)) )
	                self.NORMAL = True
	            elif self.NORMAL == True:
	                self.y -= 1
	                self.text.rect.center = ( (self.x+(self.w/2)), (self.y+(self.h/2)) )
	                self.image = self.img.normal
	                self.CLICKED = False

	def draw(self):
	        self.screen.blit(self.image, self.rect)
	        self.text.render(self.screen)

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
		#self.game_folder = path.dirname(__file__)
		#self.image_folder = path.join(self.game_folder, "image")
		self.text_logo = TextObject("DELVE", path.join(IMAGE_FOLDER, 'CuteFont-Regular.ttf'), 175, WHITE, WIDTH / 2, HEIGHT / 4)
		self.textObjects = [self.text_logo]
		self.all_buttons = []
		self.background = Background(path.join(IMAGE_FOLDER, 'menuback.jpg'), [0,0])
		self.button1 = MenuButton(self.game, "Play", [140,400], self.playgame)
		self.button2 = MenuButton(self.game, "Load", [270,400], self.loadgamescreen)
		self.button3 = MenuButton(self.game, "Quit", [400,400], self.quitgame)
		self.button4 = MenuButton(self.game, "Credits", [270,460], self.show_credits)
		self.all_buttons.append(self.button1)
		self.all_buttons.append(self.button2)
		self.all_buttons.append(self.button3)
		self.all_buttons.append(self.button4)

	def render(self):
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

	########################################################################
	# These are the functions that are executed by the button presses
	#######################################################################
	def quitgame(self):
		pygame.quit()
		quit()

	def playgame(self):
		#self.show_main_menu = False
		self.game.select_scene(1)

	def loadgamescreen(self):
		self.game.go_to(LoadGameScene(self.game))

	def mainmenu(self):
		self.game.go_to(MainMenuScene(self.game))

	def loadlevel(self, level):
		self.game.select_scene(level)

	def savelevel(self, file_name):
		f = open(path.join(SAVE_FOLDER, file_name),"w+")
		f.write(str(self.game.scene.scene_number) + "\n")
		#get current Time
		#source: https://stackoverflow.com/questions/415511/how-to-get-the-current-time-in-python
		current_time = datetime.datetime.now()
		#convert time to a string
		#Source: https://stackoverflow.com/questions/311627/how-to-print-a-date-in-a-regular-format
		time_str = current_time.strftime('%m/%d/%Y, %H:%M:%S')
		f.write(time_str)
		f.close()
		self.WAITING = False #exit the save screen

	def restartlevel(self):
		self.loadlevel(self.game.scene.scene_number)
		self.unpause()

	def show_credits(self):
		credits_screen = CreditScene(self.game)
		credits_screen.render()

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
		current_scene = game.scene.scene_number
		self.game = game
		self.background = Background(path.join(IMAGE_FOLDER,'gameoverback.jpg'), [0,0])
		self.text_logo = TextObject("GAME OVER", path.join(IMAGE_FOLDER, 'CuteFont-Regular.ttf'), 100, WHITE, WIDTH / 2, HEIGHT / 4)
		self.text_message = TextObject("Would you like to continue?", path.join(IMAGE_FOLDER, 'CuteFont-Regular.ttf'), 50, WHITE, WIDTH / 2, (HEIGHT / 3)+50)
		self.textObjects = [self.text_logo, self.text_message]
		self.button1 = MenuButton(self.game, "Yes", [270,350], self.loadlevel, current_scene)
		self.button2 = MenuButton(self.game, "No", [270,425], self.mainmenu)
		self.all_buttons = [self.button1, self.button2]

class LoadGameScene(MainMenuScene):
	def __init__(self, game):
		#super().__init__(game)
		self.game = game
		self.background = Background(path.join(IMAGE_FOLDER, 'menuback.jpg'), [0,0])
		self.text_logo = TextObject("Load Game", path.join(IMAGE_FOLDER, 'CuteFont-Regular.ttf'), 100, WHITE, WIDTH / 2, HEIGHT / 4)
		self.textObjects = [self.text_logo]
		self.button1 = MenuButton(self.game, "Back", [270,450], self.mainmenu)
		self.all_buttons = [self.button1]
		#Source: https://stackoverflow.com/questions/3207219/how-do-i-list-all-files-of-a-directory
		#gets only files not any directories
		y = 250
		count = 0
		files = [f for f in listdir(SAVE_FOLDER) if isfile(join(SAVE_FOLDER, f))]
		for o in files:
				f = open(join(SAVE_FOLDER, o), "r")
				if f.mode == 'r' and count < 5:
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
						self.textObjects.append(TextObject(save_text, path.join(IMAGE_FOLDER, 'CuteFont-Regular.ttf'), 30, WHITE, 210, y+14, "left"))
						self.all_buttons.append(MenuButton(self.game, "Load", [100, y], self.loadlevel, number))
						y += 60
						count += 1
					f.close()

class SaveGameScene(MainMenuScene):
	def __init__(self, game):
		#super().__init__(game)
		self.game = game
		self.background = Background(path.join(IMAGE_FOLDER, 'menuback.jpg'), [0,0])
		self.text_logo = TextObject("Pause Menu", path.join(IMAGE_FOLDER, 'CuteFont-Regular.ttf'), 100, WHITE, WIDTH / 2, HEIGHT / 4)
		self.textObjects = [self.text_logo]
		self.button1 = MenuButton(self.game, "Back", [270,550], self.stopwaiting)
		self.all_buttons = [self.button1]
		self.WAITING = False #wait for the player to save or quit the save game screen
		#self.files = [] #holds the file names as a string
		#Source: https://stackoverflow.com/questions/3207219/how-do-i-list-all-files-of-a-directory
		#gets only files not any directories
		y = 250
		count = 0
		files = [f for f in listdir(SAVE_FOLDER) if isfile(join(SAVE_FOLDER, f))]
		for file_name in files:
				f = open(join(SAVE_FOLDER, file_name), "r")
				if f.mode == 'r' and count < 5:
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
						self.textObjects.append(TextObject(save_text, path.join(IMAGE_FOLDER, 'CuteFont-Regular.ttf'), 30, WHITE, 210, y+14, "left"))
						self.all_buttons.append(MenuButton(self.game, "Save", [100, y], self.savelevel, file_name))
						y += 60
						count += 1
						#self.files.add(file_name) #add the file name to the files array
						f.close()
					#delete corrupted files
					elif not isinstance(number, int):
						f.close()
						remove(join(SAVE_FOLDER, file_name))
		while count < 3: #create more save files if there are some that do no exist
			file_num = 1
			temp_name = str(file_num) + ".sav"
			while isfile(join(SAVE_FOLDER, temp_name)): #loop until finding a filename that does not exist
				file_num += 1
				temp_name = str(file_num) + ".sav"
			self.all_buttons.append(MenuButton(self.game, "Save", [100, y], self.savelevel, temp_name))
			y += 60
			count += 1



	def loop(self):
		self.WAITING = True
		while self.WAITING:
			self.dt = self.game.clock.tick(FPS) / 1000
			self.handle_events(pygame.event.get())
			self.update()
			self.render()
			pygame.display.flip()

	def stopwaiting(self):
		self.WAITING = False



class PauseScene(MainMenuScene):
	def __init__(self, game):
		#super().__init__(game)
		self.game = game
		self.background = Background(path.join(IMAGE_FOLDER, 'menuback.jpg'), [0,0])
		self.text_logo = TextObject("Pause Menu", path.join(IMAGE_FOLDER, 'CuteFont-Regular.ttf'), 100, WHITE, WIDTH / 2, HEIGHT / 4)
		self.textObjects = [self.text_logo]
		self.button1 = MenuButton(self.game, "Save Game", [270,250], self.savegame)
		self.button2 = MenuButton(self.game, "Main Menu", [270,325], self.mainmenu)
		self.button3 = MenuButton(self.game, "Restart Level", [270,400], self.restartlevel)
		self.button4 = MenuButton(self.game, "Back to Game", [270,475], self.unpause)
		self.all_buttons = [self.button1, self.button2, self.button3, self.button4]
		save_path = 'save'

	def paused(self):
		self.PAUSED = True
		while self.PAUSED:
			self.dt = self.game.clock.tick(FPS) / 1000
			self.handle_events(pygame.event.get())
			self.update()
			self.render()
			pygame.display.flip()

	def unpause(self):
		self.PAUSED = False

	"""Override of mainmenu submethod for PauseScene"""
	def mainmenu(self):
			self.unpause()
			self.game.go_to(MainMenuScene(self.game))

	def savegame(self):
			saveScreen = SaveGameScene(self.game)
			saveScreen.loop()

class CreditScene(MainMenuScene):
	def __init__(self, game):
		self.game = game
		self.background = Background(path.join(IMAGE_FOLDER, 'menuback.jpg'), [0,0])
		#self.textObjects = [TextObject("Credits", path.join(IMAGE_FOLDER, 'CuteFont-Regular.ttf'), 50, BLACK, WIDTH / 2 + 1, HEIGHT / 4 + 1),
		#					TextObject("Credits", path.join(IMAGE_FOLDER, 'CuteFont-Regular.ttf'), 50, WHITE, WIDTH / 2, HEIGHT / 4)]
		self.instructions = Instructions(30, WHITE)
		self.instructions.rows.append(TextObject("Credits", path.join(IMAGE_FOLDER, 'CuteFont-Regular.ttf'), 60, BLACK, WIDTH / 2 + 1, HEIGHT / 4 - 40 + 1))
		self.instructions.rows.append(TextObject("Credits", path.join(IMAGE_FOLDER, 'CuteFont-Regular.ttf'), 60, WHITE, WIDTH / 2, HEIGHT / 4 - 40))
		self.instructions.add("Developers:", 190)
		self.instructions.add("Sir Sean Cortes", 230)
		self.instructions.add("Jason Anderson, Esq.", 270)
		self.instructions.add("Mr. Joshua Nutt", 310)
		self.instructions.add("Ice tiles by Phyromatical: https://www.deviantart.com/phyromatical", 370)
		self.instructions.increment = 10
		self.start_ticks = None

	def render(self):
		while self.instructions.opacity > 0:
			self.dt = self.game.clock.tick(FPS) / 1000
			self.handle_events(pygame.event.get())
			self.instructions.update()
			#keep the text at maximum opaqueness for longer
			if self.instructions.opacity > 250:
				if self.start_ticks == None:
					self.start_ticks=pygame.time.get_ticks() #starter tick
				seconds=(pygame.time.get_ticks()-self.start_ticks)/1000 #calculate how many seconds
				if seconds < 5:
					self.instructions.opacity = 255
				else:
					self.instructions.opacity = 250
			if self.instructions.opacity > 250:
				self.instructions.increment = 0;
			#speed up the fade away increment for the text
			elif self.instructions.increment < 0:
				self.instructions.increment = -10
			#draw background and text to screen
			self.game.screen.blit(self.background.image, self.background.rect)
			self.instructions.draw(self.game.screen)
			pygame.display.flip()

	def handle_events(self, events):
	    for event in events:
	        if event.type == pygame.QUIT:
	            pygame.quit()
	            sys.exit()

	def update(self):
		if self.instructions.opacity == 0:
			self.game.go_to(MainMenuScene(self.game))
		pass
