import pygame
from os import path
from settings import *

tile_dict =	{
  ".": "pebble_brown0.png",
  "t": "tomb0.png"
}
map_folder = "maps"
tile_folder = "image/tiles"

def create_tiles(self, map_file):
    pygame.init()
    surface = pygame.Surface((WIDTH, HEIGHT))
    f = open(path.join(map_folder, map_file), "r")
    if f.mode == 'r':
        map = f.readlines()
        #strip the newline characters
        #https://stackoverflow.com/questions/7984169/remove-trailing-newline-from-the-elements-of-a-string-list
        map = [item.strip() for item in map]
        for map_y, line in enumerate(map):
            for map_x, t in enumerate(line):
                tile = pygame.image.load(path.join(tile_folder, tile_dict[t]))
                surface.blit(tile, (map_x*32, map_y*32))
    f.close()
    return surface
"""
        window = (WIDTH, HEIGHT)
        screen = pygame.display.set_mode(window)
        clock = pygame.time.Clock()

        while True:
            dt = clock.tick(FPS) / 1000

            for event in pygame.event.get():
    	        if event.type == pygame.QUIT:
    	            pygame.quit()
    	            sys.exit()

            screen.blit(surface, [0,0])
            pygame.display.flip()

newMap = Map("level1.map")
"""
