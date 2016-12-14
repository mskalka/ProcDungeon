import random
import networkx as nx


class Map(object):

    """This class makes the map.
       X and Y variables are the map size
       Desired rooms limits final room count
       room_list holds each room
    """

    def __init__(self, x, y, desired_rooms, rmin, rmax):
        self.room_list = []
        self.hall_list = []
        self.map_abstract = []
        self.revealed_map = []
        self.x = x
        self.y = y
        self.desired_rooms = desired_rooms
        self.room_min_size = rmin
        self.room_max_size = rmax
        self.room_count = 0
        self.generate_map()

    def generate_map(self):
        # Create blank map
        for i in range(self.y):
            self.map_abstract.append([])
            self.revealed_map.append([])
            for j in range(self.x):
                self.map_abstract[i].append(7)
                self.revealed_map[i].append(0)
        # Generate list of rooms and halls to add to map
        self.place_rooms()
        self.place_halls_2()
        for hall in self.hall_list:
            hall.hprint()
        # Add rooms and halls to map
        self.carve_rooms_and_halls()
        for i in self.map_abstract:
            print(i)

    def place_rooms(self):

        while self.room_count < self.desired_rooms:
            # Get wdith, height, x and y of potential new room
            w = self.room_min_size + random.randint(0, self.room_max_size -
                                                    self.room_min_size)
            h = self.room_min_size + random.randint(0, self.room_max_size -
                                                    self.room_min_size)
            x = random.randint(1, self.x - w - 2) + 1
            y = random.randint(1, self.y - h - 3) + 1

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

    def place_halls_2(self):
        """Different hall generation method. First we create a dict of all the
        rooms, key being the room and val being number of connections.
        Next iterate through the roomlist and check for close neighbors.
        If a neighbor is found and the room doesn't have too many connections,
        carve a halway to the neighbor. When it has too many connections,
        pop it from the dictionary and move on.
        Probable point of failure: Room has no reasonably close neighbors.
        Possible solution: Check if any rooms have value of 0, then connect
        them to a room in a larger range regardless of connections.
        """
        room_list_dict = {}
        for i in range(len(self.room_list)):
            room_list_dict[self.room_list[i]] = 0

        for room in self.room_list:
            x1 = room.center[0]
            y1 = room.center[1]
            for room2, c in room_list_dict.items():
                x2 = room2.center[0]
                y2 = room2.center[1]
                if abs(x1 - x2) <= 8 and abs(y1 - y2) <= 8 and c <= 2:
                    if random.randint(0, 1) == 1:
                        self.hcorridor(x1, x2, y1)
                        self.vcorridor(y1, y2, x2)
                    else:
                        self.vcorridor(y1, y2, x1)
                        self.hcorridor(x1, x2, y2)
                    room_list_dict[room2] += 1

        for room, c in room_list_dict.items():
            if c == 0:  # Check if any room has no connections
                x1 = room.center[0]
                y1 = room.center[0]
                for room2 in self.room_list:
                    x2 = room2.center[0]
                    y2 = room2.center[1]
                    # Recheck distance, ignore max connections
                    if abs(x1 - x2) <= 16 and abs(y1 - y2) <= 16:
                        if random.randint(0, 1) == 1:
                            self.hcorridor(x1, x2, y1)
                            self.vcorridor(y1, y2, x2)
                        else:
                            self.vcorridor(y1, y2, x1)
                            self.hcorridor(x1, x2, y2)

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
                               room_1_center[0])
                self.hcorridor(room_1_center[0], room_2_center[0],
                               room_2_center[1])

    def hcorridor(self, x1, x2, y):
        self.hall_list.append(Hallway(min(x1, x2), y, max(x1, x2), y))

    def vcorridor(self, y1, y2, x):
        self.hall_list.append(Hallway(x, min(y1, y2), x, max(y1, y2)))

    def carve_rooms_and_halls(self):
        for room in self.room_list:
            for y in range(room.y1, room.y2):
                for x in range(room.x1, room.x2):
                    self.map_abstract[y][x] = 4

        for hall in self.hall_list:
            for y in range(hall.y1, hall.y2 + 1):
                for x in range(hall.x1, hall.x2 + 1):
                    self.map_abstract[y][x] = 4


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
        h_over = (self.x1 - 1 <= other_room.x2) and (self.x2 >= other_room.x1)
        v_over = (self.y1 - 1 <= other_room.y2) and (self.y2 >= other_room.y1)

        return h_over and v_over


class Hallway(object):

    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2

    def hprint(self):
        print("x1, x2: {}, {} /n y1, y2: {}, {}".format(self.x1, self.x2,
                                                        self.y1, self.y2))
