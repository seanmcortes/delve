import pygame
from os import path
from settings import WIDTH, HEIGHT

tile_dict =	{
  # ".": "pebble_brown0.png",
    ".": "dirt0.png",
  "t": "tomb0.png"
}
#map_folder = "maps"
#tile_folder = "image/tiles"

"""
    This function generates the background tiles. It does this by reading
    in characters from a .map file.  Each character is mapped to a tile image
    in the tile_dict dictionary. It draws the tiles to a surface, and then
    returns the surface, so that the main program loop can blit the surface
    to the screen as a background instead of rendering each separate tile
    Args:
    map_file: the name of the .map file (has to be saved in the maps folder)
"""
def create_tiles(map_file):
    game_folder = path.dirname(__file__)
    map_folder = path.join(game_folder, "maps")
    image_folder = path.join(game_folder, "image")
    tiles_folder = path.join(image_folder, "tiles")
    surface = pygame.Surface((WIDTH, HEIGHT)) #surface that will serve as the tiled background
    f = open(path.join(map_folder, map_file), "r") #open the map file
    if f.mode == 'r':
        map = f.readlines() #read in the map file to a list of strings
        #strip the newline characters
        #https://stackoverflow.com/questions/7984169/remove-trailing-newline-from-the-elements-of-a-string-list
        map = [item.strip() for item in map]
        for map_y, line in enumerate(map):
            for map_x, t in enumerate(line):
                #retrieve the tile image from the image/tiles folder
                tile = pygame.image.load(path.join(tiles_folder, tile_dict[t]))
                surface.blit(tile, (map_x*32, map_y*32)) #draw the tile to the surface
    f.close()
    return surface
""" Code for debugging
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
