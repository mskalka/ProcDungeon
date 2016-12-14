from Map import Map
import random


class Player(object):

    xpos, ypos = None, None

    def __init__(self):
        start_room = random.choice(Map.room_list)
        print(start_room.center[0], start_room.center[1])
        Player.xpos = start_room.center[0]
        Player.ypos = start_room.center[1]


    def get_pos(self):
        return self.xpos, self.ypos

    def set_pos(self, x, y):
        self.xpos = x
        self.ypos = y

    def move(self, x, y):
        if self.check_intersect(self.xpos, self.ypos, x, y):
            Player.xpos += x
            Player.ypos += y

    def check_intersect(self, xpos, ypos, xdelta, ydelta):
        return not Map.map_abstract[ypos + ydelta][xpos + xdelta] == 7
