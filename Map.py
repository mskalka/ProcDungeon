import random
import networkx as nx


class Map(object):
    """This class makes the map.
       X and Y variables are the map size
       Desired rooms limits final room count
       room_list holds each room
    """
    room_list = []
    hall_list = []
    map_abstract = []
    x = 50
    y = 50
    room_count = 0
    desired_rooms = 40
    room_min_size = 3
    room_max_size = 7

    def generate_map(self):
        # Create blank map
        for i in range(0, self.x + 1):
            self.map_abstract.append([])
            for j in range(0, self.y + 1):
                self.map_abstract[i].append(7)
        # Generate list of rooms and halls to add to map
        self.place_rooms()
        self.place_halls()
        for hall in self.hall_list:
            hall.hprint()
        # Add rooms and halls to map
        self.carve_rooms_and_halls()
        for i in self.map_abstract:
            print(i)

    def place_rooms(self):
        """
        """
        while self.room_count < self.desired_rooms:
            # Get wdith, height, x and y of potential new room
            w = self.room_min_size + random.randint(0, self.room_max_size -
                                                    self.room_min_size)
            h = self.room_min_size + random.randint(0, self.room_max_size -
                                                    self.room_min_size)
            x = random.randint(1, self.x - w - 1) + 1
            y = random.randint(1, self.y - h - 1) + 1

            newroom = Room(x, y, w, h)
            failed = False
            for other in self.room_list:
                # Loop through room list and check for intersections
                if newroom.intersects(other):
                    failed = True
                    break
            if not failed:
                # Adds newly made room to the room list
                self.room_list.append(newroom)
                self.room_count += 1

    def place_halls(self):
        """This puts out our graph to be used in the carve_hallways function.
           First it loops through our room_list dictionary and adds each edge,
           using the distance as the weight.
           Then the Networkx black magic outputs a minimum spanning tree using
           what's likely black magic.
        """
        G = nx.Graph()
        for room in self.room_list:
            for other_room in self.room_list:
                weight = {'weight': ((((room.center[0] -
                                        other_room.center[0]) ** 2)
                                     + ((other_room.center[1] -
                                         other_room.center[1]) ** 2)) ** 0.5)}
                G.add_edge(room, other_room, weight)
        mst = nx.minimum_spanning_tree(G)

        for hall in mst.edges():
            room_1_center = hall[0].center
            room_2_center = hall[1].center
            if random.randint(0, 1) == 1:
                self.hcorridor(room_1_center[0], room_2_center[0],
                               room_1_center[1])
                self.vcorridor(room_1_center[1], room_2_center[1],
                               room_2_center[0])
            else:
                self.vcorridor(room_1_center[1], room_2_center[1],
                               room_2_center[0])
                self.hcorridor(room_1_center[0], room_2_center[0],
                               room_1_center[1])

    def hcorridor(self, x1, x2, y):
        self.hall_list.append(Hallway(min(x1, x2), y, max(x1, x2), y))

    def vcorridor(self, y1, y2, x):
        self.hall_list.append(Hallway(x, min(y1, y2), x, max(y1, y2)))

    def carve_rooms_and_halls(self):
        for room in self.room_list:
            for x in range(room.x1, room.x2):
                for y in range(room.y1, room.y2):
                    self.map_abstract[x][y] = 4

        for hall in self.hall_list:
            for x in range(hall.x1, hall.x2 + 1):
                for y in range(hall.y1, hall.y2 + 1):
                    self.map_abstract[x][y] = 4


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


class Hallway(object):

    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2

    def hprint(self):
        print("x1, y1: {}, {} /n x2, y2: {}, {}".format(self.x1, self.y1,
                                                        self.x2, self.y2))
