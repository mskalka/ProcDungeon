import pygame
import random
from Map import Map
from Player import Player


class Screen(object):
    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 900
    mapyoffset = 0
    mapxoffset = 0

    def __init__(self, current_map):
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH,
                                              self.SCREEN_HEIGHT))
        self.screen.fill((0, 0, 0))
        self.map = current_map
        self.sprites = Spritesheet('spritesheet.png')

    def draw_player(self):
        xcord = (Player.xpos * 16)
        ycord = (Player.ypos * 16)
        player = self.sprites.image_at((192, 0, 16, 16))
        self.screen.blit(player, (ycord, xcord))

    def draw_map(self):
        walls = [self.sprites.image_at((0, 0, 16, 16)),
                 self.sprites.image_at((0, 16, 16, 16)),
                 self.sprites.image_at((0, 32, 16, 16))]
        floors = [self.sprites.image_at((16, 0, 16, 16)),
                  self.sprites.image_at((16, 16, 16, 16)),
                  self.sprites.image_at((16, 32, 16, 16))]
        door = self.sprites.image_at((32, 0, 16, 16))

        for i in range(1, self.map.y):
            for j in range(1, self.map.x):
                ycord = (i * 16) - self.mapyoffset
                xcord = (j * 16) - self.mapxoffset
                if self.map.map_abstract[i][j] == 7:
                    self.screen.blit(walls[1], (ycord, xcord))
                elif self.map.map_abstract[i][j] == 4:
                    self.screen.blit(floors[2], (ycord, xcord))
                elif self.map.map_abstract[i][j] == 2:
                    self.screen.blit(door, (ycord, xcord))

    def draw_wall_toppers(self):
        # Store the sprites for the wall tops.
        wall_toppers = [self.sprites.image_at((112, 16, 16, 16)),
                        self.sprites.image_at((80, 32, 16, 16)),
                        self.sprites.image_at((96, 0, 16, 16)),
                        self.sprites.image_at((48, 48, 16, 16)),
                        self.sprites.image_at((48, 32, 16, 16)),
                        self.sprites.image_at((64, 32, 16, 16)),
                        self.sprites.image_at((64, 48, 16, 16)),
                        self.sprites.image_at((64, 16, 16, 16)),
                        self.sprites.image_at((48, 16, 16, 16)),
                        self.sprites.image_at((64, 0, 16, 16)),
                        self.sprites.image_at((48, 0, 16, 16)),
                        self.sprites.image_at((80, 48, 16, 16)),
                        self.sprites.image_at((80, 32, 16, 16)),
                        self.sprites.image_at((80, 0, 16, 16)),
                        self.sprites.image_at((112, 0, 16, 16)),
                        self.sprites.image_at((96, 48, 16, 24))]

        for i in range(1, self.map.y):
            for j in range(1, self.map.x):
                ycord = (i * 16)
                xcord = (j * 16) - 8
                # Logic for walls here:
                try:
                    cross = (self.map.map_abstract[i][j] == 7 and  # Is wall
                             self.map.map_abstract[i - 1][j] == 7 and  # Wall above
                             self.map.map_abstract[i + 1][j] == 7 and  # Wall Below
                             self.map.map_abstract[i][j - 1] == 7 and  # Wall Left
                             self.map.map_abstract[i][j + 1] == 7)  # Wall right
                except IndexError:
                    continue
                else:
                    if cross:
                        self.screen.blit(wall_toppers[0], (ycord, xcord))  # It's a cross
                try:
                    horz = (self.map.map_abstract[i][j] == 7 and  # Is wall
                            self.map.map_abstract[i - 1][j] == 7 and  # Wall left
                            self.map.map_abstract[i + 1][j] == 7 and  # Wall right
                            self.map.map_abstract[i][j - 1] == 4 and  # Floor Above
                            self.map.map_abstract[i][j + 1] == 4)  # Floor Below
                except IndexError:
                    continue
                else:
                    if horz:
                        self.screen.blit(wall_toppers[2], (ycord, xcord))  # It's a horz
                try:
                    vert = (self.map.map_abstract[i][j] == 7 and  # Is wall
                            self.map.map_abstract[i][j - 1] == 7 and  # Wall Above
                            self.map.map_abstract[i][j + 1] == 7 and  # Wall Below
                            self.map.map_abstract[i - 1][j] == 4 and  # Floor Left
                            self.map.map_abstract[i + 1][j] == 4)  # Floor Right
                except IndexError:
                    continue
                else:
                    if vert:
                        self.screen.blit(wall_toppers[1], (ycord, xcord))  # It's a horz

                try:
                    up_t = (self.map.map_abstract[i][j] == 7 and  # Is wall
                            self.map.map_abstract[i - 1][j] == 7 and  # Wall above
                            self.map.map_abstract[i + 1][j] == 7 and  # Wall Below
                            self.map.map_abstract[i][j - 1] == 7 and
                            self.map.map_abstract[i][j + 1] == 4)  # Floor down
                except IndexError:
                    continue
                else:
                    if up_t:
                        self.screen.blit(wall_toppers[5], (ycord, xcord))  # It's an up T
                try:
                    down_t = (self.map.map_abstract[i][j] == 7 and  # Is wall
                              self.map.map_abstract[i - 1][j] == 7 and  # Wall above
                              self.map.map_abstract[i + 1][j] == 7 and  # Wall Below
                              self.map.map_abstract[i][j + 1] == 7 and  # Wall right
                              self.map.map_abstract[i][j - 1] == 4)  # Floor up
                except IndexError:
                    continue
                else:
                    if down_t:
                        self.screen.blit(wall_toppers[6], (ycord, xcord))  # It's a down T
                try:
                    left_t = (self.map.map_abstract[i][j] == 7 and  # Is wall
                              self.map.map_abstract[i][j - 1] == 7 and  # Wall above
                              self.map.map_abstract[i][j + 1] == 7 and  # Wall Below
                              self.map.map_abstract[i - 1][j] == 7 and  # Wall right
                              self.map.map_abstract[i + 1][j] == 4)  # Floor Left
                except IndexError:
                    continue
                else:
                    if left_t:
                        self.screen.blit(wall_toppers[3], (ycord, xcord))  # It's a left T
                try:
                    left_t = (self.map.map_abstract[i][j] == 7 and  # Is wall
                              self.map.map_abstract[i][j - 1] == 7 and  # Wall above
                              self.map.map_abstract[i][j + 1] == 7 and  # Wall Below
                              self.map.map_abstract[i + 1][j] == 7 and  # Wall right
                              self.map.map_abstract[i - 1][j] == 4)  # Floor Left
                except IndexError:
                    continue
                else:
                    if left_t:
                        self.screen.blit(wall_toppers[4], (ycord, xcord))  # It's a left T
                try:
                    r_u_corner = (self.map.map_abstract[i][j] == 7 and  # Is wall
                                  self.map.map_abstract[i][j - 1] == 4 and  # Floor above
                                  self.map.map_abstract[i][j + 1] == 7 and  # Wall Below
                                  self.map.map_abstract[i + 1][j] == 4 and  # Floor right
                                  self.map.map_abstract[i - 1][j] == 7)  # Wall Left
                except IndexError:
                    continue
                else:
                    if r_u_corner:  # It's a right up corner
                        self.screen.blit(wall_toppers[9], (ycord, xcord))
                try:
                    l_u_corner = (self.map.map_abstract[i][j] == 7 and  # Is wall
                                  self.map.map_abstract[i][j - 1] == 4 and  # Floor above
                                  self.map.map_abstract[i][j + 1] == 7 and  # Wall Below
                                  self.map.map_abstract[i - 1][j] == 4 and  # Floor right
                                  self.map.map_abstract[i + 1][j] == 7)  # Wall Left
                except IndexError:
                    continue
                else:
                    if l_u_corner:  # It's a left up corner
                        self.screen.blit(wall_toppers[10], (ycord, xcord))
                try:
                    l_d_corner = (self.map.map_abstract[i][j] == 7 and  # Is wall
                                  self.map.map_abstract[i][j + 1] == 4 and  # Floor below
                                  self.map.map_abstract[i][j - 1] == 7 and  # Wall above
                                  self.map.map_abstract[i - 1][j] == 4 and  # Floor right
                                  self.map.map_abstract[i + 1][j] == 7)  # Wall Left
                except IndexError:
                    continue
                else:
                    if l_d_corner:  # It's a left down corner
                        self.screen.blit(wall_toppers[8], (ycord, xcord))
                try:
                    r_d_corner = (self.map.map_abstract[i][j] == 7 and  # Is wall
                                  self.map.map_abstract[i][j + 1] == 4 and  # Floor below
                                  self.map.map_abstract[i][j - 1] == 7 and  # Wall above
                                  self.map.map_abstract[i - 1][j] == 7 and  # Wall right
                                  self.map.map_abstract[i + 1][j] == 4)  # Floor Left
                except IndexError:
                    continue
                else:
                    if r_d_corner:  # It's a right down corner
                        self.screen.blit(wall_toppers[7], (ycord, xcord))
                try:
                    down = (self.map.map_abstract[i][j] == 7 and  # Is wall
                            self.map.map_abstract[i][j + 1] == 4 and  # Floor below
                            self.map.map_abstract[i][j - 1] == 7 and  # Wall above
                            self.map.map_abstract[i - 1][j] == 4 and  # Floor right
                            self.map.map_abstract[i + 1][j] == 4)  # Floor Left
                except IndexError:
                    continue
                else:
                    if down:  # It's a down
                        self.screen.blit(wall_toppers[11], (ycord, xcord))
                try:
                    up = (self.map.map_abstract[i][j] == 7 and  # Is wall
                          self.map.map_abstract[i][j + 1] == 7 and  # Wall below
                          self.map.map_abstract[i][j - 1] == 4 and  # Floor above
                          self.map.map_abstract[i - 1][j] == 4 and  # Floor right
                          self.map.map_abstract[i + 1][j] == 4)  # Floor Left
                except IndexError:
                    continue
                else:
                    if up:  # It's an up
                        self.screen.blit(wall_toppers[12], (ycord, xcord))
                try:
                    left = (self.map.map_abstract[i][j] == 7 and  # Is wall
                            self.map.map_abstract[i][j + 1] == 4 and  # Floor below
                            self.map.map_abstract[i][j - 1] == 4 and  # Floor above
                            self.map.map_abstract[i - 1][j] == 7 and  # Wall right
                            self.map.map_abstract[i + 1][j] == 4)  # Floor Left
                except IndexError:
                    continue
                else:
                    if left:  # It's a left
                        self.screen.blit(wall_toppers[14], (ycord, xcord))
                try:
                    right = (self.map.map_abstract[i][j] == 7 and  # Is wall
                             self.map.map_abstract[i][j + 1] == 4 and  # Floor below
                             self.map.map_abstract[i][j - 1] == 4 and  # Floor above
                             self.map.map_abstract[i - 1][j] == 4 and  # Floor right
                             self.map.map_abstract[i + 1][j] == 7)  # Wall Left
                except IndexError:
                    continue
                else:
                    if right:  # It's a right
                        self.screen.blit(wall_toppers[13], (ycord, xcord))
                try:
                    pillar = (self.map.map_abstract[i][j] == 7 and  # Is wall
                              self.map.map_abstract[i][j + 1] == 4 and  # Floor below
                              self.map.map_abstract[i][j - 1] == 4 and  # Floor above
                              self.map.map_abstract[i - 1][j] == 4 and  # Floor right
                              self.map.map_abstract[i + 1][j] == 4)  # Floor Left
                except IndexError:
                    continue
                else:
                    if pillar:  # It's a pillar
                        self.screen.blit(wall_toppers[15], (ycord, xcord))

    def draw_fog(self):
        for i in range(0, self.map.y):
            for j in range(0, self.map.x):
                if self.map.revealed_map[i][j] != 1:
                    black = self.sprites.image_at((144, 0, 16, 16))
                    ycord = (i * 16) - self.mapxoffset
                    xcord = (j * 16) - self.mapyoffset
                    self.screen.blit(black, (ycord, xcord))

    def draw_screen_layers(self):
        self.screen.fill((0, 0, 0))
        self.draw_map()
        self.draw_player()
        self.draw_wall_toppers()
        self.draw_fog()
        pygame.display.update()


class Spritesheet(object):
    def __init__(self, filename):
        try:
            self.sheet = pygame.image.load(filename).convert()
        except pygame.error, message:
            print 'Unable to load spritesheet image:', filename
            raise FileNotFoundError(filename)

    # Load a specific image from a specific rectangle
    def image_at(self, rectangle, colorkey=None):
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
            image.convert_alpha()
        return image

    # Load a whole bunch of images and return them as a list
    def images_at(self, rects, colorkey=None):
        return [self.image_at(rect, colorkey) for rect in rects]

    # Load a whole strip of images
    def load_strip(self, rect, image_count, colorkey=None):
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)
