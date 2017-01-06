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

    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600

    def __init__(self):
        self.clock = pygame.time.Clock()
        self.map = Map(12, 14, 0)  # radius, rooms, fuzz
        self.player = Player(self.map)
        self.screen = Screen(self.player,
                             self.map,
                             self.SCREEN_WIDTH,
                             self.SCREEN_HEIGHT)
        self.dm = DungeonMaster(self.map)
        pygame.key.set_repeat(60, 60)

        self.run()

    def run(self):
        """
        # Test the Pathfinding:
        c = Creature(self.map.map_abstract)
        r = random.choice(self.map.room_list)
        print("Start:({}, {})".format(r.center[0], r.center[1]))
        print("Goal:({}, {})".format(Player.xpos, Player.ypos))
        p = c.path_to((r.center[0], r.center[1]), (Player.xpos, Player.ypos))
        """
        while 1:
            self.clock.tick(30)
            for event in pygame.event.get():
                self.pressed = pygame.key.get_pressed()
                if self.pressed[K_ESCAPE] or event.type == pygame.QUIT:
                    sys.exit(0)
                if self.pressed[K_UP]:
                    self.screen.mapyoffset += 16
                    # Player.move(self.player, -1, 0)
                if self.pressed[K_DOWN]:
                    self.screen.mapyoffset -= 16
                    # Player.move(self.player, 1, 0)
                if self.pressed[K_LEFT]:
                    self.screen.mapxoffset += 16
                    # Player.move(self.player, 0, -1)
                if self.pressed[K_RIGHT]:
                    self.screen.mapxoffset -= 16
                    # Player.move(self.player, 0, 1)
                else:
                    continue
            self.screen.draw_screen_layers()


def main():
    while 1:
        game = Game()


if __name__ == "__main__":
    main()
