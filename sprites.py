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

    def update(self):
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE


class Player(GameObject):
    def __init__(self, scene, x, y):
        super().__init__(scene, x, y)
        self.image.fill(ORANGE)

    def move(self, dx=0, dy=0):
        self.x += dx
        self.y += dy


class Wall(GameObject):
    def __init__(self, scene, x, y):
        super().__init__(scene, x, y)
        self.image.fill(LIGHTGREY)
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
