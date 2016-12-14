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
        self.run()

    def run(self):

        while 1:
            self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        sys.exit(0)
                    if event.key == K_UP:
                        Player.move(self.player, -1, 0)
                    if event.key == K_DOWN:
                        Player.move(self.player, 1, 0)
                    if event.key == K_LEFT:
                        Player.move(self.player, 0,-1)
                    if event.key == K_RIGHT:
                        Player.move(self.player, 0, 1)
                else:
                    continue
            self.screen.draw_screen_layers()


def main():
    while 1:
        game = Game()


if __name__ == "__main__":
    main()
