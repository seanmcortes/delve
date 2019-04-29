import pygame
from settings import *

class GameObject(pygame.sprite.Sprite):
    def __init__(self, scene, x, y):
        self.groups = scene.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.scene = scene
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.interactable = False
        self.collidable = False
        self.orientation = None

    def update(self):
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE

class Player(GameObject):
    def __init__(self, scene, x, y):
        super().__init__(scene, x, y)
        self.groups = scene.all_sprites, scene.player
        self.image.fill(ORANGE)
        self.orientation = RIGHT

    def move(self, dx=0, dy=0):
        self.x += dx
        self.y += dy

class Block(GameObject):
  def __init__(self, scene, x, y):
      super().__init__(scene, x, y)
      self.groups = scene.all_sprites, scene.block
      self.image.fill(BLUE)
      self.interactable = True

  def move(self, dx=0, dy=0):
        self.x += dx
        self.y += dy

class Wall(GameObject):
    def __init__(self, scene, x, y):
        super().__init__(scene, x, y)
        self.groups = scene.all_sprites, scene.walls
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image.fill(LIGHTGREY)
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


"""
Sources:
https://github.com/kidscancode/pygame_tutorials/blob/master/tilemap/part%2002/sprites.py
"""
