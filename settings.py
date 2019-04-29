# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
ORANGE = (255, 165, 0)
GREEN = (0, 255, 255)
RED = (255, 0, 0)

# directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# game parameters
WIDTH = 640 # 32 * 20
HEIGHT = 640 # 32 * 20
FPS = 60
TITLE = "Delve"
BGCOLOR = DARKGREY

# game dimensions
TILESIZE = 32
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

# object variables
ENEMY_SPEED = 200 # delay in ms between enemy movement


"""
Sources:
https://github.com/kidscancode/pygame_tutorials/blob/master/tilemap/part%2022/settings.py
"""