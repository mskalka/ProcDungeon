import pygame
from Map import Map
from Player import Player


class Screen(object):
    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 900
    mapyoffset = 0
    mapxoffset = 0

    def __init__(self):
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH,
                                              self.SCREEN_HEIGHT))
        self.screen.fill((0, 0, 0))

    def draw_player(self):
        xcord = (Player.xpos * 16)
        ycord = (Player.ypos * 16)
        sprites = Spritesheet('spritesheet.png')
        player = sprites.image_at((32, 0, 16, 16))
        self.screen.blit(player, (ycord, xcord))

    def draw_map(self):
        self.screen.fill((0, 0, 0))
        sprites = Spritesheet('spritesheet.png')
        wall1 = sprites.image_at((0, 0, 16, 16))
        wall2 = sprites.image_at((0, 16, 16, 16))
        wall3 = sprites.image_at((0, 32, 16, 16))
        floor1 = sprites.image_at((16, 0, 16, 16))
        floor2 = sprites.image_at((16, 16, 16, 16))
        floor3 = sprites.image_at((16, 32, 16, 16))
        door = sprites.image_at((32, 0, 16, 16))
        for i in range(0, Map.y):
            for j in range(0, Map.x):
                ycord = (i * 16) - self.mapxoffset
                xcord = (j * 16) - self.mapyoffset
                if Map.map_abstract[i][j] == 7:
                    self.screen.blit(wall1, (ycord, xcord))
                elif Map.map_abstract[i][j] == 8:
                    self.screen.blit(wall2, (ycord, xcord))
                elif Map.map_abstract[i][j] == 9:
                    self.screen.blit(wall3, (ycord, xcord))
                elif Map.map_abstract[i][j] == 4:
                    self.screen.blit(floor1, (ycord, xcord))
                elif Map.map_abstract[i][j] == 5:
                    self.screen.blit(floor1, (ycord, xcord))
                elif Map.map_abstract[i][j] == 6:
                    self.screen.blit(floor3, (ycord, xcord))
                elif Map.map_abstract[i][j] == 2:
                    self.screen.blit(door, (ycord, xcord))

    def draw_screen_layers(self):
        self.draw_map()
        self.draw_player()
        pygame.display.flip()


class Spritesheet(object):
    def __init__(self, filename):
        try:
            self.sheet = pygame.image.load(filename).convert()
        except pygame.error, message:
            print 'Unable to load spritesheet image:', filename
            raise SystemExit, message

    # Load a specific image from a specific rectangle
    def image_at(self, rectangle, colorkey=None):
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

    # Load a whole bunch of images and return them as a list
    def images_at(self, rects, colorkey=None):
        return [self.image_at(rect, colorkey) for rect in rects]

    # Load a whole strip of images
    def load_strip(self, rect, image_count, colorkey=None):
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)
