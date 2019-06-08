import sys
from os import path
import pygame
import pygame.freetype
from settings import *
from sprites import *
from scenes import Level1Scene, TutorialEnemy, TutorialIce, BlockUnitTest
from menu import *
import unittest

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        pygame.key.set_repeat(500, 100)
        self.playing = True
        self.dt = None # sub-initialization in run()
        self.scene = None # sub-initialization in go_to()
        self.title_font = None # sub-initialization in load_data()
        self.map_folder = None # sub-init in load_data()
        self.debug = False
        self.scene_dictionary = {
                    1: Level1Scene,
                    2: GameOverScene,
                    3: GameOverScene,
                    4: GameOverScene,
                    5: GameOverScene,
                    6: GameOverScene,
                    7: GameOverScene,
                    8: GameOverScene,
                    9: GameOverScene,
                    10: GameOverScene,
                    11: TutorialEnemy,
                    12: TutorialIce,
                    13: BlockUnitTest
                }
        self.load_data()

        if "-debug" in sys.argv:
            self.debug = True

        # Naive debug menu. e.g. 'python main.py -debug Level1Scene'
        if self.debug:
            function_index = sys.argv.index("-debug") + 1
            self.go_to(eval(sys.argv[function_index])(self))
        else:
            self.go_to(BlockUnitTest(self))
            #self.go_to(MainMenuScene(self))

    def load_data(self):
        game_folder = path.dirname(__file__)
        image_folder = path.join(game_folder, 'image')
        self.title_font = path.join(image_folder, 'Cutefont')
        self.map_folder = path.join(game_folder, 'maps')
        self.player_sprite_sheet = path.join(image_folder, 'Player.png')
        self.box_sprite_sheet = path.join(image_folder, 'Box.png')
        self.bat_sprite_sheet = path.join(image_folder, 'Bat.png')

    def go_to(self, scene):
        self.scene = scene

    def run(self):
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.scene.handle_events(pygame.event.get())
            self.scene.update()
            self.scene.render()
            pygame.display.flip()

    ################################################################################
    #Description: Loads a scene
    #Args:
    #   self: a copy of the Game object
    #   level: the scene you want to load
    ###############################################################################
    def select_scene(self, level):
        # Get the function from switcher dictionary
        #Source: https://jaxenter.com/implement-switch-case-statement-python-138315.html
        func = self.scene_dictionary.get(level, lambda: 0)
        # Execute the function
        if level > 1: #this is just here until we implement the other levels, becuase GameOverScene requires the game be passed to it
            self.go_to(func(self))
        else:
            self.go_to(func(self))
    ################################################################################
    # Description: Returns a scene number based on a scene name
    # Args:
    #   self: a copy of the Game object
    #   scene_name: the name of the scene you want to load (string)
    # Returns: the scene number
    ###############################################################################
    def get_scene_number(self, scene_name):
        #create a reverse dictionary to look up scene number by scene name
        inverse_scene_dictionary= {v: k for k, v in self.scene_dictionary.items()} #Python 3 version
        #Source: https://stackoverflow.com/questions/483666/python-reverse-invert-a-mapping
        # Get the function from switcher dictionary
        #Source: https://jaxenter.com/implement-switch-case-statement-python-138315.html
        scene_number = inverse_scene_dictionary.get(scene_name, lambda: 0)
        return scene_number

delve = Game()

delve.dt = delve.clock.tick(FPS) / 1000

#delve.scene.player = Player(delve.scene, 0, 0)
Block(delve.scene, 5, 5)

blockCount = 0
for block in delve.scene.blocks:

    blockCount += 1
   
    success = block.move(dx=1, dy=0)

    testFailed = False
    if block.x != 6:
        print('TEST FAILURE, EXPECTED BLOCK.X VALUE of 2 | Actual value: {}'.format(block.x))
        testFailed = True
    if block.y != 5:
        print('TEST FAILURE, EXPECTED BLOCK.y VALUE of 0 | Actual value: {}'.format(block.y))
        testFailed = True

    if not testFailed:
        print("TEST PASSED")
    

