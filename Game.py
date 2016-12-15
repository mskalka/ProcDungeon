import pygame
import sys
from Screen import Screen
from Map import Map
from Player import Player
from pygame.locals import *


class Game(object):

    def __init__(self):
        self.clock = pygame.time.Clock()
        self.map = Map(40, 40, 30, 3, 7)  # x, y, rooms, min, max
        self.screen = Screen(self.map)
        self.player = Player(self.map)
        pygame.key.set_repeat(60, 60)
        self.run()

    def run(self):

        while 1:
            self.clock.tick(30)
            for event in pygame.event.get():
                self.pressed = pygame.key.get_pressed()
                if self.pressed[K_ESCAPE]:
                    sys.exit(0)
                if self.pressed[K_UP]:
                    Player.move(self.player, -1, 0)
                if self.pressed[K_DOWN]:
                    Player.move(self.player, 1, 0)
                if self.pressed[K_LEFT]:
                    Player.move(self.player, 0, -1)
                if self.pressed[K_RIGHT]:
                    Player.move(self.player, 0, 1)

            self.screen.draw_screen_layers()


def main():
    while 1:
        game = Game()


if __name__ == "__main__":
    main()
