import os
import pygame
from settings import *
from helper import Animate, Animate_Attack
from menu import GameOverScene


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
        self.orientation = RIGHT
        self.health = 3
        self.prev_orientation = self.orientation # might not need this
        self.prev_location = (x, y)

        # State
        self.sliding = False #tells if the player is sliding on the ice
        self.attacking = False
        self.hit = False
        self.hit_detected = False

        # Animation
        self.update_delay = PLAYER_IDLE_DELAY
        self.update_attack_delay = PLAYER_ATTACK_DELAY
        self.hit_delay = HIT_DELAY
        self.last_update = pygame.time.get_ticks()
        self.animation_index = 0
        self.animation_attack_index = 0
        self.walking_up = []
        self.walking_down = []
        self.walking_left = []
        self.walking_right = []
        self.attacking_up = []
        self.attacking_down = []
        self.attacking_left = []
        self.attacking_right = []
        self.damage_up = []
        self.damage_down = []
        self.damage_left = []
        self.damage_right = []

        # Sprite sheet definition
        sprite_sheet = SpriteSheet(PLAYER_SPRITE_SHEET)
        self.image = sprite_sheet.get_image(0, 0, 32, 32)

        # Add sprites to walking arrays
        for x in range(0, 97, 32):
            self.walking_right.append(sprite_sheet.get_image(x, 0, 32, 32))
            self.walking_left.append(sprite_sheet.get_image(x, 32, 32, 32))
            self.walking_down.append(sprite_sheet.get_image(x, 64, 32, 32))
            self.walking_up.append(sprite_sheet.get_image(x, 96, 32, 32))

        # Add sprites to attacking arrays
        for x in range(0, 97, 32):
            self.attacking_right.append(sprite_sheet.get_image(x, 128, 32, 32))
            self.attacking_left.append(sprite_sheet.get_image(x, 160, 32, 32))
            self.attacking_down.append(sprite_sheet.get_image(x, 192, 32, 32))
            self.attacking_up.append(sprite_sheet.get_image(x, 224, 32, 32))

        for x in range(128, 161, 32):
            self.damage_right.append(sprite_sheet.get_image(x, 0, 32, 32))
            self.damage_left.append(sprite_sheet.get_image(x, 32, 32, 32))
            self.damage_down.append(sprite_sheet.get_image(x, 64, 32, 32))
            self.damage_up.append(sprite_sheet.get_image(x, 96, 32, 32))

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

    #https://pythonprogramming.net/adding-sounds-music-pygame/
    #https://freesound.org/
    def collision_enemy(self):
        hurt_sound = pygame.mixer.Sound(path.join(MUSIC_FOLDER,"hurt_sound.wav"))
        for enemy in self.scene.enemies:
            if enemy.x == self.x and enemy.y == self.y:
                pygame.mixer.Sound.play(hurt_sound)
                self.enemy = enemy
                return True
        return False

    def take_damage(self):
        self.health -= 1
        if self.prev_location[0] + self.orientation[0] == self.x and\
                self.prev_location[1] + self.orientation[1] == self.y:
            self.x, self.y = self.prev_location[0], self.prev_location[1]
        else:
            self.move(self.enemy.direction[0], self.enemy.direction[1])

    """
    Kill self if health = 0, render game over scene
    """
    def check_health(self):
        if self.health <= 0:
            self.kill()
            self.scene.game.go_to(GameOverScene(self.scene.game))

    """
    Have player interact with different objects:
        box: push box one unit in the direction the player is facing
        enemy: attack the enemy, deal one damage to health, have enemy enter invulnerable state

    """
    def interact(self):
        self.attacking = True
        for object in self.scene.all_sprites:
            if object.x == self.x + self.orientation[0] and \
                    object.y == self.y + self.orientation[1]:
                if object in self.scene.enemies: # check if object is an enemy
                    if object.hit_detected is False: # check if enemy is not invulnerable
                        # object.health -= 1
                        # object.hit = True
                        # self.attacking = True
                        object.take_damage()
                        self.attacking = True

    def update(self):
        now = pygame.time.get_ticks()

        # Check and animate for damage
        if self.hit and not self.hit_detected:
            self.last_update = now
            self.hit_detected = True
        elif self.hit and self.hit_detected:
            if now - self.last_update < self.hit_delay:
                if self.orientation == UP:
                    Animate(self, self.damage_up)
                elif self.orientation == LEFT:
                    Animate(self, self.damage_left)
                elif self.orientation == DOWN:
                    Animate(self, self.damage_down)
                else:
                    Animate(self, self.damage_right)
            else:
                self.last_update = now
                self.hit = False
                self.hit_detected = False
        # Animate player attack animation
        elif self.attacking:
            if now - self.last_update >= self.update_attack_delay:
                self.last_update = now
                if self.orientation == UP:
                    Animate_Attack(self, self.attacking_up)
                elif self.orientation == LEFT:
                    Animate_Attack(self, self.attacking_left)
                elif self.orientation == DOWN:
                    Animate_Attack(self, self.attacking_down)
                else:
                    Animate_Attack(self, self.attacking_right)
        # Render idle animation
        else:
            if now - self.last_update >= self.update_delay:
                self.last_update = now
                if self.orientation == UP:
                    Animate(self, self.walking_up)
                elif self.orientation == LEFT:
                    Animate(self, self.walking_left)
                elif self.orientation == DOWN:
                    Animate(self, self.walking_down)
                else:
                    Animate(self, self.walking_right)



        if self.sliding == True: #if the player is sliding on the Ice
            self.rect.x += (self.orientation[0] * 32)
            self.rect.y += (self.orientation[1] * 32)
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

        if self.collision_enemy() and not self.hit_detected:
            self.take_damage()
            self.hit = True

        self.check_health()


