import pygame
import pygame.freetype
import sys
from os import path
from settings import *
from sprites import *
from scenes import *

class Game:
	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
		pygame.display.set_caption(TITLE)
		self.clock = pygame.time.Clock()
		pygame.key.set_repeat(500, 100)
		self.manager = SceneManager()

	def run(self):
		self.playing = True
		while self.playing:
			self.dt = self.clock.tick(FPS) / 1000
			self.manager.scene.handle_events(pygame.event.get())
			self.manager.scene.update()
			self.manager.scene.render(self.screen)
			pygame.display.flip()


def main():
	g = Game()

	while True:
		g.run()


if __name__ == "__main__":
	main()