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
        self.pathfinding.find_path(start, goal)

class Pathfinding:

    def __init__(self, current_map):
        self.adjacents = ((-1, 0), (1, 0), (0, -1), (0, 1))
        self.graph = self.make_graph(current_map)

    def make_graph(self, current_map):
        g = nx.Graph()
        for i in range(0, len(current_map)):
            for j in range(0, len(current_map)):
                cell = (i, j)
                neighbors = []
                # If it's not a wall, add it to the list of neighbors
                try:
                    neighbors = [(i + y, j + x) for (x, y) in self.adjacents if current_map[i + y][j + x] == 4]
                except IndexError:
                    continue
                for room in neighbors:
                    g.add_edge(cell, room, {'weight': 1})
        return g

    def find_path(self, start, goal):
        p = (nx.astar_path(self.graph, start, goal, self.dist))
        print(p)
        return p

    def dist(self, a, b):
        (x1, y1) = a
        (x2, y2) = b
        return (((x1 - x2) ** 2) + ((y1 - y2) ** 2) ** 0.5)



'''
class Graph:

    def __init__(self, current_map):
        self.adjacents = ((-1, 0), (1, 0), (0, -1), (0, 1))
        self.current_map = current_map
        self.graph = {}
        self.make_graph(self.current_map)


    def make_graph(self, current_map):
        for i in range(0, len(current_map)):
            for j in range(0, len(current_map)):
                cell = (i, j)
                # If it's not a wall, add it to the list of neighbors
                try:
                    neighbors = [(i + y, j + x) for (x, y) in self.adjacents if current_map[i + y][j + x] == 4]
                except IndexError:
                    continue
                else:
                    self.graph[cell] = neighbors
        print(self.graph)

    def neighbors(self, cell):
        return self.graph[cell]

    def cost(self, cell, to_cell):
        return 1


class PriorityQueue:

    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]


class A_star:

    def __init__(self, current_map):
        self.current_map = current_map
        self.graph = Graph(self.current_map)
        self.priority = PriorityQueue()

    def get_path(self, start, goal):
        p = self.a_star_search(self.graph.graph, start, goal)
        print(p)

    def heuristic(self, a, b):
        (x1, y1) = a
        (x2, y2) = b
        return abs(x1 - x2) + abs(y1 - y2)

    def a_star_search(self, graph, start, goal):
        frontier = self.priority
        frontier.put(start, 0)
        came_from = {}
        cost_so_far = {}
        came_from[start] = None
        cost_so_far[start] = 0

        while not frontier.empty():
            current = frontier.get()
            if current == goal:
                break
            for next in self.graph.neighbors(current):
                new_cost = cost_so_far[current] + self.graph.cost(current, next)
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + self.heuristic(goal, next)
                    frontier.put(next, priority)
                    came_from[next] = current

        return came_from, cost_so_far

    '''
