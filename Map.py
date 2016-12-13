import random
import networkx as nx


class Room(object):
    """Holds the coordinates of the room object including the center.
    Used later to determine intersections.
    """
    # Grid coords for each corner of the rooms
    x1 = None
    x2 = None
    y1 = None
    y2 = None
    # Width and Heighth
    width = None
    height = None
    # Center of the room
    center = None

    def new(self, x, y, w, h):
        self.x1 = x
        self.x2 = x + w
        self.y1 = y
        self.y2 = y + h
        self.width = w
        self.height = h
        self.center = ((self.x1 + self.x2) // 2, (self.y1 + self.y2) // 2)

    def intersects(self, other_room):
        return (self.x1 <= other_room.x2 & self.x2 >= other_room.x1 &
                self.y1 <= other_room.y2 & self.y2 >= other_room.y1)


class Hallway(object):

    x1 = None
    x2 = None
    y1 = None
    y2 = None

    def new(self, x1, x2, y1, y2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2


class Map(object):
    """This class makes the map.
       X and Y variables are the map size
       Desired rooms limits final room count
       room_list holds each room
    """
    room_list = []
    x = 60
    y = 60
    room_count = 0
    desired_rooms = 30
    room_min_size = 3
    room_max_size = 12

    def create_map(self):
        self.place_rooms
        self.make_graph
        self.place_halls

    def place_rooms(self):

        for i in range(0, self.desired_rooms):
            # Get wdith, height, x and y of potential new room
            w = self.room_min_size + random(self.room_max_size -
                                            self.room_min_size + 1)
            h = self.room_min_size + random(self.room_max_size -
                                            self.room_min_size + 1)
            x = random(self.x - w - 1) + 1
            y = random(self.y - h - 1) + 1

            newroom = Room.new(x, y, w, h)
            failed = False
            for other in self.room_list:
                # Loop through room list and check for intersections
                if newroom.intersects(other):
                    failed = True
                    break
            if not failed:
                # Adds newly made room to the room list
                self.room_list.add(newroom)

    def place_halls(self):
        connections = self.make_graph()
        pass

    def make_graph(self):
        """This puts out our graph to be used in the carve_hallways function.
           First it loops through our room_list dictionary and adds each edge,
           using the distance (pythag's theorem) as the weight.
           Then the Networkx black magic outputs a minimum spanning tree
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
        return mst
