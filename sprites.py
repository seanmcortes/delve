import pygame
from settings import *

class GameObject(pygame.sprite.Sprite):
    def __init__(self, scene, x, y):
        self.scene = scene
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.interactable = False
        self.collidable = False
        self.orientation = None
        self.enemy = None
        self.sliding = False #tells if the object is sliding on the ice

    def update(self):
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE

    """
        Check if enemy has collided with a collidable object

        Args:
            dx (int): x-coordinate for collision check
            dy (int): y-coordinate for collision check

        Returns:
            bool: True if collision with collidable object. False if not
        """

    def collision_object(self, dx, dy):
        for game_object in self.scene.all_sprites:
            if game_object.collidable and (game_object.x == self.x + dx and game_object.y == self.y + dy):
                return True
        return False

    def collision_ice(self):
        for ice in self.scene.ice:
            if ice.x == self.x and ice.y == self.y:
                return True
        return False

    def collision_block(self, dx, dy):
        for block in self.scene.blocks:
            if block.x == self.x + dx and block.y == self.y + dy and block.sliding == False:
                return True
        return False

class Player(GameObject):
    def __init__(self, scene, x, y):
        super().__init__(scene, x, y)
        self.groups = scene.all_sprites, scene.players
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image.fill(ORANGE)
        self.orientation = RIGHT
        self.health = 3
        self.prev_orientation = self.orientation # might not need this
        self.prev_location = (x, y)
        self.sliding = False #tells if the player is sliding on the ice

    def move(self, dx=0, dy=0):
        if not self.collision_object(dx, dy):
            self.prev_location = (self.x, self.y)
            self.x += dx
            self.y += dy
            self.prev_orientation = self.orientation
            self.orientation = (dx, dy)
            return True
        else:
            return False


    def collision_enemy(self):
        for enemy in self.scene.enemies:
            if enemy.x == self.x and enemy.y == self.y:
                self.enemy = enemy
                return True
        return False

    def take_damage(self):
        self.health -= 1
        print("You have taken damage. Current health: ", self.health) # place-holder
        if self.prev_location[0] + self.orientation[0] == self.x and\
                self.prev_location[1] + self.orientation[1] == self.y:
            self.x, self.y = self.prev_location[0], self.prev_location[1]
        else:
            self.move(self.enemy.direction[0], self.enemy.direction[1])

    def check_health(self):
        if self.health <= 0:
            self.kill()
            print("You have died!") # place-holder

    def update(self):
        if self.sliding == True: #if the player is sliding on the Ice
            self.rect.x += (self.orientation[0] * 8)
            self.rect.y += (self.orientation[1] * 8)
            self.x = (self.rect.x - (self.rect.x % TILESIZE)) / TILESIZE
            self.y = (self.rect.y - (self.rect.y % TILESIZE)) / TILESIZE
            #stop sliding if they collide into a collidable object
            if self.collision_object(self.orientation[0], self.orientation[1]):
                self.sliding = False
            #stop sliding if they collide with a block
            if self.collision_block(self.orientation[0], self.orientation[1]):
                self.sliding = False
            #stop sliding if they are not on an ice tile
            elif self.rect.x % TILESIZE == 0 and self.rect.y % TILESIZE == 0 and not self.collision_ice():
                self.sliding = False
            #align the rectangle with a tile
            if self.sliding == False:
                self.rect.x = self.x * TILESIZE
                self.rect.y = self.y * TILESIZE
        else:
            self.rect.x = self.x * TILESIZE
            self.rect.y = self.y * TILESIZE
        """version without sliding animations
        if self.sliding == True: #if the player is sliding on the Ice
            #stop sliding if they collide into a collidable object
            if self.collision_object(self.orientation[0], self.orientation[1]):
                self.sliding = False
            #stop sliding if they collide with a block
            if self.collision_block(self.orientation[0], self.orientation[1]):
                self.sliding = False
            #stop sliding if they are not on an ice tile
            elif not self.collision_ice():
                self.sliding = False
            else: #else, move them to the next tile
                self.move(self.orientation[0], self.orientation[1])

        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE
        """

        if self.collision_enemy():
            self.take_damage()

        self.check_health()

class Block(GameObject):
  def __init__(self, scene, x, y):
      super().__init__(scene, x, y)
      self.groups = scene.all_sprites, scene.blocks
      pygame.sprite.Sprite.__init__(self, self.groups)
      self.image.fill(BLUE)
      self.interactable = True
      self.sliding = False

  def move(self, dx=0, dy=0):
        #Test if this block is going to collide with anything
        if not self.collision_object(dx, dy) and not self.collision_block(dx, dy):
            self.x += dx
            self.y += dy
            if self.collision_ice(): #if the box has just been pused onto ice
                self.sliding = True
            return True

        return False


  def update(self):
    if self.sliding == True: #if the player is sliding on the Ice
        self.rect.x += (self.scene.player.orientation[0] * 8)
        self.rect.y += (self.scene.player.orientation[1] * 8)
        self.x = (self.rect.x - (self.rect.x % TILESIZE)) / TILESIZE
        self.y = (self.rect.y - (self.rect.y % TILESIZE)) / TILESIZE
        #stop sliding if they collide into a collidable object
        if self.collision_object(self.scene.player.orientation[0], self.scene.player.orientation[1]):
            self.sliding = False
        #stop sliding if they collide with a block
        if self.collision_block(self.scene.player.orientation[0], self.scene.player.orientation[1]):
            self.sliding = False
        #stop sliding if they are not on an ice tile
        elif self.rect.x % TILESIZE == 0 and self.rect.y % TILESIZE == 0 and not self.collision_ice():
            self.sliding = False
    else:
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE
    """ Version without sliding animations
    if self.sliding == True: #if the player is sliding on the Ice
        #stop sliding if they collide into a collidable object
        if self.collision_object(self.scene.player.orientation[0], self.scene.player.orientation[1]):
            self.sliding = False
        #stop sliding if they collide with a block
        if self.collision_block(self.scene.player.orientation[0], self.scene.player.orientation[1]):
            self.sliding = False
        #stop sliding if they are not on an ice tile
        elif not self.collision_ice():
            self.sliding = False
        else: #else, move them to the next tile
            self.move(self.scene.player.orientation[0], self.scene.player.orientation[1])

    self.rect.x = self.x * TILESIZE
    self.rect.y = self.y * TILESIZE
    """
class Wall(GameObject):
    def __init__(self, scene, x, y):
        super().__init__(scene, x, y)
        self.groups = scene.all_sprites, scene.walls
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image.fill(LIGHTGREY)
        self.interactable = False
        self.collidable = True

class Ice(GameObject):
    def __init__(self, scene, x, y):
        super().__init__(scene, x, y)
        self.groups = scene.all_sprites, scene.ice
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image.fill(WHITE)
        self.interactable = False
        self.collidable = False


# Sources:
# https://github.com/kidscancode/pygame_tutorials/blob/master/tilemap/part%2002/sprites.py
