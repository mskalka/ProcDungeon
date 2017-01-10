import pygame
import sys
import random
from Screen import Screen
from Map import Map
from Player import Player
from Creature import Creature
from DungeonMaster import DungeonMaster
from pygame.locals import *


class Game(object):

    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 800

    def __init__(self):
        """
        Start clock
        Create Screen
            Blank until fed map
            Create Camera
                Points to nothing until screen updates
        Create DM
            DM creates maps, player, creatures
            Then feeds map
        """
        self.clock = pygame.time.Clock()
        self.screen = Screen(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        self.dm = DungeonMaster(self.screen)
        pygame.key.set_repeat(60, 60)
        self.run()

    def run(self):
        while 1:
            self.clock.tick(30)
            
            self.dm.update()
            self.screen.draw_screen_layers()


def main():
    while 1:
        game = Game()


if __name__ == "__main__":
    main()
