import pygame, sys
from Screen import Screen, Spritesheet
from Map import Map
from pygame.locals import *
            

class Game(object):
    def __init__(self):
        self.screen = Screen()
        self.clock = pygame.time.Clock()
        self.map = Map()
        self.map.generate_map()
        self.run()
        
    def run(self):
        
        while 1:
            self.clock.tick(30)
            for event in pygame.event.get():
                            if not hasattr(event, 'key'): continue
                            if event.key == K_ESCAPE: sys.exit(0)
            self.screen.draw_screen_layers()

def main():
    while 1:
        game = Game()
     
if __name__ == "__main__":
    main()