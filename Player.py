from Map import Map
from Creature import Creature
import random
import pygame


class Player(Creature):

    def __init__(self, (x, y)=(0, 0)):
        super(Creature, self).__init__()
        self.current_map = None
        self.hp = 0
        self.inventory = {}

    def get_start_room(self):
        start = random.choice(self.current_map.room_list)
        (x, y) = (start.center[1] * 2, start.center[0] * 2)
        print "Start: {}, {}".format(x, y)
        return (x, y)
