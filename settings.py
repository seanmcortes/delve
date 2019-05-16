import os
import sys
from os import path
from os.path import join #for file handling

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
HEIGHT = 672 # 32 * 21
FPS = 12
TITLE = "Delve"
BGCOLOR = DARKGREY

# game dimensions
TILESIZE = 32
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

# object variables
ENEMY_SPEED = 500 # delay in ms between enemy movement
PLAYER_IDLE_DELAY = 200
KEY_IDLE_DELAY = 300
HIT_DELAY = 60

#file folders
if getattr(sys, 'frozen', False):
    GAME_FOLDER = os.path.dirname(sys.executable)
else:
    GAME_FOLDER = os.path.dirname(os.path.realpath(__file__))

# GAME_FOLDER = path.dirname(__file__)
MAP_FOLDER = path.join(GAME_FOLDER, "maps")
SAVE_FOLDER = path.join(GAME_FOLDER, "save")
IMAGE_FOLDER = path.join(GAME_FOLDER, "image")
TILE_FOLDER = path.join(IMAGE_FOLDER, "tiles")
PLAYER_SPRITE_SHEET = path.join(IMAGE_FOLDER, 'Player.png')
BLOCK_SPRITE_SHEET = path.join(IMAGE_FOLDER, 'Block.png')
BAT_SPRITE_SHEET = path.join(IMAGE_FOLDER, 'Bat.png')
WALL_SPRITESHEET = path.join(IMAGE_FOLDER, 'Walls.png')
KEY_SPRITESHEET = path.join(IMAGE_FOLDER, 'Key.png')
LIFE_SPRITESHEET = path.join(IMAGE_FOLDER, 'Heart.png')
SWITCH_SPRITESHEET = path.join(IMAGE_FOLDER, 'Switch.png')
INVENTORY_SPRITESHEET = path.join(IMAGE_FOLDER, 'Inventory.png')
DOOR_SPRITESHEET = path.join(IMAGE_FOLDER, 'Door.png')
CUTEFONT = path.join(IMAGE_FOLDER, 'CuteFont-Regular.ttf')

# Sources:
# https://github.com/kidscancode/pygame_tutorials/blob/master/tilemap/part%2022/settings.py
