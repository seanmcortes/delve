import pygame
import pygame.freetype
import sys
import random
from os import path
from os import remove # to delete corrupted save files
from settings import *
from helper import *
from os import listdir #for file handling
from os.path import isfile, join #for file handling
import datetime #for getting the time for the save files
#################################################################################################
# Background class for the menu scenes
# Arguments: the file, and the x,y cordinates on the screen
# Source: https://stackoverflow.com/questions/28005641/how-to-add-a-background-image-into-pygame
#################################################################################################
class Background(pygame.sprite.Sprite):
	def __init__(self, image_file, location):
		pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
		self.image = pygame.image.load(image_file)
		self.rect = self.image.get_rect()
		self.rect.left, self.rect.top = location
		self.opacity = 255 #use with blit_alpha function to make image partially transparent

	#################################################################################################
	# Makes the Background partially transparent based on the self.opacity variablle
	# Arguments: the screen the background will be blitted to
	# Source: https://nerdparadise.com/programming/pygameblitopacity
	#################################################################################################
	def blit_alpha(self, screen):
		x = 0
		y = 0
		temp = pygame.Surface((self.image.get_width(), self.image.get_height())).convert()
		temp.blit(screen, (-x, -y))
		temp.blit(self.image, (0, 0))
		temp.set_alpha(self.opacity)
		screen.blit(temp, [x, y])

#################################################################################################
# Class for buttons on the menu
# Arguments: The Game object, the message that will be displayed on the button, the coordinates,
# an optional function name that the button will execute, an optional argument that can be passed
# to that function
#################################################################################################
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
		self.sound = pygame.mixer.Sound(path.join(MUSIC_FOLDER,"button.wav"))
		self.sound.set_volume(.05)

	#################################################################################################
	# Stores the three images that are used for the buttons
	# The normal image is used when not interacting with the button, the hover image is used when
	# the mouse is hovering over the button, and the click image is used when the button has been
	# clicked
	#################################################################################################
	class img_holder():
		def __init__(self):
			self.normal = pygame.image.load(path.join(IMAGE_FOLDER,'button_normal.png'))
			self.hover = pygame.image.load(path.join(IMAGE_FOLDER,'button_hover.png'))
			self.click = pygame.image.load(path.join(IMAGE_FOLDER,'button_click.png'))
	#################################################################################################
	# Handles keyboard and mouse inputs for the button
	#################################################################################################
	def handle_events(self):
		mouse = pygame.mouse.get_pos()
		click = pygame.mouse.get_pressed()
		#test if the mouse is over the button
		if self.x + self.w > mouse[0] > self.x and self.y + self.h > mouse[1] > self.y:
		    self.image = self.img.hover
			# when the button is clicked
		    if click[0] == 1 and self.action != None:
		        pygame.mixer.Sound.play(self.sound)
		        self.image = self.img.click
		        self.CLICKED = True
		        self.NORMAL = False
		#set the image to normal if the user is not interacting with the button
		else:
		   	self.image = self.img.normal

		return None
	#################################################################################################
	# Update function for the button. Changes the button from the clicked image to the normal image
	# after the button has been clicked
	#################################################################################################
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
	#################################################################################################
	# Draws the button to the screen
	#################################################################################################
	def draw(self):
	        self.screen.blit(self.image, self.rect)
	        self.text.render(self.screen)

