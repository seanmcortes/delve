import sys
from os import path
import pygame
import pygame.freetype
from settings import *
from sprites import *
from scenes import Level1Scene, TutorialEnemy, TutorialIce
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
        self.title_font = None # sub-initialization in load_data()
        self.map_folder = None # sub-init in load_data()
        self.debug = False
        self.load_data()

        if "-debug" in sys.argv:
            self.debug = True

        # Naive debug menu. e.g. 'python main.py -debug Level1Scene'
        if self.debug:
            function_index = sys.argv.index("-debug") + 1
            self.go_to(eval(sys.argv[function_index])(self))
        else:
            #self.go_to(TutorialIce(self))
            self.go_to(MainMenuScene(self))

    def load_data(self):
        game_folder = path.dirname(__file__)
        image_folder = path.join(game_folder, 'image')
        self.title_font = path.join(image_folder, 'Cutefont')
        self.map_folder = path.join(game_folder, 'maps')

    def go_to(self, scene):
        self.scene = scene

    def run(self):
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.scene.handle_events(pygame.event.get())
            self.scene.update()
            self.scene.render()
            pygame.display.flip()

    def select_scene(self, level):
        #Source: https://jaxenter.com/implement-switch-case-statement-python-138315.html
        switcher = {
            1: Level1Scene,
            2: GameOverScene,
            3: GameOverScene,
            4: GameOverScene,
            5: GameOverScene,
            6: GameOverScene,
            7: GameOverScene,
            8: GameOverScene,
            9: GameOverScene,
            10: GameOverScene
        }
        # Get the function from switcher dictionary
        func = switcher.get(level, lambda: "Invalid level")
        # Execute the function
        if level > 1: #this is just here until we implement the other levels, becuase GameOverScene requires the game be passed to it
            self.go_to(func(self))
        else:
            self.go_to(func(self))


def main():
    delve = Game()

    while True:
        delve.run()


if __name__ == "__main__":
    main()


# Sources:
# https://github.com/kidscancode/pygame_tutorials/blob/master/tilemap/part%2007/main.py
# https://stackoverflow.com/questions/14700889/pygame-level-menu-states
