from Map import Map
import networkx as nx


class Creature(object):

    def __init__(self, current_map):
        self.current_map = current_map
        self.pathfinding = Pathfinding(current_map)

    def get_pos(self):
        return self.xpos, self.ypos

    def set_pos(self, x, y):
        self.xpos = x
        self.ypos = y

    def move(self, x, y):
        if self.check_intersect(self.xpos, self.ypos, x, y):
            self.xpos += x
            self.ypos += y

    def check_intersect(self, xpos, ypos, xdelta, ydelta):
        return not Map.map_abstract[ypos + ydelta][xpos + xdelta] == 7

    def path_to(self, start, goal):
        return self.pathfinding.find_path(start, goal)


class Pathfinding:

    def __init__(self, current_map):
        self.adjacents = ((-1, 0), (1, 0), (0, -1), (0, 1))
        self.graph = self.make_graph(current_map)

    def make_graph(self, current_map):
        g = nx.Graph()
        for i in range(0, len(current_map)):
            for j in range(0, len(current_map)):
                if current_map[i][j] != 7:
                    cell = (j, i)
                    neighbors = []
                    # If it's not a wall, add it to the list of neighbors
                    try:
                        neighbors = [(j + x, i + y) for (x, y) in self.adjacents if
                                     current_map[i + y][j + x] == 4]
                    except IndexError:
                        continue
                    for room in neighbors:
                        g.add_edge(cell, room, {'weight': 1})
        return g

    def find_path(self, start, goal):
        try:
            return nx.astar_path(self.graph, start, goal, self.dist)
        except Exception:
            print "I failed to find a path!"

    def dist(self, a, b):
        (x1, y1) = a
        (x2, y2) = b
        return (((x1 - x2) ** 2) + ((y1 - y2) ** 2) ** 0.5)