#####################################################################################################
# Display the main menu screen.
# Allow the user to perform the following options:
#    1. Start the game from level 1
#    2. Call the load game screen
#    3. Quit the game
#    4. Show the credits screen
# Arguments: a copy of the Game object
#####################################################################################################
class MainMenuScene():
	def __init__(self, game):
		self.game = game
		self.text_logo = TextObject("DELVE", path.join(IMAGE_FOLDER, 'CuteFont-Regular.ttf'), 175, WHITE, WIDTH / 2, HEIGHT / 4)
		logo_shadow = TextObject("DELVE", path.join(IMAGE_FOLDER, 'CuteFont-Regular.ttf'), 175, BLACK, WIDTH / 2+1, HEIGHT / 4+1)
		self.textObjects = [logo_shadow, self.text_logo]
		self.all_buttons = []
		self.background = Background(path.join(IMAGE_FOLDER, 'menuback.png'), [0,0])
		self.button1 = MenuButton(self.game, "Play", [140,400], self.playgame)
		self.button2 = MenuButton(self.game, "Load", [270,400], self.loadgamescreen)
		self.button3 = MenuButton(self.game, "Quit", [400,400], self.quitgame)
		self.button4 = MenuButton(self.game, "Credits", [270,460], self.show_credits)
		self.all_buttons.append(self.button1)
		self.all_buttons.append(self.button2)
		self.all_buttons.append(self.button3)
		self.all_buttons.append(self.button4)
	#####################################################################################################
	# Render the menu and buttons to the screen, and call a buttons action if it has been clicked
	#####################################################################################################
	def render(self):
		self.dt = self.game.clock.tick() / 1000
		#self.game.screen.fill(BLACK)
		self.game.screen.blit(self.background.image, self.background.rect)
		for t in self.textObjects:
			t.render(self.game.screen)

		for p in self.all_buttons:
			p.draw()
		#test if a button has been clicked, and call the buttons action if it has
		for p in self.all_buttons:
			if p.CLICKED == True:
				pygame.display.flip()
				pygame.time.delay(100)
				p.update()
				p.draw()
				pygame.display.flip()
				pygame.time.delay(250)
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
		self.game.select_scene(1)

	def loadgamescreen(self):
		self.game.go_to(LoadGameScene(self.game))

	def mainmenu(self):
		self.game.go_to(MainMenuScene(self.game))

	def loadlevel(self, level):
		self.game.select_scene(level)


	def savegame(self):
			saveScreen = SaveGameScene(self.game)
			saveScreen.loop()

	def savelevel(self, file_name):
		f = open(path.join(SAVE_FOLDER, file_name),"w+")
		scene_str = encrypt(self.game)
		f.write(scene_str)
		f.close()
		self.WAITING = False #exit the save screen

	def restartlevel(self):
		self.loadlevel(self.game.scene.scene_number)
		self.unpause()

	def show_credits(self):
		credits_screen = CreditScene(self.game)
		credits_screen.render()

	########################################################################################
	# Event listener for main menu.
	#########################################################################################
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

