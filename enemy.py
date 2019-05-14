import pygame
from sprites import GameObject, SpriteSheet
from settings import RED, GREEN, TILESIZE, ENEMY_SPEED, \
    HIT_DELAY, UP, DOWN, LEFT, RIGHT, BAT_SPRITE_SHEET
from helper import Animate


class Enemy(GameObject):
    def __init__(self, scene, x, y, orientation, moves):
        super().__init__(scene, x, y)
        self.groups = scene.all_sprites, scene.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.orientation = orientation
        self.moves = moves
        self.interactable = False
        self.collidable = False
        self.move_counter = 0
        self.move_counter_increment = 1
        self.reverse = False
        self.health = 1
        self.hit = False
        self.hit_detected = False

        if len(moves) > 0:
            self.direction = None

        # Animation
        self.animation_index = 0
        self.update_delay = ENEMY_SPEED
        self.last_update = pygame.time.get_ticks()
        self.last_idle_update = pygame.time.get_ticks()
        self.hit_delay = HIT_DELAY

        sprite_sheet = SpriteSheet(BAT_SPRITE_SHEET)
        self.image = sprite_sheet.get_image(0, 0, 32, 32)

        self.walking_up = []
        self.walking_down = []
        self.walking_left = []
        self.walking_right = []

        for x in range(0, 33, 32):
            self.walking_right.append(sprite_sheet.get_image(x, 0, 32, 32))
        for x in range(0, 33, 32):
            self.walking_left.append(sprite_sheet.get_image(x, 32, 32, 32))
        for x in range(0, 33, 32):
            self.walking_down.append(sprite_sheet.get_image(x, 64, 32, 32))
        for x in range(0, 33, 32):
            self.walking_up.append(sprite_sheet.get_image(x, 96, 32, 32))

    """
    Move object a number of tiles
    
    Args:
        dx (int): number of tiles moved in x-coordinate
        dy (int): number of tiles moved in y-coordinate
        
    Returns:
        bool: True if object can move, false if there is collision.
    """
    def move(self, dx=0, dy=0):
        if not self.collision_object(dx, dy):
            self.x += dx
            self.y += dy
            self.orientation = (dx, dy)
            return True
        else:
            return False

    """
    Handle enemy patrol route. Reverses route if collision occurs.
    """
    def move_algorithm(self):
        if self.move_counter >= len(self.moves) or self.move_counter < 0: # enemy finishes movement
            self.reverse = not self.reverse
            self.move_counter_increment *= -1
            self.orientation = self.opposite_direction(self.orientation)
        else: # enemy has not finished movement, check for collisions then move
            self.direction = self.moves[self.move_counter]
            if self.reverse: # reverse movement
                self.direction = self.opposite_direction(self.moves[self.move_counter])
            if not self.move(self.direction[0], self.direction[1]): # collision, reverse movement
                self.reverse = not self.reverse
                self.move_counter_increment *= -1
        self.move_counter += self.move_counter_increment

    """
    Reverses direction (e.g. LEFT -> RIGHT, UP -> DOWN, vice-versa)
    
    Args:
        direction (tuple): (x, y) as represented by directions in settings.py
        
    Returns:
        tuple: (x, y) as represented by direction in settings.py
    """
    def opposite_direction(self, direction):
        return tuple(x * -1 for x in direction)

    """
    Check health, kill if 0
    """
    def check_health(self):
        if self.health <= 0:
            self.kill()

    def render_orientation(self):
        if self.orientation == UP:
            self.image = self.walking_up[0]
        elif self.orientation == DOWN:
            self.image = self.walking_down[0]
        elif self.orientation == LEFT:
            self.image = self.walking_left[0]
        else:
            self.image = self.walking_right[0]

    """
    Draw image. Handle movement
    """
    def update(self):
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE

        now = pygame.time.get_ticks()

        if now - self.last_idle_update >= self.update_delay:
            self.last_idle_update = now
            if self.orientation == UP:
                Animate(self, self.walking_up)
            elif self.orientation == LEFT:
                Animate(self, self.walking_left)
            elif self.orientation == DOWN:
                Animate(self, self.walking_down)
            else:
                Animate(self, self.walking_right)

        self.check_health()

        if self.hit and not self.hit_detected: # player first hits enemy, starts recovery timer for enemy
            self.last_update = now
            self.hit_detected = True
        elif self.hit and self.hit_detected:
            if now - self.last_update < self.hit_delay:
                self.image = self.walking_left[0]
            else:
                self.last_update = now
                self.hit = False
                self.hit_detected = False
        else:
            # self.render_orientation()
            if now - self.last_update >= self.update_delay:
                self.last_update = now

                if len(self.moves) > 0:
                    self.move_algorithm()


# Sources:
# https://github.com/kidscancode/pygame_tutorials/blob/master/tilemap/part%2002/sprites.py
# https://stackoverflow.com/questions/10762823/how-can-i-pause-one-pygame-function-without-pausing-others
