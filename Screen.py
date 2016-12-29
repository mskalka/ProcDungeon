import pygame
import random
from Map import Map
from Player import Player


class Screen(object):
    mapyoffset = 0
    mapxoffset = 0

    def __init__(self, player, current_map, width, height):
        self.screen = pygame.display.set_mode((width, height))
        self.screen.fill((0, 0, 0))
        self.entities = pygame.sprite.LayeredUpdates()
        self.map = current_map
        self.spritesheet = Spritesheet('spritesheet.png')
        self.player = player
        self.map_surface = self.draw_map(width, height)

    def draw_player(self):
        xcord = (self.player.xpos * 16)
        ycord = (self.player.ypos * 16)
        player = self.spritesheet.image_at((192, 0, 16, 16))
        self.screen.blit(player, (ycord, xcord))

    def draw_map(self, width, height):
        """
        In order to cut down on the current number of blits and loops while the
        screen updates, we only call the draw map function once. This outputs the
        map to a seprate surface that we can move around our main screen.
        By positioning the surface by the map offset the map can be moved and
        the player can stand still. This will be further refined with the addition
        of a sane camera system that is softly bounded by the screen itself.
        AKA more to come.

        In addition to the map itself, the wall topper has to be drawn at a 8px
        offset above the walls to give a sense of depth. For now this is going to
        be a solid color until a more exact solution can be found.
        """

        wall = self.spritesheet.image_at((0, 0, 16, 16))
        floor = self.spritesheet.image_at((16, 32, 16, 16))

        x_min = 0
        y_min = 0
        x_max = 0
        y_max = 0

        for room in self.map.room_list:
            x_min = min(room.x1, x_min)
            y_min = min(room.y1, y_min)
            x_max = max(room.x2, x_max)
            y_max = max(room.y2, y_max)

        map_surface = pygame.Surface(((x_max + 3) * 16,
                                      (y_max + 3) * 16))

        print("X_min: {}, X_max: {}, Y_min: {}, Y_max: {}".format(x_min, x_max,
                                                                  y_min, y_max))

        for x in range(-100, 100):
            for y in range(-100, 100):
                ycord = (y * 16)
                xcord = (x * 16)
                map_surface.blit(wall, (xcord, ycord))

        for room in self.map.room_list:
            for x in range(room.x1, room.x2):
                for y in range(room.y1, room.y2):
                    ycord = (y * 16) + 16
                    xcord = (x * 16) + 16
                    map_surface.blit(floor, (xcord, ycord))

        for hall in self.map.hall_list:
            for x in range(hall.x1, hall.x2 + 1):
                for y in range(hall.y1, hall.y2 + 1):
                    ycord = (y * 16)
                    xcord = (x * 16)
                    map_surface.blit(floor, (xcord, ycord))
        map_surface.blit(floor, ((x_max + 1) * 16,
                                 (y_max + 1) * 16))
        return map_surface

    def draw_map_old(self):
        walls = [self.spritesheet.image_at((0, 0, 16, 16)),
                 self.spritesheet.image_at((0, 16, 16, 16)),
                 self.spritesheet.image_at((0, 32, 16, 16))]
        floors = [self.spritesheet.image_at((16, 0, 16, 16)),
                  self.spritesheet.image_at((16, 16, 16, 16)),
                  self.spritesheet.image_at((16, 32, 16, 16))]
        door = self.spritesheet.image_at((32, 0, 16, 16))

        for i in range(self.map.y):
            for j in range(self.map.x):
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
        wall_toppers = [self.spritesheet.image_at((112, 16, 16, 16)),
                        self.spritesheet.image_at((80, 32, 16, 16)),
                        self.spritesheet.image_at((96, 0, 16, 16)),
                        self.spritesheet.image_at((48, 48, 16, 16)),
                        self.spritesheet.image_at((48, 32, 16, 16)),
                        self.spritesheet.image_at((64, 32, 16, 16)),
                        self.spritesheet.image_at((64, 48, 16, 16)),
                        self.spritesheet.image_at((64, 16, 16, 16)),
                        self.spritesheet.image_at((48, 16, 16, 16)),
                        self.spritesheet.image_at((64, 0, 16, 16)),
                        self.spritesheet.image_at((48, 0, 16, 16)),
                        self.spritesheet.image_at((80, 48, 16, 16)),
                        self.spritesheet.image_at((80, 32, 16, 16)),
                        self.spritesheet.image_at((80, 0, 16, 16)),
                        self.spritesheet.image_at((112, 0, 16, 16)),
                        self.spritesheet.image_at((96, 48, 16, 24))]

        for i in range(1, self.map.y):
            for j in range(1, self.map.x):
                ycord = (i * 16)
                xcord = (j * 16) - 8
                # Logic for walls here:
                if self.map.map_abstract[i][j] == 7:
                    if (self.check_tile(i + 1, j, 7) and
                       self.check_tile(i - 1, j, 7) and
                       self.check_tile(i, j - 1, 7) and
                       self.check_tile(i, j + 1, 7)):
                            # It's a cross
                            self.screen.blit(wall_toppers[0], (ycord, xcord))

                    if (self.check_tile(i + 1, j, 7) and  # Below
                       self.check_tile(i - 1, j, 7) and  # Above
                       self.check_tile(i, j - 1, 4) and  # Left
                       self.check_tile(i, j + 1, 4)):  # Right
                            self.screen.blit(wall_toppers[2], (ycord, xcord))
                    if (self.check_tile(i + 1, j, 4) and
                       self.check_tile(i - 1, j, 4) and
                       self.check_tile(i, j - 1, 7) and
                       self.check_tile(i, j + 1, 7)):
                            self.screen.blit(wall_toppers[1], (ycord, xcord))
                    if (self.check_tile(i + 1, j, 7) and
                       self.check_tile(i - 1, j, 7) and
                       self.check_tile(i, j - 1, 7) and
                       self.check_tile(i, j + 1, 4)):
                            self.screen.blit(wall_toppers[5], (ycord, xcord))
                    if (self.check_tile(i + 1, j, 7) and
                       self.check_tile(i - 1, j, 7) and
                       self.check_tile(i, j - 1, 4) and
                       self.check_tile(i, j + 1, 7)):
                            self.screen.blit(wall_toppers[6], (ycord, xcord))
                    if (self.check_tile(i + 1, j, 4) and
                       self.check_tile(i - 1, j, 7) and
                       self.check_tile(i, j - 1, 7) and
                       self.check_tile(i, j + 1, 7)):
                            self.screen.blit(wall_toppers[3], (ycord, xcord))
                    if (self.check_tile(i + 1, j, 7) and
                       self.check_tile(i - 1, j, 4) and
                       self.check_tile(i, j - 1, 7) and
                       self.check_tile(i, j + 1, 7)):
                            self.screen.blit(wall_toppers[4], (ycord, xcord))
                    if (self.check_tile(i + 1, j, 4) and
                       self.check_tile(i - 1, j, 7) and
                       self.check_tile(i, j - 1, 4) and
                       self.check_tile(i, j + 1, 7)):
                            self.screen.blit(wall_toppers[9], (ycord, xcord))
                    if (self.check_tile(i + 1, j, 7) and
                       self.check_tile(i - 1, j, 4) and
                       self.check_tile(i, j - 1, 4) and
                       self.check_tile(i, j + 1, 7)):
                            self.screen.blit(wall_toppers[10], (ycord, xcord))
                    if (self.check_tile(i + 1, j, 7) and
                       self.check_tile(i - 1, j, 4) and
                       self.check_tile(i, j - 1, 7) and
                       self.check_tile(i, j + 1, 4)):
                            self.screen.blit(wall_toppers[8], (ycord, xcord))
                    if (self.check_tile(i + 1, j, 4) and
                       self.check_tile(i - 1, j, 7) and
                       self.check_tile(i, j - 1, 7) and
                       self.check_tile(i, j + 1, 4)):
                            self.screen.blit(wall_toppers[7], (ycord, xcord))
                    if (self.check_tile(i + 1, j, 4) and
                       self.check_tile(i - 1, j, 4) and
                       self.check_tile(i, j - 1, 7) and
                       self.check_tile(i, j + 1, 4)):
                            self.screen.blit(wall_toppers[11], (ycord, xcord))
                    if (self.check_tile(i + 1, j, 4) and
                       self.check_tile(i - 1, j, 4) and
                       self.check_tile(i, j - 1, 4) and
                       self.check_tile(i, j + 1, 7)):
                            self.screen.blit(wall_toppers[12], (ycord, xcord))
                    if (self.check_tile(i + 1, j, 4) and
                       self.check_tile(i - 1, j, 7) and
                       self.check_tile(i, j - 1, 4) and
                       self.check_tile(i, j + 1, 4)):
                            self.screen.blit(wall_toppers[14], (ycord, xcord))
                    if (self.check_tile(i + 1, j, 7) and
                       self.check_tile(i - 1, j, 4) and
                       self.check_tile(i, j - 1, 4) and
                       self.check_tile(i, j + 1, 4)):
                            self.screen.blit(wall_toppers[13], (ycord, xcord))
                    if (self.check_tile(i + 1, j, 4) and
                       self.check_tile(i - 1, j, 4) and
                       self.check_tile(i, j - 1, 4) and
                       self.check_tile(i, j + 1, 4)):
                            self.screen.blit(wall_toppers[15], (ycord, xcord))

    def check_tile(self, y, x, tile):
        try:
            is_tile = self.map.map_abstract[y][x] == tile
        except IndexError:
            return True
        else:
            return is_tile

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
        self.screen.blit(self.map_surface, (self.mapxoffset, self.mapyoffset))
        # self.draw_path()
        # self.draw_player()
        pygame.display.flip()


class Spritesheet(object):
    def __init__(self, filename):
        try:
            self.sheet = pygame.image.load(filename).convert_alpha()
        except pygame.error, message:
            print 'Unable to load spritesheetheet image:', filename
            raise FileNotFoundError(filename)

    # Load a specific image from a specific rectangle
    def image_at(self, rectangle, colorkey=0):
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


class Sprite(pygame.sprite.Sprite):
    def __init__(self, image, pos=(0, 0)):
        super(Sprite, self).__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.pos = pos

    def _get_pos(self):
        return (self.rect.midbottom[0]-16)/16, (self.rect.midbottom[1]-16)/16

    def _set_pos(self, pos):
        self.rect.midbottom = pos[0]*16+16, pos[1]*16+16
        self.depth = self.rect.midbottom[1]

    pos = property(_get_pos, _set_pos)

    def move(self, dx, dy):
        self.rect.move_ip(dx, dy)
        self.depth = self.rect.midbottom[1]