#####################################################################################################
# Display the game over screen
# Ask the user if they would like to continue and prompt with "yes" or "no"
#    1. Yes (reload current level)
#    2. No (exit to main menu)
# Parent: MainMenuScene
# Arguments: a copy of the Game object
#####################################################################################################
class GameOverScene(MainMenuScene):
	def __init__(self, game):
		#super().__init__(game)
		current_scene = game.scene.scene_number
		self.game = game
		self.background = Background(path.join(IMAGE_FOLDER,'gameoverback.png'), [0,0])
		self.text_logo1 = TextObject("GAME OVER", path.join(IMAGE_FOLDER, 'CuteFont-Regular.ttf'), 100, BLACK, WIDTH / 2-1, HEIGHT / 4-1)
		self.text_logo2 = TextObject("GAME OVER", path.join(IMAGE_FOLDER, 'CuteFont-Regular.ttf'), 100, BLACK, WIDTH / 2+1, HEIGHT / 4+1)
		self.text_logo3 = TextObject("GAME OVER", path.join(IMAGE_FOLDER, 'CuteFont-Regular.ttf'), 100, BLACK, WIDTH / 2+1, HEIGHT / 4-1)
		self.text_logo4 = TextObject("GAME OVER", path.join(IMAGE_FOLDER, 'CuteFont-Regular.ttf'), 100, BLACK, WIDTH / 2-1, HEIGHT / 4+1)
		self.text_logo5 = TextObject("GAME OVER", path.join(IMAGE_FOLDER, 'CuteFont-Regular.ttf'), 100, WHITE, WIDTH / 2, HEIGHT / 4)
		logo_shadow = TextObject("GAME OVER", path.join(IMAGE_FOLDER, 'CuteFont-Regular.ttf'), 100, BLACK, WIDTH / 2+1, HEIGHT / 4+1)
		self.text_message1 = TextObject("Would you like to continue?", path.join(IMAGE_FOLDER, 'CuteFont-Regular.ttf'), 50, BLACK, WIDTH / 2-1, (HEIGHT / 3)+50-1)
		self.text_message2 = TextObject("Would you like to continue?", path.join(IMAGE_FOLDER, 'CuteFont-Regular.ttf'), 50, BLACK, WIDTH / 2+1, (HEIGHT / 3)+50+1)
		self.text_message3 = TextObject("Would you like to continue?", path.join(IMAGE_FOLDER, 'CuteFont-Regular.ttf'), 50, BLACK, WIDTH / 2-1, (HEIGHT / 3)+50+1)
		self.text_message4 = TextObject("Would you like to continue?", path.join(IMAGE_FOLDER, 'CuteFont-Regular.ttf'), 50, BLACK, WIDTH / 2+1, (HEIGHT / 3)+50-1)
		self.text_message5 = TextObject("Would you like to continue?", path.join(IMAGE_FOLDER, 'CuteFont-Regular.ttf'), 50, WHITE, WIDTH / 2, (HEIGHT / 3)+50)
		self.textObjects = [logo_shadow, self.text_logo1, self.text_logo2, self.text_logo3, self.text_logo4, self.text_logo5,
							self.text_message1, self.text_message2, self.text_message3, self.text_message4, self.text_message5]
		self.button1 = MenuButton(self.game, "Yes", [270,350], self.loadlevel, current_scene)
		self.button2 = MenuButton(self.game, "No", [270,425], self.mainmenu)
		self.all_buttons = [self.button1, self.button2]
#####################################################################################################
# Display the Load Game screen
# Displays up to three saved games
# Parent: MainMenuScene
# Arguments: a copy of the Game object
#####################################################################################################
class LoadGameScene(MainMenuScene):
	def __init__(self, game):
		self.game = game
		self.background = Background(path.join(IMAGE_FOLDER, 'menuback.png'), [0,0])
		self.text_logo = TextObject("Load Game", path.join(IMAGE_FOLDER, 'CuteFont-Regular.ttf'), 100, WHITE, WIDTH / 2, HEIGHT / 4)
		logo_shadow = TextObject("Load Game", path.join(IMAGE_FOLDER, 'CuteFont-Regular.ttf'), 100, BLACK, WIDTH / 2+1, HEIGHT / 4+1)
		self.textObjects = [logo_shadow, self.text_logo]
		self.button1 = MenuButton(self.game, "Back", [270,450], self.mainmenu)
		self.all_buttons = [self.button1]
		#Source: https://stackoverflow.com/questions/3207219/how-do-i-list-all-files-of-a-directory
		#gets only files not any directories
		y = 250
		count = 0
		files = [f for f in listdir(SAVE_FOLDER) if isfile(join(SAVE_FOLDER, f))]
		for file_name in files:
				f = open(join(SAVE_FOLDER, file_name), "r")
				if f.mode == 'r' and count < 3:
					file_list = list(f.read())
					number, date = decrypt(file_list)
					if isinstance(number, int): #to do: make sure number is an actual level
						if (number < 10):
							save_text = "Level:   " + str(number) + " Time: " + date
						else:
							save_text = "Level: " + str(number) + " Time: " + date
						self.textObjects.append(TextObject(save_text, path.join(IMAGE_FOLDER, 'CuteFont-Regular.ttf'), 30, WHITE, 210, y+14, "left"))
						self.all_buttons.append(MenuButton(self.game, "Load", [100, y], self.loadlevel, number))
						y += 60
						count += 1
					f.close()
