import pygame
import sys
from os import path
from helper import *
from settings import *
from sprites import *
from map import create_tiles
from enemy import Enemy
#

"""
Parent class for game scene.

Contains initialization of sprites/player, and functions to draw the game grid.
"""
class GameScene(object):
    def __init__(self, game):
        self.all_sprites = pygame.sprite.Group()
        self.player = None
        self.walls = pygame.sprite.Group()
        self.game = game
        self.tile_map = create_tiles("level1.map")
        self.layout = [
            "WWWWWWWWWWWWWWWWWWWW",
            "WP.................W",
            "W..................W",
            "W..................W",
            "W..................W",
            "W..................W",
            "W..................W",
            "W..................W",
            "W..................W",
            "W..................W",
            "W..................W",
            "W..................W",
            "W..................W",
            "W..................W",
            "W..................W",
            "W..................W",
            "W..................W",
            "W..................W",
            "W..................W",
            "WWWWWWWWWWWWWWWWWWWW"
        ]

    def render(self):
        self.game.screen.fill(BGCOLOR)
        self.game.screen.blit(self.tile_map, [0,0])
        self.draw_grid()
        self.all_sprites.draw(self.game.screen)

    def update(self):
        self.all_sprites.update()

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            keyState = pygame.key.get_pressed()
            if keyState[pygame.K_w]:
                if not self.collision_wall(dx=0, dy=-1):
                    self.player.move(dx=0, dy=-1)
            if keyState[pygame.K_s]:
                if not self.collision_wall(dx=0, dy=1):
                    self.player.move(dx=0, dy=1)
            if keyState[pygame.K_a]:
                if not self.collision_wall(dx=-1, dy=0):
                    self.player.move(dx=-1, dy=0)
            if keyState[pygame.K_d]:
                if not self.collision_wall(dx=1, dy=0):
                    self.player.move(dx=1, dy=0)
        
    def collision_wall(self, dx, dy):
        for wall in self.walls:
            if wall.x == self.player.x + dx and wall.y == self.player.y + dy:
                return True
        return False

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pygame.draw.line(self.game.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pygame.draw.line(self.game.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw_layout(self):
        for row, tiles in enumerate(self.layout):
            for col, tile in enumerate(tiles):
                if tile == 'W':
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
    # https://github.com/kidscancode/pygame_tutorials/blob/master/tilemap/part%2007/main.py


"""
Display Level 1

- Simple tutorial, show player how to move character and what the objectives of the game are.
"""
class Level1Scene(GameScene):
    def __init__(self, game):
        super().__init__(game)
        self.draw_layout()

"""
Display tutorial level for enemies
"""
class TutorialEnemy(GameScene):
    def __init__(self, game):
        super().__init__(game)
        self.enemy = Enemy(self, 18, 9, LEFT, [DOWN, LEFT])
        self.enemy = Enemy(self, 1, 18, RIGHT, [UP, LEFT, DOWN])
        self.layout = [
            "WWWWWWWWWWWWWWWWWWWW",
            "W.P................W",
            "W..................W",
            "W..................W",
            "W..................W",
            "W...........WWW....W",
            "W...........W.W....W",
            "W...........W.W....W",
            "W...........W.WWWWWW",
            "W...........W......W",
            "W...........W.WWWWWW",
            "W.......WWWWW.W....W",
            "W.......W.....W....W",
            "W.......WWWWWWW....W",
            "W..................W",
            "W..................W",
            "W..................W",
            "W..................W",
            "W..................W",
            "WWWWWWWWWWWWWWWWWWWW"
        ]

"""
Sources:
https://github.com/kidscancode/pygame_tutorials/blob/master/tilemap/part%2007/main.py
"""