class Block(GameObject):
  def __init__(self, scene, x, y):
        super().__init__(scene, x, y)
        self.groups = scene.all_sprites, scene.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image.fill(BLUE)
        self.collidable = True
        self.interactable = True
        self.sliding = False
        self.orientation = None

        sprite_sheet = SpriteSheet(BLOCK_SPRITE_SHEET)
        self.image = sprite_sheet.get_image(0, 0, 32, 32)

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
    if self.sliding == True: #if the block is sliding on the Ice
        self.rect.x += (self.orientation[0] * 32)
        self.rect.y += (self.orientation[1] * 32)
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
        #self.image = sprite
        self.interactable = False
        self.collidable = True
        self.checked = False #used to tell if the switch has been checked each updated

class Switch(GameObject):
    def __init__(self, scene, x, y, type):
        super().__init__(scene, x, y)
        self.groups = scene.all_sprites, scene.switches
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.interactable = True
        self.collidable = False
        self.switchType = type
        self.isSwitched = False
        sprite_sheet = SpriteSheet(SWITCH_SPRITESHEET)
        self.image = sprite_sheet.get_image(0, 0, 32, 32)
        self.switch_sound = pygame.mixer.Sound(path.join(MUSIC_FOLDER,"switch.wav"))
        self.switch_sound.set_volume(.1)
    def switchOn(self):
        self.isSwitched = True
        pygame.mixer.Sound.play(self.switch_sound)
    def switchOff(self):
        self.isSwitched = False

#Door object.  ImageType filed is "Ice" if this is to be an ice door
class Door(GameObject):
    def __init__(self, scene, x, y, doorType, imageType=None):
        super().__init__(scene, x, y)
        self.groups = scene.all_sprites, scene.doors
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image.fill(RED)
        self.isOpen = False
        self.interactable = False
        self.collidable = True
        self.doorType = doorType
        self.unlocked = False
        self.checked = False #used to tell if the door has been checked to see if it is open each update

        if imageType == "Ice":
            self.sprite_sheet = SpriteSheet(ICEDOOR_SPRITESHEET)
        elif doorType == "Entrance" or doorType == "Exit":
            self.sprite_sheet = SpriteSheet(DOOR_SPRITESHEET)
        else:
            self.sprite_sheet = SpriteSheet(WALLDOOR_SPRITESHEET)
        self.image = self.sprite_sheet.get_image(0, 0, 32, 32)

    def openDoor(self):
        if self.doorType != 'Entrance':
            self.isOpen = True
            self.collidable = False
            self.image = self.sprite_sheet.get_image(64, 0, 32, 32)

    def closeDoor(self):
        if self.unlocked == False: #only unlocked doors can be closed
            if self.doorType != "Entrance":
                self.isOpen = False
                self.collidable = True
                self.image = self.sprite_sheet.get_image(32, 0, 32, 32)

class Chest(GameObject):
    def __init__(self, scene, x, y):
        super().__init__(scene, x, y)
        self.groups = scene.all_sprites, scene.doors
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.isOpen = False
        self.interactable = False
        self.collidable = True
        self.doorType = "Chest"
        self.unlocked = False
        self.checked = False #used to tell if the door has been checked to see if it is open each update
        self.sprite_sheet = SpriteSheet(CHEST_SPRITESHEET)
        self.image = self.sprite_sheet.get_image(32, 0, 32, 32)

    def openDoor(self):
        self.isOpen = True
        self.collidable = False
        self.image = self.sprite_sheet.get_image(64, 0, 32, 32)


class Ice(GameObject):
    def __init__(self, scene, x, y):
        super().__init__(scene, x, y)
        self.groups = scene.all_sprites, scene.ice
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.interactable = False
        self.collidable = False

class LifeHUD(GameObject):
    def __init__(self, scene, x, y):
        super().__init__(scene, x, y)
        self.image = pygame.Surface((TILESIZE * 3, TILESIZE))
        self.groups = scene.all_sprites, scene.hud
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.heart_state = []

        sprite_sheet = SpriteSheet(LIFE_SPRITESHEET)
        self.image = sprite_sheet.get_image(0, 0, 96, 32)

        for x in range(0, 97, 32):
            self.heart_state.append(sprite_sheet.get_image(0, x, 96, 32))

    def update(self):
        heart_state_index = self.scene.player.health - 1
        self.image = self.heart_state[heart_state_index]
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE

class SpriteSheet(object):
    def __init__(self, file_name):
        # You have to call `convert_alpha`, so that the background of
        # the surface is transparent.
        self.sprite_sheet = pygame.image.load(file_name).convert_alpha()

    def get_image(self, x, y, width, height):
        # Use a transparent surface as the base image (pass pygame.SRCALPHA).
        image = pygame.Surface([width, height], pygame.SRCALPHA)
        image.blit(self.sprite_sheet, (0,0), (x, y, width, height))
        return image
# https://stackoverflow.com/questions/48055291/spritesheet-help-in-pygame

# Sources:
# https://github.com/kidscancode/pygame_tutorials/blob/master/tilemap/part%2002/sprites.py
# https://stackoverflow.com/questions/48055291/spritesheet-help-in-pygame