#####################################################################################################
# Display the Save Game screen
# Allows up to three saved games
# Parent: MainMenuScene
# Arguments: a copy of the Game object
#####################################################################################################
class SaveGameScene(MainMenuScene):
	def __init__(self, game):
		#super().__init__(game)
		self.game = game
		self.background = Background(path.join(IMAGE_FOLDER, 'menuback.png'), [0,0])
		self.text_logo = TextObject("Pause Menu", path.join(IMAGE_FOLDER, 'CuteFont-Regular.ttf'), 100, WHITE, WIDTH / 2, HEIGHT / 4)
		logo_shadow = TextObject("Pause Menu", path.join(IMAGE_FOLDER, 'CuteFont-Regular.ttf'), 100, BLACK, WIDTH / 2+1, HEIGHT / 4+1)
		self.textObjects = [logo_shadow, self.text_logo]
		self.button1 = MenuButton(self.game, "Back", [270,550], self.stopwaiting)
		self.all_buttons = [self.button1]
		self.WAITING = False #wait for the player to save or quit the save game screen
		#Source: https://stackoverflow.com/questions/3207219/how-do-i-list-all-files-of-a-directory
		#gets only files not any directories
		y = 250
		count = 0
		files = [f for f in listdir(SAVE_FOLDER) if isfile(join(SAVE_FOLDER, f))]
		for file_name in files:
				f = open(join(SAVE_FOLDER, file_name), "r")
				if f.mode == 'r' and count < 3:
					file_list = list(f.read())
					number, date = decrypt(file_list)
					if isinstance(number, int): #to do: make sure number is an actual level
						if (number < 10):
							save_text = "Level:   " + str(number) + " Time: " + date
						else:
							save_text = "Level: " + str(number) + " Time: " + date
						self.textObjects.append(TextObject(save_text, path.join(IMAGE_FOLDER, 'CuteFont-Regular.ttf'), 30, WHITE, 210, y+14, "left"))
						self.all_buttons.append(MenuButton(self.game, "Save", [100, y], self.savelevel, file_name))
						y += 60
						count += 1
				f.close()
		while count < 3: #create more save files if there are some that do no exist
			file_num = 1
			temp_name = str(file_num) + ".sav"
			while isfile(join(SAVE_FOLDER, temp_name)): #loop until finding a filename that does not exist
				file_num += 1
				temp_name = str(file_num) + ".sav"
			self.all_buttons.append(MenuButton(self.game, "Save", [100, y], self.savelevel, temp_name))
			y += 60
			count += 1

	#####################################################################################################
	# This causes the gameplay to pause and loops the Save Game screen while waiting for player input
	#####################################################################################################
	def loop(self):
		self.WAITING = True
		while self.WAITING:
			self.dt = self.game.clock.tick() / 1000
			self.handle_events(pygame.event.get())
			self.update()
			self.render()
			pygame.display.flip()
	#####################################################################################################
	# Sets the WAITING variable to false so the loop function terminates.  Called by button actions
	#####################################################################################################
	def stopwaiting(self):
		self.WAITING = False

#####################################################################################################
# Display the Pause Menu
# Allows the player to click buttons to perform actions
#   1. Go to the Save Game menu
#   2. Go to the main menu
#   3. Restart the level
#   4. Unpause and return to the game
# Parent: MainMenuScene
# Arguments: a copy of the Game object
#####################################################################################################
class PauseScene(MainMenuScene):
	def __init__(self, game):
		#super().__init__(game)
		self.game = game
		self.background = Background(path.join(IMAGE_FOLDER, 'menuback.png'), [0,0])
		self.text_logo = TextObject("Pause Menu", path.join(IMAGE_FOLDER, 'CuteFont-Regular.ttf'), 100, WHITE, WIDTH / 2, HEIGHT / 4)
		logo_shadow = TextObject("Pause Menu", path.join(IMAGE_FOLDER, 'CuteFont-Regular.ttf'), 100, BLACK, WIDTH / 2+1, HEIGHT / 4+1)
		self.textObjects = [logo_shadow, self.text_logo]
		self.button1 = MenuButton(self.game, "Back to Game", [270,250], self.unpause)
		self.button2 = MenuButton(self.game, "Save Game", [270,325], self.savegame)
		self.button3 = MenuButton(self.game, "Restart Level", [270,400], self.restartlevel)
		self.button4 = MenuButton(self.game, "Main Menu", [270,475], self.mainmenu)
		self.all_buttons = [self.button1, self.button2, self.button3, self.button4]
		save_path = 'save'
	#####################################################################################################
	# This causes the gameplay to pause and loops the Pause screen while waiting for player input
	#####################################################################################################
	def paused(self):
		self.PAUSED = True
		while self.PAUSED:
			self.dt = self.game.clock.tick() / 1000
			self.handle_events(pygame.event.get())
			self.update()
			self.render()
			pygame.display.flip()
	#####################################################################################################
	# Sets the PAUSED variable to False so that the paused function breaks the loop
	#####################################################################################################
	def unpause(self):
		self.PAUSED = False
	#####################################################################################################
	# Override of mainmenu submethod from the MainMenu scene.  This is called by the Main Menu button
	#####################################################################################################
	def mainmenu(self):
			self.unpause()
			self.game.go_to(MainMenuScene(self.game))
