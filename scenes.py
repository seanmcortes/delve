import pygame
import sys
from os import path
from helper import *
from settings import *
from sprites import *
from map import create_tiles
from enemy import Enemy


"""
Parent class for game scene.

Contains initialization of sprites/player, and functions to draw the game grid.
"""
class GameScene(object):
    def __init__(self, game):
        self.all_sprites = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.blocks = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.ice = pygame.sprite.Group()
        self.player = None
        self.block = None
        self.game = game
        self.tile_map = create_tiles("level1.map")

    def render(self):
        self.game.screen.fill(BGCOLOR)
        self.game.screen.blit(self.tile_map, [0,0])
        self.draw_grid()
        self.all_sprites.draw(self.game.screen)
        self.players.draw(self.game.screen) #adding this so player is drawn on top of the ice tiles

    def update(self):
        self.all_sprites.update()

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            keyState = pygame.key.get_pressed()
            if self.player.sliding == False: #Ignore the directional key key presses if player is sliding on ice
                if keyState[pygame.K_w]:
                    if self.collision_ice(dx=0, dy=-1):
                        self.player.sliding = True
                    if not self.collision_wall(dx=0, dy=-1):
                        if not self.collision_block(dx=0, dy=-1):
                            self.player.move(dx=0, dy=-1)
                            self.player.orientation = UP
                        else:
                            self.player.move(dx=0, dy=-1)
                            self.block.move(dx=0, dy=-1)
                            self.player.orientation = UP
                if keyState[pygame.K_s]:
                    if self.collision_ice(dx=0, dy=1):
                        self.player.sliding = True
                    if not self.collision_wall(dx=0, dy=1):
                        if not self.collision_block(dx=0, dy=1):
                            self.player.move(dx=0, dy=1)
                            self.player.orientation = DOWN
                        else:
                            self.player.move(dx=0, dy=1)
                            self.block.move(dx=0, dy=1)
                            self.player.orientation = DOWN
                if keyState[pygame.K_a]:
                    if self.collision_ice(dx=-1, dy=0):
                        self.player.sliding = True
                    if not self.collision_wall(dx=-1, dy=0):
                        if not self.collision_block(dx=-1, dy=0):
                            self.player.move(dx=-1, dy=0)
                            self.player.orientation = LEFT
                        else:
                            self.player.move(dx=-1, dy=0)
                            self.block.move(dx=-1,dy=0)
                            self.player.orientation = LEFT
                if keyState[pygame.K_d]:
                    if self.collision_ice(dx=1, dy=0):
                        self.player.sliding = True
                    if not self.collision_wall(dx=1, dy=0):
                        if not self.collision_block(dx=1, dy=0):
                            self.player.move(dx=1, dy=0)
                            self.player.orientation = RIGHT
                        else:
                            self.player.move(dx=1, dy=0)
                            self.block.move(dx=1,dy=0)
                            self.player.orientation = RIGHT

    def collision_wall(self, dx, dy):
        for wall in self.walls:
            if wall.x == self.player.x + dx and wall.y == self.player.y + dy:
                return True
        return False

    def collision_ice(self, dx, dy):
        for ice in self.ice:
            if ice.x == self.player.x +dx and ice.y == self.player.y + dy:
                return True
        return False

    def collision_block(self, dx, dy):
        if self.block.x == self.player.x + dx and self.block.y == self.player.y +dy:
            return True
        return False

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pygame.draw.line(self.game.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pygame.draw.line(self.game.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw_layout(self, map_file):
        f = open(path.join(self.game.map_folder, map_file), "r")
        if f.mode == 'r':
            map = f.readlines()
            map = [item.strip() for item in map]
            for row, tiles in enumerate(map):
                for col, tile in enumerate(tiles):
                    if tile == 'W':
                        Wall(self, col, row)
                    if tile == 'P':
                        self.player = Player(self, col, row)
                    if tile == 'B':
                        self.block = Block(self, col, row)
                    if tile == 'i':
                        Ice(self, col, row)


"""
Display Level 1

- Simple tutorial, show player how to move character and what the objectives of the game are.
"""
class Level1Scene(GameScene):
    def __init__(self, game):
        super().__init__(game)
        self.draw_layout("level1object.map")


"""
Display tutorial level for enemies
"""
class TutorialEnemy(GameScene):
    def __init__(self, game):
        super().__init__(game)
        self.draw_layout("tutorialenemyobject.map")
        self.spawn_enemies()

    def spawn_enemies(self):
        Enemy(self, 18, 9, LEFT, [LEFT, LEFT, LEFT, LEFT, LEFT,
                                  DOWN, DOWN, DOWN,
                                  LEFT, LEFT, LEFT, LEFT])

        Enemy(self, 1, 18, RIGHT, [RIGHT, RIGHT, RIGHT, RIGHT, RIGHT,
                                   UP, UP, UP, UP,
                                   LEFT, LEFT, LEFT, LEFT,
                                   DOWN, DOWN, DOWN, DOWN])

        Enemy(self, 3, 3, UP, [RIGHT, RIGHT, RIGHT])
        self.block = Block(self, 10, 10)

"""
Display tutorial level for ice
"""
class TutorialIce(GameScene):
    def __init__(self, game):
        super().__init__(game)
        self.draw_layout("tutorialIceObjects.map")
        self.block = Block(self, 2, 10)



# Sources:
# https://github.com/kidscancode/pygame_tutorials/blob/master/tilemap/part%2007/main.py
# https://stackoverflow.com/questions/14700889/pygame-level-menu-states
