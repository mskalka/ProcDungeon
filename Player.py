from Map import Map
import random


class Player(object):

    xpos, ypos = None, None

    def __init__(self, current_map):
        self.current_map = current_map
        start_room = random.choice(current_map.room_list)
        print(start_room.center[0], start_room.center[1])
        Player.xpos = start_room.center[0]
        Player.ypos = start_room.center[1]
        self.vision = 1
        self.uncover_map()

    def get_pos(self):
        return self.xpos, self.ypos

    def set_pos(self, x, y):
        self.xpos = x
        self.ypos = y

    def move(self, x, y):
        if self.check_intersect(self.xpos, self.ypos, x, y):
            Player.xpos += x
            Player.ypos += y
        self.uncover_map()

    def uncover_map(self):
        for i in range(-2 * self.vision, (2 * self.vision) + 1):
            for j in range(-2 * self.vision, (2 * self.vision) + 1):
                try:
                    self.current_map.revealed_map[Player.ypos + i][Player.xpos + j] = 1
                except IndexError:
                    continue

    def check_intersect(self, xpos, ypos, xdelta, ydelta):
        try:
            return not self.current_map.map_abstract[ypos + ydelta][xpos + xdelta] == 7
        except IndexError:
            return False
