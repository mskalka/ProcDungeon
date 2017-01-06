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
                h += (rect // 2)
            else:
                w += (rect // 2)
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
            room.move_room((self.radius + 9, self.radius + 9))
            x_max = max(max(room.x1, room.x2), x_max)
            y_max = max(max(room.y1, room.y2), y_max)

        cells = [Cell((x, y)) for x in range(x_max + 15) for y in range(y_max + 15)]
        r = max(x_max, y_max)

        for c in cells:
            (x, y) = c.center
            dist = math.sqrt((x - ((x_max + 8) / 2)) ** 2 + (y - ((y_max + 8) / 2)) ** 2)
            if dist <= self.radius + 6:
                c.tile = 0
            else:
                c.tile = 99
            self.map_abstract[(x, y)] = c

        for room in self.room_list:
            room.carve_room(self.map_abstract)

    def add_halls(self):
        # Add each cell into a list of unvisited cells, remove when visited
        cells = []
        regions = {}
        region_id = 0
        for _, cell in self.map_abstract.iteritems():
            # Add only cells where there isn't a floor already
            if cell.tile == 0:
                cells.append(cell)

        """
        Every time a cell is added to a region it's popped from the cell list
        so while the list of cells is greater than 0, repeat the maze generation.
        This ensures that even if a cell is unreachable by the first iteration
        of the generator, it will have a maze greated for it.
        """

        while len(cells) > 0:
            regions[region_id] = self.generate_maze(region_id, cells)

        """
        After maze generation , ensure that the room is connected to each
        region it abuts. First find candidate doors, then pick 1-3 at random,
        add a door between those two tiles using connect_cells
        """

        for room in self.room_list:
            x1 = room.x1
            x2 = room.x2
            y1 = room.y1
            y2 = room.y2
            neighbors = {}
            potential_joins = []
            final_joins = []
            # Loop through each outer edge of the map,
            # see which cells it abuts orthogonally from each region
            for x in range(x1, x2):                  # Cells above & below
                potential_joins.append((self.map_abstract[(x, y1)],
                                        self.map_abstract[(x, y1 + 1)]))
                potential_joins.append((self.map_abstract[(x, y2)],
                                        self.map_abstract[(x, y2 - 1)]))
            for y in range(y1, y2):                  # Cells left & right
                potential_joins.append((self.map_abstract[(x1, y)],
                                        self.map_abstract[(x1 - 1, y)]))
                potential_joins.append((self.map_abstract[(x2, y)],
                                        self.map_abstract[(x2 + 1, y)]))


            for region, cells in regions.iteritems():
                neighbors[region] = []
                for (r_cell, l_cell) in potential_joins:
                    if l_cell in cells:
                        neighbors[region].append((r_cell, l_cell))
                n = random.randint(1, min(len(neighbors[region]), 3))
                final_joins.extend(random.sample(neighbors[region], n))

            # Connect each cell with it's partner and set the door flag to true
            for (r_cell, l_cell) in final_joins:
                r_cell.add_connection(l_cell, door=True)

    def generate_maze(self, region_id, cells):
        """
        Use a recursive backtracking alg to fill the space between the rooms with
        a maze.
        """
        path = []
        path.append(random.choice(cells))
        region = []
        while len(path) > 0:
            moved = False
            current = path[-1]
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            random.shuffle(directions)

            if current not in region:
                region.append(current)

            for direction in directions:
                next_target = map(sum, zip(current.center,
                                           direction))
                next_target = (next_target[0], next_target[1])
                try:
                    next_cell = self.map_abstract[next_target]
                except KeyError:
                    continue
                if next_cell in cells:
                    next_cell.tile = 7
                    path.append(next_cell)
                    current.add_connection(next_cell)
                    cells.remove(next_cell)
                    moved = True
                    break
                else:
                    continue
            if not moved:
                popped = path.pop()
                continue

        region_id += 1
        return region

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
        self.doors = []

    def add_connection(self, other_cell, door=False):
        self.connections.append(other_cell)
        if door:
            self.doors.append(other_cell)


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
        h_over = (self.x1 <= other_room.x2) and (self.x2 >= other_room.x1)
        v_over = (self.y1 <= other_room.y2) and (self.y2 >= other_room.y1)

        return h_over and v_over

    def carve_room(self, map_abstract):
        cells = []
        for x in range(self.x1, self.x2):
            for y in range(self.y1, self.y2):
                cells.append(map_abstract[(x, y)])
                map_abstract[(x, y)].tile = 4
        for cell in cells:
            for other_cell in cells:
                if cell != other_cell:
                    cell.add_connection(other_cell)

    def move_room(self, (dx, dy)):
        # Offset all the room's positional values by dx, dy
        self.center = (self.center[0] + dx, self.center[1] + dy)
        self.x1 += dx
        self.y1 += dy
        self.x2 += dx
        self.y2 += dy
