import sys
from os import path
import pygame
import pygame.freetype
from settings import *
from sprites import *
from scenes import *
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
        self.go_to(MainMenuScene(self))
        #

    def go_to(self, scene):
        self.scene = scene
        self.scene.Game = self

    def run(self):
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.scene.handle_events(pygame.event.get())
            self.scene.update()
            self.scene.render(self.screen)
            pygame.display.flip()


def main():
    delve = Game()

    while True:
        delve.run()


if __name__ == "__main__":
    main()
