import random
import math
import networkx as nx


class Map(object):

    """This class makes the map.
       X and Y variables are the map size
       Desired rooms limits final room count
       room_list holds each room
    """

    def __init__(self, radius, desired_rooms, fuzz):
        self.room_list = []
        self.hall_list = []
        self.map_abstract = []
        self.revealed_map = []
        self.radius = radius
        self.desired_rooms = desired_rooms
        self.room_fuzz = fuzz
        self.room_count = 0
        self.generate_map()

    def generate_map(self):
        self.place_rooms()

    def place_rooms(self):
        while self.room_count < self.desired_rooms:
            # Create a room with a random, odd width and height
            size = random.randint(2, 3 + self.room_fuzz) * 2 + 1
            rect = random.randint(0, 1 + size // 2) * 2
            w = size
            h = size
            if bool(random.getrandbits(1)):
                w += rect
            else:
                h += rect

            # Places the room on a point within the circle of supplied radius
            point = self.get_random_point(self.radius)
            new_room = Room((point[0]//2) * 2 + 1, (point[1]//2) * 2 + 1, w, h)
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
        # Then set the max size of the map for hall generation
        for room in self.room_list:
            room.move_room((self.radius, self.radius))
            x_max = max(room.x2, x_max)
            y_max = max(room.y2, y_max)
        # Finally generate a map abstract to hold a list of cells for maze generation
        self.map_abstract = [[0 for i in range(x_max + 1)] for j in range(y_max + 1)]
        # Carve each room into the map abstract
        for room in self.room_list:
            room.carve_room(self.map_abstract)

    def add_halls(self):
        pass

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


class Room(object):

    def __init__(self, x, y, w, h):
        self.x1 = x
        self.x2 = x + w
        self.y1 = y
        self.y2 = y + h
        self.width = w
        self.height = h
        self.center = ((self.x1 + self.x2) // 2, (self.y1 + self.y2) // 2)

    def intersects(self, other_room):
        h_over = (self.x1 <= other_room.x2) and (self.x2 >= other_room.x1)
        v_over = (self.y1 <= other_room.y2) and (self.y2 >= other_room.y1)

        return h_over and v_over

    def carve_room(self, map_abstract):
        for y in range(self.y1, self.y2):
            for x in range(self.x1, self.x2):
                map_abstract[y][x] = 7

    def move_room(self, (dx, dy)):
        # Offset all the room's positional values by dx, dy
        self.center = (self.center[0] + dx, self.center[1] + dy)
        self.x1 += dx
        self.y1 += dy
        self.x2 += dx
        self.y2 += dy
