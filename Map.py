import random
import math
import networkx as nx


class Map(object):

    """
    This class makes the map.
    Each map is roughly round, with a radius set in initial map generation
    Desired rooms limits final room count
    room_list holds each room

    Each entry in the abstract map represents each "cell",
    a 3x3 grid of room tiles.


    Floor is represented by a 4, walls 7, halls 6, raw area as 0.

    """

    def __init__(self, radius, desired_rooms, fuzz):
        self.room_list = []
        self.hall_list = []
        self.map_abstract = {}
        self.revealed_map = []
        self.radius = radius
        self.desired_rooms = desired_rooms
        self.room_fuzz = fuzz
        self.room_count = 0
        self.generate_map()

    def generate_map(self):
        self.place_rooms()
        self.add_halls()

    def place_rooms(self):
        while self.room_count < self.desired_rooms:
            # Each room gets its own unique region ID, to be used in hall placement

            # Create a room with a random, odd width and height
            size = (random.randint(2, 3 + self.room_fuzz))
            rect = random.randint(0, 1 + size)
            w = size
            h = size
            if bool(random.getrandbits(1)):
                w += rect
                h += (rect // 2) * 2
            else:
                w += (rect // 2) * 2
                h += rect

            # Places the room on a point within the circle of supplied radius
            point = self.get_random_point(self.radius)
            new_room = Room((point[0], point[1]),
                            w, h)
            failed = False
            for other in self.room_list:
                # Loop through room list and check for intersections
                if new_room.intersects(other):
                    failed = True
                    break
            if not failed:
                # Adds newly made room to the room list
                self.room_list.append(new_room)
                self.room_count += 1

        x_max = 0
        y_max = 0
        # Offset the rooms by the radius to move the center from (0, 0) to
        # (r, r) which puts the bottom left room close enough to (0, 0)
        for room in self.room_list:
            room.move_room((self.radius + 10, self.radius + 10))
            x_max = max(max(room.x1, room.x2), x_max)
            y_max = max(max(room.y1, room.y2), y_max)

        cells = [Cell((x, y)) for x in range(x_max + 15) for y in range(y_max + 15)]
        r = max(x_max, y_max)

        for c in cells:
            (x, y) = c.center
            dist = math.sqrt((x - ((x_max + 8) / 2)) ** 2 + (y - ((y_max + 8) / 2)) ** 2)
            if dist <= self.radius + 4:
                c.tile = 0
            else:
                c.tile = 99
            self.map_abstract[(x, y)] = c

        for room in self.room_list:
            room.carve_room(self.map_abstract)

    def add_halls(self):
        """
        Use a recursive backtracking alg to fill the space between the rooms with
        a maze.
        """
        # Add each cell into a dict of unvisited cells, value represents unvisited
        cells = {}
        for _, cell in self.map_abstract.iteritems():
            # Add only cells where there isn't a floor already
            if cell.tile == 0:
                # Bool for unvisited
                cells[cell] = True
        print cells
        path = []
        path.extend(random.sample(cells, 1))
        print path
        while len(path) > 0:
            moved = False
            current = path[-1]
            print path
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            random.shuffle(directions)
            # cells[current] = False
            for direction in directions:
                next_target = map(sum, zip(current.center,
                                           direction))
                next_target = (next_target[0], next_target[1])
                try:
                    next_cell = cells[self.map_abstract[next_target]]
                except KeyError:
                    continue
                if next_cell:
                    path.append(self.map_abstract[next_target])
                    moved = True
                    current.add_connection(self.map_abstract[next_target])
                    cells[self.map_abstract[next_target]] = False
                    break
                else:
                    continue
            if not moved:
                popped = path.pop()
                continue

    def get_random_point(self, radius):
        t = 2 * math.pi * random.random()
        u = random.random() + random.random()
        r = None
        if u > 1:
            r = 2 - u
        else:
            r = u

        point = (self.roundm(radius * r * math.cos(t), 1),
                 self.roundm(radius * r * math.sin(t), 1))

        return point

    def roundm(self, n, m):
        return int(n // m)


class Cell(object):

    def __init__(self, (x, y)):
        self.center = (x, y)
        self.tile = 0
        self.connections = []

    def __hash__(self):
        return hash(self.center)

    def __eq__(self, other):
        return self.center == other.center

    def __ne__(self, other):
        # Not strictly necessary, but to avoid having both x==y and x!=y
        # True at the same time
        return not(self == other)

    def add_connection(self, other_cell):
        self.connections.append(other_cell)


class Room(object):

    def __init__(self, center, w, h):
        self.center = center
        self.width = w
        self.height = h
        self.x1 = center[0] - w // 2
        self.x2 = center[0] + 1 + w // 2
        self.y1 = center[1] - h // 2
        self.y2 = center[1] + 1 + h // 2

    def intersects(self, other_room):
        h_over = (self.x1 < other_room.x2) and (self.x2 > other_room.x1)
        v_over = (self.y1 < other_room.y2) and (self.y2 > other_room.y1)

        return h_over and v_over

    def carve_room(self, map_abstract):
        for x in range(self.x1, self.x2):
            for y in range(self.y1, self.y2):
                map_abstract[(x, y)].tile = 4

    def move_room(self, (dx, dy)):
        # Offset all the room's positional values by dx, dy
        self.center = (self.center[0] + dx, self.center[1] + dy)
        self.x1 += dx
        self.y1 += dy
        self.x2 += dx
        self.y2 += dy
