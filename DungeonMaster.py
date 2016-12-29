import random
from Creature import Creature
from Map import Map


class DungeonMaster(object):

    monsters_per_level = 10
    monsters = []

    def __init__(self, current_map):
        self.current_map = current_map

    def generate_creatures(self, num_monsters):
        for i in range(0, num_monsters):
            monsters[i] = Creature(self.current_map)