#####################################################################################################
# Display the Credits Scene
# This displays the credits to the screen as test.  The text fades in, fades out, then returns to
# the previous screen
# Parent: MainMenuScene
# Arguments: a copy of the Game object
#####################################################################################################
class CreditScene(MainMenuScene):
	def __init__(self, game):
		self.game = game
		self.background = Background(path.join(IMAGE_FOLDER, 'menuback.png'), [0,0])
		#self.textObjects = [TextObject("Credits", path.join(IMAGE_FOLDER, 'CuteFont-Regular.ttf'), 50, BLACK, WIDTH / 2 + 1, HEIGHT / 4 + 1),
		#					TextObject("Credits", path.join(IMAGE_FOLDER, 'CuteFont-Regular.ttf'), 50, WHITE, WIDTH / 2, HEIGHT / 4)]
		self.instructions = Instructions(20, WHITE)
		self.instructions.rows.append(TextObject("Credits", path.join(IMAGE_FOLDER, 'CuteFont-Regular.ttf'), 100, BLACK, WIDTH / 2 + 1, 60 + 1))
		self.instructions.rows.append(TextObject("Credits", path.join(IMAGE_FOLDER, 'CuteFont-Regular.ttf'), 100, WHITE, WIDTH / 2, 60))
		self.instructions.rows.append(TextObject("Developers:", path.join(IMAGE_FOLDER, 'CuteFont-Regular.ttf'), 40, BLACK, WIDTH / 2 + 1, 120+ 1))
		self.instructions.rows.append(TextObject("Sean Cortes", path.join(IMAGE_FOLDER, 'CuteFont-Regular.ttf'), 36, BLACK, WIDTH / 2 + 1, 150+ 1))
		self.instructions.rows.append(TextObject("Jason Anderson:", path.join(IMAGE_FOLDER, 'CuteFont-Regular.ttf'), 36,BLACK, WIDTH / 2 + 1, 180+ 1))
		self.instructions.rows.append(TextObject("Joshua Nutt", path.join(IMAGE_FOLDER, 'CuteFont-Regular.ttf'), 36, BLACK, WIDTH / 2 + 1, 210+ 1))
		self.instructions.rows.append(TextObject("Developers:", path.join(IMAGE_FOLDER, 'CuteFont-Regular.ttf'), 40, WHITE,  WIDTH / 2, 120))
		self.instructions.rows.append(TextObject("Sean Cortes", path.join(IMAGE_FOLDER, 'CuteFont-Regular.ttf'), 36, WHITE,  WIDTH / 2, 150))
		self.instructions.rows.append(TextObject("Jason Anderson:", path.join(IMAGE_FOLDER, 'CuteFont-Regular.ttf'), 36, WHITE,  WIDTH / 2, 180))
		self.instructions.rows.append(TextObject("Joshua Nutt", path.join(IMAGE_FOLDER, 'CuteFont-Regular.ttf'), 36, WHITE,  WIDTH / 2, 210))
		self.instructions.add("Ice tiles by Phyromatical | https://www.deviantart.com/phyromatical", 240)
		self.instructions.add("Game over screen background vector created by kjpargeterat | www.freepik.com", 270)
		self.instructions.add("Treasure chest sprite by goo30 | www.opengameart.org | License: CC0 1.0", 300)
		self.instructions.add("Free fantasy GUI by pzUH | www.opengameart.org | License: CC0 1.0", 330)
		self.instructions.add("Click2 sound created by Sebastian | www.soundbible.com | License: CC BY 3.0", 360)
		self.instructions.add("Rock Scrape 2.wav by Benboncan | License: CC BY 3.0", 390)
		self.instructions.add("https://freesound.org/people/Benboncan/sounds/74441/ | Edits: Silence trimmed, volume adjusted", 410)
		self.instructions.add("Game sound by chris_schum | | License: CC0 |", 440)
		self.instructions.add("https://freesound.org/people/chris_schum/sounds/418149/ | Edits: Silence trimmed, volume adjusted", 460)
		self.instructions.add("Retro Game sfx_jump bump.wav by mikala_oidua | License: CC0", 490)
		self.instructions.add("https://freesound.org/people/mikala_oidua/sounds/365672/ | Edits: Silence trimmed, volume adjusted", 510)
		self.instructions.add("Metal sound, fighting game by evilus | License: CC0", 540)
		self.instructions.add("https://freesound.org/people/evilus/sounds/203454/ | Edits: Silence trimmed, volume adjusted" , 560)
		self.instructions.add("Game Over Sound by TheZero | License: License: CC0", 590)
		self.instructions.add("https://freesound.org/people/TheZero/sounds/368367/ | Edited to remove noise artifacts", 610)





		self.incrementvalue = 10
		self.instructions.increment = self.incrementvalue
		self.start_ticks = None
		self.exit = True #used to record key presses to exit
	#####################################################################################################
	# Draws the credits to the screen
	# This function updates the opacity of the test on the screen to make the text fade in and then
	# fade out
	#####################################################################################################
	def render(self):
		seconds = -1 #create the second variable
		while self.instructions.opacity > 0:
			self.dt = self.game.clock.tick() / 1000
			self.handle_events(pygame.event.get())
			self.instructions.update()
			#keep the text at maximum opaqueness for longer
			if self.instructions.opacity > 250:
				if self.start_ticks == None:
					if self.__class__.__name__ == "VictoryScene":
						self.exit = False #force game to wait for keypress in handle events to exit
					self.start_ticks=pygame.time.get_ticks() #starter tick
				seconds=(pygame.time.get_ticks()-self.start_ticks)/1000 #calculate how many seconds
				if seconds < 5 or self.exit == False: #player will have to hit a key to set self.exit to true on VictoryScene
					self.instructions.opacity = 255
				else:
					self.instructions.opacity = 250
			if self.instructions.opacity > 250:
				self.instructions.increment = 0;
			#speed up the fade away increment for the text
			elif self.instructions.increment < 0:
				self.instructions.increment = -1* self.incrementvalue
			#draw background and text to screen
			if self.__class__.__name__ == "CreditScene":
				self.game.screen.blit(self.background.image, (0,0))
			elif seconds > 4:
				self.background.blit_alpha(self.game.screen)
				if self.background.opacity > 255:
					self.background.opacity = 255
				elif self.background.opacity < 255:
					self.background.opacity += 1

			self.instructions.draw(self.game.screen)
			pygame.display.flip()

	#####################################################################################################
	# Event listerner for the Credits scene
	#####################################################################################################
	def handle_events(self, events):
		for event in events:
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			# if the player clicks a button on the mouse, set the exit variable to true to go to the next
			# Only used for the VictoryScene class
			else:
				self.exit = True

	#####################################################################################################
	# Go back to the Main Menu after the opacity of the text has returned to zero
	#####################################################################################################
	def update(self):
		if self.instructions.opacity == 0:
			#blit the background one more time to get rid of transparent text
			self.dt = self.game.clock.tick() / 1000
			self.game.screen.blit(self.background.image, (0,0))
			pygame.display.flip()

			#delay the game before going to next scene
			seconds = 0
			start_ticks=pygame.time.get_ticks() #starter tick
			while seconds < 1:
				self.handle_events(pygame.event.get())
				seconds=(pygame.time.get_ticks()-start_ticks)/1000 #calculate how many seconds
			self.game.go_to(MainMenuScene(self.game))
