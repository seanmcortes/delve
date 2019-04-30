import pygame
from sprites import GameObject
from settings import RED, TILESIZE, ENEMY_SPEED


class Enemy(GameObject):
    def __init__(self, scene, x, y, direction, turns):
        super().__init__(scene, x, y)
        self.image.fill(RED)
        self.direction = direction
        self.directionX = direction[0]
        self.directionY = direction[1]
        self.turns = turns
        self.turn_counter = 0
        self.move_count = [0]
        self.time_counter = 0
        self.reverse = False
        self.move_count_reverse = None
        self.turns_reverse = None

        self.update_delay = ENEMY_SPEED
        self.last_update = pygame.time.get_ticks()

    def move(self, dx=0, dy=0):
        if not self.collision_wall(dx, dy):
            self.x += dx
            self.y += dy
            return True
        else:
            return False

    def collision_wall(self, dx, dy):
        for wall in self.scene.walls:
            if wall.x == self.x + dx and wall.y == self.y + dy:
                return True
        return False

    def move_algorithm(self):
        if self.move(self.directionX, self.directionY):
            self.move_count[self.turn_counter] += 1
        else:
            if self.reverse:
                # unravel
                self.directionX = self.opposite_direction(self.turns[self.turn_counter])[0]
                self.directionY = self.opposite_direction(self.turns[self.turn_counter])[1]
            else:
                if self.turn_counter >= len(self.turns):
                    self.reverse = True
                    self.move_count_reverse = self.move_count[::-1]
                    self.turns_reverse = [self.opposite_direction(x) for x in self.turns[::-1]]
                    self.turns_reverse.append(self.opposite_direction(self.direction))
                    self.turn_counter = 0
                    self.directionX = self.turns_reverse[self.turn_counter][0]
                    self.directionY = self.turns_reverse[self.turn_counter][1]
                else:
                    self.directionX = self.turns[self.turn_counter][0]
                    self.directionY = self.turns[self.turn_counter][1]
                    self.turn_counter += 1
                    self.move_count.append(0)

    def move_algorithm_reverse(self):
        if self.move(self.directionX, self.directionY):
            if self.move_count_reverse[self.turn_counter] <= 1:
                self.turn_counter += 1

                if self.turn_counter >= len(self.turns_reverse):
                    self.reverse = False
                    self.turn_counter = 0
                    self.directionX = self.direction[0]
                    self.directionY = self.direction[1]
                    self.move_count_reverse = None
                    self.turns_reverse = None
                    self.move_count = [0]
                    self.turn_counter = 0
                else:
                    self.directionX = self.turns_reverse[self.turn_counter][0]
                    self.directionY = self.turns_reverse[self.turn_counter][1]
            else:
                self.move_count_reverse[self.turn_counter] -= 1

    def opposite_direction(self, direction):
        return [x * -1 for x in direction]

    def update(self):
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE

        now = pygame.time.get_ticks()

        if now - self.last_update >= self.update_delay:
            self.last_update = now
            if not self.reverse:
                self.move_algorithm()
            else:
                self.move_algorithm_reverse()

        # pygame.time.delay(100)


# Sources:
# https://github.com/kidscancode/pygame_tutorials/blob/master/tilemap/part%2002/sprites.py
# https://stackoverflow.com/questions/10762823/how-can-i-pause-one-pygame-function-without-pausing-others
