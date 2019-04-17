import pygame
import pygame.freetype
import sys
from os import path
from settings import *
from sprites import *

class Game:
	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
		pygame.display.set_caption(TITLE)
		self.clock = pygame.time.Clock()
		pygame.key.set_repeat(500, 100)


	def new(self):
		self.all_sprites = pygame.sprite.Group()
		self.player = Player(self, 10, 10)


	def run(self):
		self.playing = True
		while self.playing:
			self.dt = self.clock.tick(FPS) / 1000
			self.events()
			self.update()
			self.draw()


	def update(self):
		self.all_sprites.update()


	def quit(self):
		pygame.quit()
		sys.exit()


	def draw_grid(self):
		for x in range(0, WIDTH, TILESIZE):
			pygame.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
		for y in range(0, HEIGHT, TILESIZE):
			pygame.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))


	def draw(self):
		self.screen.fill(BGCOLOR)
		self.draw_grid()
		self.all_sprites.draw(self.screen)
		pygame.display.flip()


	def events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.quit()


	def load_data(self):
		image_folder = path.join(path.dirname(__file__), 'image')
		self.title_font_path = path.join(image_folder, 'CuteFont-Regular.ttf')	# get path for cutefont
	

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
	def text_to_screen(self, text, path, size, color, x=0, y=0, align="center"):
		self.font = pygame.freetype.Font(path, size)
		text_surface, rect = self.font.render(text, color)
		text_rect = text_surface.get_rect()

		if align == "center":
			text_rect.center = (x, y)

		self.screen.blit(text_surface, text_rect)
	# https://stackoverflow.com/questions/20842801/how-to-display-text-in-pygame

	"""
	Display the main menu screen.

	Allow the user to perform the following options:
	1. Start the game from level 1
	2. Load a saved file
	3. Exit the game
	"""
	def run_main_menu(self):
		pass


	"""
	Display the game over screen

	Ask the user if they would like to continue and prompt with "yes" or "no"
	1. Yes (reload current level)
	2. No (exit to main menu)
	"""
	def run_game_over(self):
		self.playing_game_over = True
		while self.playing_game_over:
			self.dt = self.clock.tick(FPS) / 1000
			self.events_game_over()
			self.draw_game_over()


	"""
	Fill screen and display text for game over screen. 
	"""
	def draw_game_over(self):
		self.screen.fill(BLACK)
		self.text_to_screen("GAME OVER!", self.title_font_path, 100, WHITE, WIDTH / 2, HEIGHT / 4)
		self.text_to_screen("Retry", self.title_font_path, 25, WHITE, WIDTH / 2, HEIGHT / 2)
		self.text_to_screen("Save", self.title_font_path, 25, WHITE, WIDTH / 2, HEIGHT / 1.75)
		self.text_to_screen("Main Menu", self.title_font_path, 25, WHITE, WIDTH / 2, HEIGHT / 1.5)
		pygame.display.flip()
	

	"""
	Event listener for game over screen.
	"""
	def events_game_over(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					self.run()


g = Game()
g.load_data()

while True:
	g.new()
	g.run_main_menu()
	g.run_game_over()