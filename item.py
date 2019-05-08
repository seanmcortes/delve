import pygame
from sprites import GameObject, SpriteSheet
from settings import KEY_SPRITESHEET, INVENTORY_SPRITESHEET, TILESIZE


class Inventory(GameObject):
    def __init__(self, scene, x, y):
        super().__init__(scene, x, y)
        self.groups = scene.all_sprites, scene.hud
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.sprite_sheet = SpriteSheet(INVENTORY_SPRITESHEET)
        self.image = self.sprite_sheet.get_image(0, 0, 32, 32)
        self.item_list = []

    def update(self):
        if len(self.item_list) > 0:
            if type(self.item_list[0]) == Key:
                self.image = self.sprite_sheet.get_image(0, 32, 32, 32)

        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE


class Item(GameObject):
    def __init__(self, scene, x, y):
        super().__init__(scene, x, y)
        self.groups = scene.all_sprites, scene.items
        pygame.sprite.Sprite.__init__(self, self.groups)


class Key(Item):
    def __init__(self, scene, x, y):
        super().__init__(scene, x, y)
        self.groups = scene.all_sprites, scene.items, scene.keys
        self.interactable = True
        self.collidable = True
        self.animation = []

        sprite_sheet = SpriteSheet(KEY_SPRITESHEET)
        self.image = sprite_sheet.get_image(0, 0, 32, 32)

        for x in range(0, 97, 32):
            self.animation.append(sprite_sheet.get_image(x, 0, 32, 32))
