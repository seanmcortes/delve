import sys
from os import path
import pygame
import pygame.freetype
from settings import *
from sprites import *
from scenes import Level1Scene, TutorialEnemy, TutorialIce, BlockUnitTest, TutorialBlocks
from menu import *

#
"""
Manages games scenes
"""
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
                    12: TutorialBlocks,
                    14: BlockUnitTest
                }
        # self.load_data()

        if "-debug" in sys.argv:
            self.debug = True

        # Naive debug menu. e.g. 'python main.py -debug Level1Scene'
        if self.debug:
            function_index = sys.argv.index("-debug") + 1
            self.go_to(eval(sys.argv[function_index])(self))
        else:
            # self.go_to(TutorialIce(self))
            self.go_to(MainMenuScene(self))

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


def main():
    delve = Game()

    while True:
        delve.run()


if __name__ == "__main__":
    main()


# Sources:
# https://github.com/kidscancode/pygame_tutorials/blob/master/tilemap/part%2007/main.py
# https://stackoverflow.com/questions/14700889/pygame-level-menu-states
# https://stackoverflow.com/questions/21937695/python-cx-freeze-name-file-is-not-defined