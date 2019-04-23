import pygame
import sys
from os import path
from helper import *
from settings import *
from sprites import *
#

"""
Parent class for game scene.

Contains initialization of sprites/player, and functions to draw the game grid.
"""
class GameScene(object):
    def __init__(self, game):
        self.all_sprites = pygame.sprite.Group()
        self.game = game

        self.player = Player(self, 10, 10)

        for x in range(0, 20):
            Wall(self, x, 0)
            Wall(self, x, 19)

        for y in range(0, 20):
            Wall(self, 0, y)
            Wall(self, 19, y)

    def render(self):
        raise NotImplementedError

    def update(self):
        self.all_sprites.update()

    def handle_events(self, events):
        raise NotImplementedError

    def draw(self):
        self.game.screen.fill(BGCOLOR)
        self.draw_grid()
        self.all_sprites.draw(self.game.screen)

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pygame.draw.line(self.game.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pygame.draw.line(self.game.screen, LIGHTGREY, (0, y), (WIDTH, y))


"""
Display Level 1

- Simple tutorial, show player how to move character and what the objectives of the game are.
"""
class Level1Scene(GameScene):
    def __init__(self, game):
        super().__init__(game)

    def render(self):
        self.game.screen.fill(BLACK)
        self.draw()
        self.draw_grid()

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
