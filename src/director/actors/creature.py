import networkx as nx


class Creature(object):

    def __init__(self):
        self.xpos = 0
        self.ypos = 0

    def update(self):
        if self.path:
            self.move(path[:1])

    def set_map(self, current_map):
        self.current_map = current_map

    def set_pos(self, (x, y)):
        self.xpos = x
        self.ypos = y

    def move(self, (x, y)):
        if self.check_intersect(self.xpos, self.ypos, x, y):
            self.xpos += x
            self.ypos += y
            return True
        else:
            return False

    def check_intersect(self, xpos, ypos, xdelta, ydelta):
        return not self.current_map.final_map[ypos + ydelta][xpos + xdelta] == 7

    def path_to(self, start, goal):
        return self.pathfinding.find_path(start, goal)
