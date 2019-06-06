import pygame
import sys
from os import path
from helper import *
from settings import *
from sprites import *
from map import TiledMap
from enemy import Enemy, Ghost
from menu import PauseScene, CreditScene, VictoryScene
from item import Key, Inventory

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
        self.scene_number = 0
        self.volume_level = 0.5

    def render(self):
        self.game.screen.fill(BGCOLOR)
        self.game.screen.blit(self.map.image, self.map.rect)
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
        self.adjust_music_volume()
        self.checkSwitches()
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
            if keyState[pygame.K_EQUALS]:
                if (self.volume_level < 1.0):
                    self.volume_level += .1
            if keyState[pygame.K_MINUS]:
                if self.volume_level > 0.1:
                    self.volume_level -= .1
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
                if event.key == pygame.K_SPACE and not self.player.hit_detected: # attack only if player is in vulnerable state
                    self.player.interact()


    """
    Adjust volume levels for sounds
    #https://www.pygame.org/docs/ref/mixer.html
    """
    def adjust_music_volume(self):
        pygame.mixer.music.set_volume(self.volume_level)


    """
    Check for collision with a wall.
    Args:
        dx (int): x direction that the player is planning on moving
        dy (int): y direction that player is planning on moving
    Return:
        bool: True if player will hit a wall, false if not
    """
    def collision_wall(self, dx, dy):
        for wall in self.walls:
            if wall.x == self.player.x + dx and wall.y == self.player.y + dy:
                return True
        return False

    """
    Check for collision with an ice tile.
    Args:
        dx (int): x direction that the player is planning on moving
        dy (int): y direction that player is planning on moving
    Return:
         bool: True if player will hit ice tile, false if not
    """
    def collision_ice(self, dx, dy):
        for ice in self.ice:
            if ice.x == self.player.x +dx and ice.y == self.player.y + dy:
                return True
        return False

    """
    Check for collision with a block.
    Args:
        dx (int): x direction that the player is planning on moving
        dy (int): y direction that player is planning on moving
    Return:
        bool: True if player will hit block, false if not
    """
    def collision_block(self, dx, dy):
        for block in self.blocks:
            if block.x == self.player.x + dx and block.y == self.player.y + dy:
                return True
        return False

    """
    Draw lines for map grid
    """
    # TODO: potentially remove, unecessary function
    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pygame.draw.line(self.game.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pygame.draw.line(self.game.screen, LIGHTGREY, (0, y), (WIDTH, y))

    """
    Take in tmx file and render object layer:
        Keywords:
            Player
            Wall
            Block
            Ice
            Key
            Switch
            Entrance
            Exit
    """
    def draw_objects(self):
        for tile_object in self.map.tmxdata.objects:
            if tile_object.name == 'Player':
                self.player = Player(self, tile_object.x/32, tile_object.y/32)
            if tile_object.name == 'Wall':
                Wall(self, tile_object.x/32, tile_object.y/32)
            if tile_object.name == 'Block':
                Block(self, tile_object.x/32, tile_object.y/32)
            #use tyoe unstead of name for ice
            if tile_object.type == 'Ice':
                Ice(self, tile_object.x/32, tile_object.y/32)
            if tile_object.name == 'Key':
                Key(self, tile_object.x/32, tile_object.y/32)
            if tile_object.name == 'Switch':
                Switch(self,tile_object.x/32,tile_object.y/32, tile_object.type)
            if tile_object.type == "Door":
                if tile_object.name == 'IceEntrance':
                    door = Door(self,tile_object.x/32,tile_object.y/32, "Entrance", "Ice")
                elif tile_object.name == 'IceExit':
                    door = Door(self,tile_object.x/32,tile_object.y/32, "Exit", "Ice")
                else:
                    door = Door(self,tile_object.x/32,tile_object.y/32, tile_object.name)
                if door.doorType != 'Entrance':
                    door.closeDoor()
            if tile_object.name == 'Chest':
                Chest(self, tile_object.x/32,tile_object.y/32)


        LifeHUD(self, 3, 0)
        self.inventory = Inventory(self, 17, 0)

    def draw_HUD(self, screen):

        life_text = TextObject("LIFE:", path.join(IMAGE_FOLDER, 'CuteFont-Regular.ttf'), 40, WHITE, WIDTH/11,
                                        HEIGHT/32)
        life_text.render(screen)

    """
    This checks the switches to to see if the player or a block has activated the switch
    and checks the exits and treasure chest to see if the player interacted with them
    """
    def checkSwitches(self):
        if len(self.switches) > 0:
            for door in self.doors: #set all the doors to closed by default
                door.checked = False
            for switch in self.switches:
                switch.adjustVolume(self.volume_level)
                switch.checked = False
                for block in self.blocks:
                    for door in self.doors:
                        if block.x == switch.x and block.y == switch.y:
                            switch.checked = True
                            if switch.isSwitched == False:
                                switch.switchOn()
                            if door.doorType == switch.switchType:
                                door.checked = True
                                if door.isOpen == False:
                                    door.openDoor()
                        elif switch.x == self.player.x and switch.y == self.player.y:
                            switch.checked = True
                            if switch.isSwitched == False:
                                switch.switchOn()
                            if door.doorType == switch.switchType:
                                door.checked = True
                                if door.isOpen == False:
                                    door.openDoor()
        for door in self.doors:
            if self.player.x == door.x and (self.player.y == door.y + 1 or self.player.y == door.y - 1):
                        if len(self.inventory.item_list) > 0:
                            if type(self.inventory.item_list[0]) == Key:
                                if door.doorType == 'Exit' or door.doorType == "Chest":
                                    door.unlocked = True
                                    door.openDoor()
                                    self.inventory.item_list.pop()
            elif self.player.y == door.y and (self.player.x == door.x + 1 or self.player.x == door.x - 1):
                        if len(self.inventory.item_list) > 0:
                            if type(self.inventory.item_list[0]) == Key:
                                if door.doorType == 'Exit' or door.doorType == "Chest":
                                    door.unlocked = True
                                    door.openDoor()
                                    self.inventory.item_list.pop()
            if self.player.x == door.x and self.player.y == door.y:
                if door.doorType == 'Chest':
                    self.game.go_to(VictoryScene(self.game))
                if door.doorType == 'Exit':
                    self.players.update()
                    self.render()
                    pygame.display.flip()
                    pygame.time.delay(500)
                    self.game.select_scene(self.scene_number + 1)
            #unactivate all the switched that no long have objects on them
            for switch in self.switches:
                if switch.checked == False and switch.isSwitched ==True:
                    switch.switchOff()
            for door in self.doors:
                if door.checked == False and door.isOpen == True and door.unlocked ==False:
                    door.closeDoor()
"""
Display Level 1: Tutorial Movement

- Simple tutorial, show player how to move character and what the objectives
    of the game are.
"""
class TutorialMovement(GameScene):
    def __init__(self, game):
        super().__init__(game)
        self.map = TiledMap(path.join(MAP_FOLDER, 'TutorialMovement.tmx'))
        self.scene_number = self.game.get_scene_number(TutorialMovement)
        self.draw_objects()
        self.instructions.add("Use the WASD keys to move around.", 100)
        self.instructions.add("Press P to pause the game.", 140)
        self.instructions.add("Get the key to unlock the door and proceed to the next level.", 180)


"""
Display Level 2: Tutorial Blocks
- Simple tutorial, shows player how to push blocks and using a switch to unlock
    the door
"""
class TutorialBlock(GameScene):
    def __init__(self, game):
        super().__init__(game)
        self.map = TiledMap(path.join(MAP_FOLDER, 'TutorialBlock.tmx'))
        self.scene_number = self.game.get_scene_number(TutorialBlock)
        self.draw_objects()
        self.instructions.add("You can move the blocks by standing next to them", 100)
        self.instructions.add("and pushing the directional buttons.", 140)
        self.instructions.add("Push the block on top of the switch to unlock the door.", 180)


"""
Display Level 3: Tutorial Enemy
- Simple tutorial, shows player how to attack and avoid enemies.
"""
class TutorialEnemy(GameScene):
    def __init__(self, game):
        super().__init__(game)
        self.map = TiledMap(path.join(MAP_FOLDER, 'TutorialEnemy.tmx'))
        self.scene_number = self.game.get_scene_number(TutorialEnemy)
        self.draw_objects()
        self.spawn_enemies()
        self.instructions.add("Press the Spacebar while standing next to an enemy to attack it.", 100)
        self.instructions.add("Make sure you don't run out of Hearts!", 140)

    def spawn_enemies(self):
        Enemy(self, 10, 5, LEFT, [])

        Enemy(self, 10, 15, UP, [UP, UP, UP, UP, UP,
                                 UP, UP, UP, UP])


"""
Display Level 4: Tutorial Ice
- Simple tutorial, shows player interaction with ice tiles between the
    player character and boxes.
"""
class TutorialIce(GameScene):
    def __init__(self, game):
        super().__init__(game)
        self.map = TiledMap(path.join(MAP_FOLDER, 'TutorialIce.tmx'))
        self.scene_number = self.game.get_scene_number(TutorialIce)
        self.draw_objects()
        self.instructions = Instructions(30, BLUE)
        self.instructions.add("Be careful on the ice!", 100)
        self.instructions.add("You will slide until you collide with an object.", 140)
        self.instructions.add("Try to position the blocks to help you", 180)
        self.instructions.add("reach the key and unlock the door.", 220)


"""
Display Level 5
- Level which teaches interaction between blocks, switches, and
    unlocking doors and the exit.
"""
class Level5(GameScene):
    def __init__(self, game):
        super().__init__(game)
        self.map = TiledMap(path.join(MAP_FOLDER, 'Level5.tmx'))
        self.scene_number = self.game.get_scene_number(Level5)
        self.draw_objects()


"""
Display Level 6: Complex Enemy
- Complex level featuring only enemies.
"""
class Level6(GameScene):
    def __init__(self, game):
        super().__init__(game)
        self.map = TiledMap(path.join(MAP_FOLDER, 'Level6.tmx'))
        self.scene_number = self.game.get_scene_number(Level6)
        self.draw_objects()
        self.spawn_enemies()

    def spawn_enemies(self):
        type_1 = [UP, UP, UP,
                  RIGHT, RIGHT, RIGHT, RIGHT,
                  RIGHT, RIGHT, RIGHT, RIGHT]

        type_2 = [DOWN, DOWN, DOWN,
                  LEFT, LEFT, LEFT, LEFT]

        type_3 = [DOWN, DOWN, DOWN,
                  RIGHT, RIGHT, RIGHT, RIGHT,
                  RIGHT, RIGHT, RIGHT, RIGHT,
                  UP, UP, UP, UP]

        type_4 = [UP, UP, UP,
                  LEFT, LEFT, LEFT, LEFT]

        type_5 = [DOWN, DOWN, DOWN, DOWN]

        type_6 = [UP, UP, UP, UP]

        Enemy(self, 2, 5, UP, type_1)
        Enemy(self, 6, 3, DOWN, type_2)
        Enemy(self, 10, 3, UP, type_3)
        Enemy(self, 14, 5, DOWN, type_4)
        Enemy(self, 16, 17, UP, [])
        Enemy(self, 14, 9, DOWN, type_5)
        Enemy(self, 12, 13, DOWN, type_6)
        Enemy(self, 10, 9, DOWN, type_5)

class Level7(GameScene):
    def __init__(self, game):
        super().__init__(game)
        self.map = TiledMap(path.join(MAP_FOLDER, 'Level7.tmx'))
        self.scene_number = self.game.get_scene_number(Level7)
        self.draw_objects()
"""
Display Level 8: Blocks and enemies
-
"""
class Level8(GameScene):
    def __init__(self, game):
        super().__init__(game)
        self.map = TiledMap(path.join(MAP_FOLDER, 'Level8.tmx'))
        self.scene_number = self.game.get_scene_number(Level8)
        self.draw_objects()
        self.spawn_enemies()

    def spawn_enemies(self):
        type_1 = [LEFT, LEFT,
                  DOWN,
                  LEFT, LEFT, LEFT, LEFT, LEFT]

        type_2 = [LEFT, LEFT,
                  UP,
                  LEFT, LEFT, LEFT, LEFT, LEFT]

        Ghost(self, 16, 8, DOWN, type_1)
        Ghost(self, 16, 12, DOWN, type_2)

"""
Display Level: More boxes
- Complex level featuring only enemies.
"""
class Level9(GameScene):
    def __init__(self, game):
        super().__init__(game)
        self.map = TiledMap(path.join(MAP_FOLDER, 'Level9.tmx'))
        self.scene_number = self.game.get_scene_number(Level9)
        self.draw_objects()
        self.spawn_enemies()

    def spawn_enemies(self):
        type_1 = [UP, UP, UP,
                  RIGHT, RIGHT, RIGHT, RIGHT,
                  RIGHT, RIGHT, RIGHT, RIGHT]

        type_2 = [DOWN, DOWN, DOWN,
                  LEFT, LEFT, LEFT, LEFT]

        type_3 = [DOWN, DOWN, DOWN,
                  RIGHT, RIGHT, RIGHT, RIGHT,
                  RIGHT, RIGHT, RIGHT, RIGHT,
                  UP, UP, UP, UP]

        type_4 = [UP, UP, UP,
                  LEFT, LEFT, LEFT, LEFT]

        Enemy(self, 5, 5, UP, type_1)
        Enemy(self, 6, 15, DOWN, type_2)
        Enemy(self, 15, 15, UP, type_3)
        Enemy(self, 16, 4, DOWN, type_4)
"""
Display Level 10: Final level with Treasure Chest
-
"""
class Level10(GameScene):
    def __init__(self, game):
        super().__init__(game)
        self.map = TiledMap(path.join(MAP_FOLDER, 'Level10.tmx'))
        self.scene_number = self.game.get_scene_number(Level10)
        self.draw_objects()
        self.spawn_enemies()

    def spawn_enemies(self):
        type_1 = [LEFT, LEFT,
                  DOWN,
                  LEFT, LEFT, LEFT, LEFT, LEFT]

        type_2 = [LEFT, LEFT,
                  UP,
                  LEFT, LEFT, LEFT, LEFT, LEFT]

        type_3 = [RIGHT, RIGHT, RIGHT ,RIGHT,
                    DOWN, LEFT, LEFT, LEFT]
        type_4 = [RIGHT, RIGHT, RIGHT,
                    DOWN, DOWN,
                    LEFT, LEFT, LEFT]

        Ghost(self, 6, 14, DOWN, type_2)
        Enemy(self, 16, 8, DOWN, type_1)
        Ghost(self, 12, 14, DOWN, type_3)
        Enemy(self, 2, 17, DOWN, type_3)
        Enemy(self, 2, 3, DOWN, type_4)

class DevRoom(GameScene):
    def __init__(self, game):
        super().__init__(game)
        self.map = TiledMap(path.join(MAP_FOLDER, 'TutorialMovement.tmx'))
        self.scene_number = self.game.get_scene_number(Level8)
        self.draw_objects()
        self.spawn_enemies()

    def spawn_enemies(self):
        type_1 = []

        Ghost(self, 16, 8, DOWN, type_1)
        Ghost(self, 16, 12, DOWN, type_1)

"""
Unit test scene for blocks
"""
class BlockUnitTest(GameScene):
    def __init__(self, game):
        super().__init__(game)
        self.scene_number = self.game.get_scene_number(BlockUnitTest)
        self.draw_layout("blockUnitTest.map")


# Sources:
# https://github.com/kidscancode/pygame_tutorials/blob/master/tilemap/part%2007/main.py
# https://stackoverflow.com/questions/14700889/pygame-level-menu-states
