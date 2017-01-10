import networkx as nx


class Creature(object):

    def __init__(self):
        self.pathfinding = Pathfinding(current_map.final_map)
        self.xpos = 0
        self.ypos = 0

    def set_pos(self, (x, y)):
        self.xpos = x
        self.ypos = y

    def move(self, (x, y)):
        # if self.check_intersect(self.xpos, self.ypos, x, y):
        self.xpos += x
        self.ypos += y
        print self.xpos, self.ypos

    def check_intersect(self, xpos, ypos, xdelta, ydelta):
        return not self.current_map.final_map[ypos + ydelta][xpos + xdelta] == 7

    def path_to(self, start, goal):
        return self.pathfinding.find_path(start, goal)


class Pathfinding:

    def __init__(self, current_map):
        self.adjacents = ((-1, 0), (1, 0), (0, -1), (0, 1))
        self.graph = self.make_graph(current_map)

    def make_graph(self, current_map):
        g = nx.Graph()
        for y in range(0, len(current_map)):
            for x in range(0, len(current_map[0])):
                if (current_map[y][x] == 4 or current_map[y][x] == 3):
                    cell = (x, y)
                    neighbors = []
                    # If it's not a wall, add it to the list of neighbors
                    try:
                        neighbors = [(x + j, y + j) for (i, j) in self.adjacents if
                                     (current_map[y + j][x + i] == 4 or
                                      current_map[y + j][x + i] == 3)]
                    except IndexError:
                        continue
                    for room in neighbors:
                        g.add_edge(cell, room, {'weight': 1})
        return g

    def find_path(self, start, goal):
        try:
            return nx.astar_path(self.graph, start, goal, self.dist)
        except Exception:
            return None

    def dist(self, a, b):
        (x1, y1) = a
        (x2, y2) = b
        return (((x1 - x2) ** 2) + ((y1 - y2) ** 2) ** 0.5)
