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

    def __init__(self):
        self.clock = pygame.time.Clock()
        self.map = Map(40, 40, 30, 3, 7)  # x, y, rooms, min, max
        self.screen = Screen(self.map)
        self.player = Player(self.map)
        self.dm = DungeonMaster(self.map)

        pygame.key.set_repeat(60, 60)

        self.run()

    def run(self):
        c = Creature(self.map.map_abstract)
        r = random.choice(self.map.room_list)
        print("Start:({}, {})".format(r.center[0], r.center[1]))
        print("Goal:({}, {})".format(Player.xpos, Player.ypos))
        c.path_to((r.center[0], r.center[1]), (Player.xpos, Player.ypos))

        while 1:
            self.clock.tick(30)
            for event in pygame.event.get():
                self.pressed = pygame.key.get_pressed()
                if self.pressed[K_ESCAPE] or event.type == pygame.QUIT:
                    sys.exit(0)
                if self.pressed[K_UP]:
                    Player.move(self.player, -1, 0)
                if self.pressed[K_DOWN]:
                    Player.move(self.player, 1, 0)
                if self.pressed[K_LEFT]:
                    Player.move(self.player, 0, -1)
                if self.pressed[K_RIGHT]:
                    Player.move(self.player, 0, 1)
                else:
                    continue
            self.screen.draw_screen_layers()


def main():
    while 1:
        game = Game()


if __name__ == "__main__":
    main()
