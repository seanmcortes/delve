import pygame
import sys
from os import path
from helper import *
from settings import *
from sprites import *
from menu import *


"""
Parent class for game scene.

Contains initialization of sprites/player, and functions to draw the game grid.
"""
class GameScene(object):
    def __init__(self):
        self.all_sprites = pygame.sprite.Group()
        self.player = Player(self, 0, 0)

    def render(self, screen):
        raise NotImplementedError

    def update(self):
        self.all_sprites.update()

    def handle_events(self, events):
        raise NotImplementedError

    def draw(self, screen):
        screen.fill(BGCOLOR)
        self.draw_grid(screen)
        self.all_sprites.draw(screen)

    def draw_grid(self, screen):
        for x in range(0, WIDTH, TILESIZE):
            pygame.draw.line(screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pygame.draw.line(screen, LIGHTGREY, (0, y), (WIDTH, y))


"""
Display Level 1

- Simple tutorial, show player how to move character and what the objectives of the game are.
"""
class Level1Scene(GameScene):
    def __init__(self):
        super().__init__()

    def render(self, screen):
        screen.fill(BLACK)
        self.draw(screen)
        self.draw_grid(screen)

    def update(self):
        pass

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


"""
Display the game over screen

Ask the user if they would like to continue and prompt with "yes" or "no"

    1. Yes (reload current level)
    2. No (exit to main menu)

"""
class GameOverScene(object):
    def __init__(self):
        super().__init__()

    def render(self, screen):
        text_to_screen(screen, "GAME OVER!", TITLE_FONT_PATH, 100, WHITE, WIDTH / 2, HEIGHT / 4)
        text_to_screen(screen, "Retry", TITLE_FONT_PATH, 25, WHITE, WIDTH / 2, HEIGHT / 2)
        text_to_screen(screen, "Save", TITLE_FONT_PATH, 25, WHITE, WIDTH / 2, HEIGHT / 1.75)
        text_to_screen(screen, "Main Menu", TITLE_FONT_PATH, 25, WHITE, WIDTH / 2, HEIGHT / 1.5)

    def update(self):
        pass

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
