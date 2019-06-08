import pygame
from sprites import GameObject, SpriteSheet
from settings import KEY_SPRITESHEET, INVENTORY_SPRITESHEET, TILESIZE, KEY_IDLE_DELAY
from helper import Animate

'''
Inventory class:
    Holds a list of Items
'''
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
        else:
            self.image = self.sprite_sheet.get_image(0, 0, 32, 32)

        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE

'''
Base item class
'''
class Item(GameObject):
    def __init__(self, scene, x, y):
        super().__init__(scene, x, y)
        self.groups = scene.all_sprites, scene.items
        pygame.sprite.Sprite.__init__(self, self.groups)

'''
Key class
'''
class Key(Item):
    def __init__(self, scene, x, y):
        super().__init__(scene, x, y)
        self.groups = scene.all_sprites, scene.items, scene.keys


        # Animation
        self.animation_index = 0
        self.last_update = pygame.time.get_ticks()
        self.update_delay = KEY_IDLE_DELAY
        self.animation = []
        sprite_sheet = SpriteSheet(KEY_SPRITESHEET)
        self.image = sprite_sheet.get_image(0, 0, 32, 32)

        # Append sprites to animation array
        for x in range(0, 65, 32):
            self.animation.append(sprite_sheet.get_image(x, 0, 32, 32))

    def update(self):
        now = pygame.time.get_ticks()

        # Increment animation
        if now - self.last_update >= self.update_delay:
            self.last_update = now
            Animate(self, self.animation)

        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE

        # Append self to inventory and remove object sprite from map
        if self.scene.player.x == self.x and self.scene.player.y == self.y:
            self.scene.inventory.item_list.append(self)
            self.kill()
