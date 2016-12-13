from Map import Map
import random


class Player(object):

    xpos = None
    ypos = None

    def __init__(self):
        start_room = random.choice(Map.room_list)
        print(start_room.center[0], start_room.center[1])
        self.xpos = start_room.center[0]
        self.ypos = start_room.center[1]

    def move(self, x, y):
        self.xpos += x
        self.ypos += y

    def check_intersect(self, xpos, ypos, xdelta, ydelta):
        if not Map.map_abstract[ypos + ydelta][xpos + xdelta] == 7:
            self.move(xdelta, ydelta)
