import random
from Creature import Creature
from Player import Player
from Map import Map


class DungeonMaster(object):

    p_input = {
        K_UP: self.player.move((0, -1)),
        K_DOWN: self.player.move((0, 1)),
        K_LEFT: self.player.move((-1, 0)),
        K_RIGHT: self.player.move((1, 0))
    }

    def __init__(self, screen):
        self.screen = screen
        self.floors = {}
        self.pathfinding = Pathfinding()
        self.player = Player()

    def update(self):
        """
        Update the DM:
            Take player input
            For each creature, do AI call
                Pathfinding will happen at top level to aid with creature coordination
                and reduce graph recreation. Store graph with level for re-use
            Update the screen with creature AI and player movement

        """
        for event in pygame.event.get():
            self.pressed = pygame.key.get_pressed()
            if self.pressed in self.p_input.keys():
                self.p_input.get(self.pressed)
            elif self.pressed[K_ESCAPE] or event.type == pygame.QUIT:
                sys.exit(0)
            else:
                continue

        for creature in self.creatures:
            creature.update()
        self.screen.update(self.current_floor, self.player, self.creatures)

    def generate_creature(self,):
        pass

    def generate_level(self, n):
        self.floors[n] = (Map(10, 15, 0))


class Pathfinding:

    def __init__(self):
        self.adjacents = ((-1, 0), (1, 0), (0, -1), (0, 1))

    def start(self, current_floor):
        self.current_floor = current_floor
        self.graph = make_graph(current_floor)

    def make_graph(self, current_floor):
        g = nx.Graph()
        for y in range(0, len(current_floor)):
            for x in range(0, len(current_floor[0])):
                if (current_floor[y][x] == 4 or current_floor[y][x] == 3):
                    cell = (x, y)
                    neighbors = []
                    # If it's not a wall, add it to the list of neighbors
                    try:
                        neighbors = [(x + j, y + j) for (i, j) in self.adjacents if
                                     (current_floor[y + j][x + i] == 4 or
                                      current_floor[y + j][x + i] == 3)]
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
