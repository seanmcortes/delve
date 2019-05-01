import pygame
from sprites import GameObject
from settings import RED, GREEN, TILESIZE, ENEMY_SPEED, HIT_DELAY


class Enemy(GameObject):
    def __init__(self, scene, x, y, orientation, moves):
        super().__init__(scene, x, y)
        self.groups = scene.all_sprites, scene.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image.fill(RED)
        self.orientation = orientation
        self.moves = moves
        self.interactable = False
        self.collidable = False
        self.move_counter = 0
        self.move_counter_increment = 1
        self.reverse = False
        self.health = 3
        self.hit = False
        self.hit_detected = False

        if len(moves) > 0:
            self.direction = None
        # self.direction = direction
        # self.directionX = moves[0]
        # self.directionY = moves[1]
        # self.turns = turns
        # self.turn_counter = 0
        # self.move_count = [0]
        # self.time_counter = 0
        # self.reverse = False
        # self.move_count_reverse = None
        # self.turns_reverse = None

        self.update_delay = ENEMY_SPEED
        self.last_update = pygame.time.get_ticks()
        self.hit_delay = HIT_DELAY

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
        else: # enemy has not finished movement, check for collisions then move
            self.direction = self.moves[self.move_counter]
            if self.reverse: # reverse movement
                self.direction = self.opposite_direction(self.moves[self.move_counter])
            if not self.move(self.direction[0], self.direction[1]): # collision, reverse movement
                self.reverse = not self.reverse
                self.move_counter_increment *= -1
        self.move_counter += self.move_counter_increment

    # def move_algorithm(self):
    #     if self.move(self.directionX, self.directionY):
    #         self.move_count[self.turn_counter] += 1
    #     else:
    #         if self.reverse:
    #             # unravel
    #             self.directionX = self.opposite_direction(self.turns[self.turn_counter])[0]
    #             self.directionY = self.opposite_direction(self.turns[self.turn_counter])[1]
    #         else:
    #             if self.turn_counter >= len(self.turns):
    #                 self.reverse = True
    #                 self.move_count_reverse = self.move_count[::-1]
    #                 self.turns_reverse = [self.opposite_direction(x) for x in self.turns[::-1]]
    #                 self.turns_reverse.append(self.opposite_direction(self.direction))
    #                 self.turn_counter = 0
    #                 self.directionX = self.turns_reverse[self.turn_counter][0]
    #                 self.directionY = self.turns_reverse[self.turn_counter][1]
    #             else:
    #                 self.directionX = self.turns[self.turn_counter][0]
    #                 self.directionY = self.turns[self.turn_counter][1]
    #                 self.turn_counter += 1
    #                 self.move_count.append(0)
    #
    # def move_algorithm_reverse(self):
    #     if self.move(self.directionX, self.directionY):
    #         if self.move_count_reverse[self.turn_counter] <= 1:
    #             self.turn_counter += 1
    #
    #             if self.turn_counter >= len(self.turns_reverse):
    #                 self.reverse = False
    #                 self.turn_counter = 0
    #                 self.directionX = self.direction[0]
    #                 self.directionY = self.direction[1]
    #                 self.move_count_reverse = None
    #                 self.turns_reverse = None
    #                 self.move_count = [0]
    #                 self.turn_counter = 0
    #             else:
    #                 self.directionX = self.turns_reverse[self.turn_counter][0]
    #                 self.directionY = self.turns_reverse[self.turn_counter][1]
    #         else:
    #             self.move_count_reverse[self.turn_counter] -= 1
    #

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

    """
    Draw image. Handle movement
    """
    def update(self):
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE

        now = pygame.time.get_ticks()

        self.check_health()

        if self.hit and not self.hit_detected: # player first hits enemy, starts recovery timer for enemy
            self.last_update = now
            self.hit_detected = True
        elif self.hit and self.hit_detected:
            if now - self.last_update < self.hit_delay:
                self.image.fill(GREEN)
            else:
                self.last_update = now
                self.hit = False
                self.hit_detected = False
        else:
            self.image.fill(RED)
            if now - self.last_update >= self.update_delay:
                self.last_update = now

                if len(self.moves) > 0:
                    self.move_algorithm()


# Sources:
# https://github.com/kidscancode/pygame_tutorials/blob/master/tilemap/part%2002/sprites.py
# https://stackoverflow.com/questions/10762823/how-can-i-pause-one-pygame-function-without-pausing-others
