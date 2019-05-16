import pygame
import sys
from os import path
from helper import *
from settings import *
from sprites import *
from map import create_tiles
from map import TiledMap
from enemy import Enemy
from menu import PauseScene
from item import Key, Inventory
#from main import select_scene


"""
Parent class for game scene.

Contains initialization of sprites/player, and functions to draw the game grid.
"""
class GameScene(object):
    def __init__(self, game):
        self.all_sprites = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.blocks = pygame.sprite.Group()
        self.doors = pygame.sprite.Group()
        self.switches = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.ice = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.keys = pygame.sprite.Group()
        self.hud = pygame.sprite.Group()
        self.instructions = Instructions(30, WHITE)
        self.player = None
        self.game = game
        self.tile_map = create_tiles("defaultTile.map")
        self.scene_number = 0

    def render(self):
        self.game.screen.fill(BGCOLOR)
        self.game.screen.blit(self.map_img, self.map_rect)
        #self.game.screen.blit(self.tile_map, [0,0])
        # self.draw_grid()
        self.ice.draw(self.game.screen)#draw ice tiles on the bottom
        #self.walls.draw(self.game.screen)
        self.switches.draw(self.game.screen)
        self.blocks.draw(self.game.screen)
        self.doors.draw(self.game.screen)
        self.enemies.draw(self.game.screen)
        self.players.draw(self.game.screen)
        self.hud.draw(self.game.screen)
        self.items.draw(self.game.screen)
        self.instructions.draw(self.game.screen)
        self.draw_HUD(self.game.screen)

    def update(self):
        self.ice.update()
        self.walls.update()
        self.blocks.update() #update blocks before player so blocks sliding on the ice stop before the player
        self.switches.update()
        self.doors.update()
        self.enemies.update()
        self.players.update()
        self.items.update()
        self.instructions.update()
        self.hud.update()

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            keyState = pygame.key.get_pressed()
            if keyState[pygame.K_p]: #Pause the game
                pauseScene = PauseScene(self.game) #create a pause scene
                pauseScene.paused() #loop until the player exits the pause screen
            if self.player.sliding == False: #Ignore the directional key key presses if player is sliding on ice
                if keyState[pygame.K_w]:
                    if self.player.orientation != UP:
                        self.player.orientation = UP
                    else:
                        if self.collision_ice(dx=0, dy=-1):
                            self.player.sliding = True
                        if not self.collision_wall(dx=0, dy=-1):
                            if not self.collision_block(dx=0, dy=-1):
                                self.player.move(dx=0, dy=-1)
                                self.player.orientation = UP
                            else:
                                for block in self.blocks:
                                    if block.x == self.player.x+0 and block.y == self.player.y-1:
                                        if block.move(dx=0, dy=-1):
                                            block.orientation = self.player.orientation
                                            self.player.move(dx=0, dy=-1)
                                        else:
                                            self.player.sliding = False
                                self.player.orientation = UP
                if keyState[pygame.K_s]:
                    if self.player.orientation != DOWN:
                        self.player.orientation = DOWN
                    else:
                        if self.collision_ice(dx=0, dy=1):
                            self.player.sliding = True
                        if not self.collision_wall(dx=0, dy=1):
                            if not self.collision_block(dx=0, dy=1):
                                self.player.move(dx=0, dy=1)
                                self.player.orientation = DOWN
                            else:
                                for block in self.blocks:
                                    if block.x == self.player.x+0 and block.y == self.player.y+1:
                                        if block.move(dx=0, dy=1):
                                            block.orientation = self.player.orientation
                                            self.player.move(dx=0, dy=1)
                                        else:
                                            self.player.sliding = False
                                self.player.orientation = DOWN
                if keyState[pygame.K_a]:
                    if self.player.orientation != LEFT:
                        self.player.orientation = LEFT
                    else:
                        if self.collision_ice(dx=-1, dy=0):
                            self.player.sliding = True
                        if not self.collision_wall(dx=-1, dy=0):
                            if not self.collision_block(dx=-1, dy=0):
                                self.player.move(dx=-1, dy=0)
                                self.player.orientation = LEFT
                            else:
                                for block in self.blocks:
                                    if block.x == self.player.x-1 and block.y == self.player.y+0:
                                        if block.move(dx=-1, dy=0):
                                            block.orientation = self.player.orientation
                                            self.player.move(dx=-1, dy=0)
                                        else:
                                            self.player.sliding = False
                                self.player.orientation = LEFT
                if keyState[pygame.K_d]:
                    if self.player.orientation != RIGHT:
                        self.player.orientation = RIGHT
                    else:
                        if self.collision_ice(dx=1, dy=0):
                            self.player.sliding = True
                        if not self.collision_wall(dx=1, dy=0):
                            if not self.collision_block(dx=1, dy=0):
                                self.player.move(dx=1, dy=0)
                                self.player.orientation = RIGHT
                            else:
                                for block in self.blocks:
                                    if block.x == self.player.x+1 and block.y == self.player.y+0:
                                        if block.move(dx=1, dy=0):
                                            block.orientation = self.player.orientation
                                            self.player.move(dx=1, dy=0)
                                        else:
                                            self.player.sliding = False
                                self.player.orientation = RIGHT
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.player.interact()
            if len(self.switches) > 0:
                for door in self.doors:
                    for block in self.blocks:
                        for switch in self.switches:
                            if block.x == switch.x and block.y == switch.y:
                                if door.doorType == 'exit':
                                    door.isOpen = True
                                    door.collidable = False
                                    door.openDoor()
                            elif switch.x == self.player.x and switch.y == self.player.y:
                                if door.doorType == 'exit':
                                    door.isOpen = True
                                    door.collidable = False
                                    door.openDoor()
                            else:
                                    door.isOpen = False
                                    door.collidable = True
                                    door.closeDoor()
            for door in self.doors:
                if self.player.x == door.x and (self.player.y == door.y + 1 or self.player.y == door.y - 1):
                            if len(self.inventory.item_list) > 0:
                                if type(self.inventory.item_list[0]) == Key:
                                    if door.doorType == 'exit':
                                        door.isOpen = True
                                        door.collidable = False
                                        door.openDoor()
                elif self.player.y == door.y and (self.player.x == door.x + 1 or self.player.x == door.x - 1):
                            if len(self.inventory.item_list) > 0:
                                if type(self.inventory.item_list[0]) == Key:
                                    if door.doorType == 'exit':
                                        door.isOpen = True
                                        door.collidable = False
                                        door.openDoor()
                if self.player.x == door.x and self.player.y == door.y:
                    if door.doorType == 'exit':
                        self.game.select_scene(self.scene_number + 1)

    def collision_wall(self, dx, dy):
        for wall in self.walls:
            if wall.x == self.player.x + dx and wall.y == self.player.y + dy:
                return True
        return False

    def collision_ice(self, dx, dy):
        for ice in self.ice:
            if ice.x == self.player.x +dx and ice.y == self.player.y + dy:
                return True
        return False

    def collision_block(self, dx, dy):
        for block in self.blocks:
            if block.x == self.player.x +dx and block.y == self.player.y + dy:
                return True
        return False

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pygame.draw.line(self.game.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pygame.draw.line(self.game.screen, LIGHTGREY, (0, y), (WIDTH, y))

    #def draw_layout(self, map_file):
    def draw_objects(self):
        for tile_object in self.map.tmxdata.objects:
            if tile_object.name == 'Player':
                self.player = Player(self, tile_object.x/32, tile_object.y/32)
            if tile_object.name == 'Wall':
                Wall(self, tile_object.x/32, tile_object.y/32)
            if tile_object.name == 'Block':
                Block(self, tile_object.x/32, tile_object.y/32)
            if tile_object.name == 'Ice':
                Ice(self, tile_object.x/32, tile_object.y/32)
            if tile_object.name == 'Key':
                Key(self, tile_object.x/32, tile_object.y/32)
            if tile_object.name == 'Switch':
                Switch(self,tile_object.x/32,tile_object.y/32)
            if tile_object.name == 'Entrance':
                Door(self,tile_object.x/32,tile_object.y/32, "entrance")
            if tile_object.name == 'Exit':
                exit = Door(self,tile_object.x/32,tile_object.y/32, "exit")
                exit.closeDoor()


        LifeHUD(self, 3, 0)
        self.inventory = Inventory(self, 17, 0)
        """
        if f.mode == 'r':
            map = f.readlines()
            map = [item.strip() for item in map]
            for row, tiles in enumerate(map):
                for col, tile in enumerate(tiles):
                    if tile == 'Q':
                        Wall(self, col, row, sprite_sheet.get_image(0, 0, 32, 32))
                    if tile == 'W':
                        Wall(self, col, row, sprite_sheet.get_image(32, 0, 32, 32))
                    if tile == 'E':
                        Wall(self, col, row, sprite_sheet.get_image(64, 0, 32, 32))
                    if tile == 'A':
                        Wall(self, col, row, sprite_sheet.get_image(0, 32, 32, 32))
                    if tile == 'X':
                        Wall(self, col, row, sprite_sheet.get_image(32, 32, 32, 32))
                    if tile == 'D':
                        Wall(self, col, row, sprite_sheet.get_image(64, 32, 32, 32))
                    if tile == 'Z':
                        Wall(self, col, row, sprite_sheet.get_image(0, 64, 32, 32))
                    if tile == 'S':
                        Wall(self, col, row, sprite_sheet.get_image(32, 64, 32, 32))
                    if tile == 'C':
                        Wall(self, col, row, sprite_sheet.get_image(64, 64, 32, 32))
                    if tile == 'P':
                        self.player = Player(self, col, row)
                    if tile == 'B':
                        Block(self, col, row)
                    if tile == 'i':
                        Ice(self, col, row)
                    if tile == 'K':
                        Key(self, col, row)
                    if tile == 'F':
                        Switch(self,col,row)
                    if tile == 'G':
                        Door(self,col,row, "entrance")
                    if tile == 'H':
                        exit = Door(self,col,row, "exit")
                        exit.closeDoor()
            """

    def draw_HUD(self, screen):

        life_text = TextObject("LIFE:", path.join(IMAGE_FOLDER, 'CuteFont-Regular.ttf'), 40, WHITE, WIDTH/11,
                                        HEIGHT/32)
        life_text.render(screen)




"""
Display Level 1

- Simple tutorial, show player how to move character and what the objectives of the game are.
"""
class TutorialMovement(GameScene):
    def __init__(self, game):
        super().__init__(game)
        self.map = TiledMap(path.join(MAP_FOLDER, 'level1.tmx'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        #self.player = Player(self, 1, 2)
        self.scene_number = self.game.get_scene_number(TutorialMovement)
        #self.tile_map = create_tiles("tutorialMovementTile.map")
        self.draw_objects()
        self.instructions.add("Use the WASD keys to move around.", 100)
        self.instructions.add("Press P to pause the game.", 140)
        self.instructions.add("Get the key to unlock the door and proceed to the next level.", 180)


"""
Display tutorial level for enemies
"""
class TutorialEnemy(GameScene):
    def __init__(self, game):
        super().__init__(game)
        self.scene_number = self.game.get_scene_number(TutorialEnemy)
        self.tile_map = create_tiles("tutorialEnemyTile.map")
        self.draw_layout("tutorialEnemyObject.map")
        self.spawn_enemies()
        self.instructions.add("Press the Spacebar while standing next to an enemy to attack it.", 100)
        self.instructions.add("Make sure you don't run out of Hearts!", 140)

    def spawn_enemies(self):
        Enemy(self, 10, 5, LEFT, [])

        Enemy(self, 10, 15, UP, [UP, UP, UP, UP, UP,
                                   UP, UP, UP, UP])

"""
Display tutorial level for ice
"""
class TutorialIce(GameScene):
    def __init__(self, game):
        super().__init__(game)
        self.scene_number = self.game.get_scene_number(TutorialIce)
        self.draw_layout("tutorialIceObjects.map")
        Block(self, 2, 10)
        Block(self, 16, 11)
        Key(self, 16, 17)
        self.instructions = Instructions(30, BLUE)
        self.instructions.add("Be careful on the ice!", 100)
        self.instructions.add("You will slide until you collide with an object.", 140)
        self.instructions.add("Try to position the blocks to help you", 180)
        self.instructions.add("reach the key and unlock the door.", 220)

"""
Unit test scene for blocks
"""

class BlockUnitTest(GameScene):
    def __init__(self, game):
        super().__init__(game)
        self.scene_number = self.game.get_scene_number(BlockUnitTest)
        self.draw_layout("blockUnitTest.map")

class TutorialBlocks(GameScene):
    def __init__(self, game):
        super().__init__(game)
        self.scene_number = self.game.get_scene_number(TutorialBlocks)
        self.draw_layout("tutorialBlocks.map")
        self.instructions.add("You can move the blocks by standing next to them", 100)
        self.instructions.add("and pushing the directional buttons.", 140)
        self.instructions.add("Push the block on top of the switch to unlock the door.", 180)



# Sources:
# https://github.com/kidscancode/pygame_tutorials/blob/master/tilemap/part%2007/main.py
# https://stackoverflow.com/questions/14700889/pygame-level-menu-states