#####################################################################################################
# Display the Victory Scene after the player beats the game
# This displays the message to the screen as test.  The text fades in, fades out, then returns to
# the previous screen
# Parent: CreditScene
# Arguments: a copy of the Game object
#####################################################################################################
class VictoryScene(CreditScene):
	def __init__(self, game):
		super().__init__(game)
		self.background.opacity = 10
		self.instructions = Instructions(50, WHITE)
		self.instructions.rows.append(TextObject("Congratulations", path.join(IMAGE_FOLDER, 'CuteFont-Regular.ttf'), 100, BLACK, WIDTH / 2+1, HEIGHT / 2.5+1))
		self.instructions.rows.append(TextObject("Congratulations", path.join(IMAGE_FOLDER, 'CuteFont-Regular.ttf'), 100, WHITE, WIDTH / 2, HEIGHT / 2.5))
		self.instructions.add("You have found the treasure!", 350)
		self.instructions.increment = 10
		self.start_ticks = None
		self.exit = False #used to record key presses to exit

#################################################################################################
# Creates and returns a random string to pad the beginning and ending of the save files
# Returns: the random string
#################################################################################################
def randomString():
	random_str = ""
	count = random.randint(20,51)
	for x in range(count):
		number = random.randint(0,13) # select a number from 0 to 13
		random_str = random_str + chr((number + (random.randint(0,5) * 15)) + 32)
	#add a newline character at the end
	newline = 14
	random_str = random_str + chr((newline + (random.randint(0,5) * 15)) + 32)
	return random_str

#################################################################################################
# Encrypts the current level and datetime to store in the save files
# Arguments: A copy of the game object
# Returns: The encrypted string
#################################################################################################
def encrypt(game):
	#get current Time so it can be converted to a formated date
	#Source: https://stackoverflow.com/questions/415511/how-to-get-the-current-time-in-python
	#Source: https://stackoverflow.com/questions/311627/how-to-print-a-date-in-a-regular-format
	current_time = datetime.datetime.now()
	text_list = list(str(game.scene.scene_number) + "\n" + current_time.strftime('%m/%d/%Y, %H:%M:%S') + "\n")
	scene_str = randomString()
	for letter in text_list:
		if letter == " " :
			number = 10
		elif letter == ',' :
			number = 11
		elif letter == ':':
			number = 12
		elif letter == '/':
			number = 13
		elif letter == '\n':
			number = 14
		else:
			number = ord(letter)-48 #convert character number to string
		scene_str = scene_str + chr((number + (random.randint(0,5) * 15)) + 32)
	scene_str = scene_str + randomString()
	return scene_str
#################################################################################################
# Decrypts the text stored in the save files
# Arguments:The input of the file stored as a list
# Returns: The level number and the time the game was saved at
#################################################################################################
def decrypt(file_list):
	file_str = ""
	for char in file_list:
		#scene_str = scene_str + chr((number + (random.randint(1,6) * 15)) + 32)
		number = (ord(char) - 32) % 15
		if number == 10:
			letter = " "
		elif number == 11:
			letter = ','
		elif number == 12:
			letter = ':'
		elif number == 13:
			letter = '/'
		elif number == 14:
			letter = '\n'
		else:
			letter = chr(number+48) #convert character number to string
		file_str = file_str + letter
	junk1, number, date, junk2, junk3 = file_str.split('\n')
	try:
		number = int(number)
	except:
		number = "Not an integer"
	return number, date
