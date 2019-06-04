import pygame
import pytmx
from settings import *

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
"""
This class creates the Tiled maps.  It is used with the .tmx files created in the
third-party Tiled program
"""
class TiledMap:
    def __init__(self, filename):
        tm = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm
        self.image = self.make_map()
        self.rect = self.image.get_rect()

    def render(self, surface):
        ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile = ti(gid)
                    if tile:
                        surface.blit(tile, (x * self.tmxdata.tilewidth,
                                            y * self.tmxdata.tileheight))

    def make_map(self):
        temp_surface = pygame.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface
