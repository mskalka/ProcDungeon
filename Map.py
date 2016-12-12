import random, networkx as nx

class Map(object):
    """This class makes the map!
       X and Y variables are the map size
       Desired rooms limits final room count
       map and roomlist just to initialize the variables for later use
       map holds the final map
       roomlist holds a record of each room for later use in the MST calculation 
    """
    map = []
    visiblemap = []
    x = 60
    y = 60
    roomcount = 0
    desiredrooms = 40
    roomlist = {}
    
    def blank_map(self):    
        for i in range(self.y):
            self.map.append([])     #Create a blank map of dimensions
            self.visiblemap.append([])
            for j in range (self.x):# X and Y, fill with placeholders
                self.map[i].append('.')
                self.visiblemap[i].append(0)
            
    def add_rooms(self):
        """Adds rooms to our blank map, deonted by '0's.
           First generates a random room by size and location,
           then checks to see if that space is occupied. If it's not,
           then it adds the room to that location. If it is, then it just
           repeats with another room until the roomcount is reached.
            
           It's a little slow at this point, when I figure out how to speed 
           the map generation up I can optimize it further. Works well enough
           at this point if you don't try to make the desiredrooms variable 
           too high compaired to the map size 
        """
        while self.roomcount < self.desiredrooms:
            occupied = False
            xdim = random.randint(4,7) #Set horz size
            ydim = random.randint(4,7) #Set vert size
            xloc = random.randint(1,self.x - xdim - 3) #Set the location, within bounds of map
            yloc = random.randint(1,self.y - ydim - 3) #Keeps the room away from the edges
            for i in range(yloc - 1, yloc + ydim + 1):
                for j in range(xloc - 1, xloc + xdim + 1): #Check to see if the area is occuped
                    if self.map[i][j] == '0':
                        occupied = True
                        
            if not occupied:
                for i in range(yloc, yloc + ydim):
                    for j in range(xloc, xloc + xdim):  #Puts a room there if it's not occupied
                        self.map[i][j] = '0'            #Use '0' for the basic floor tile
                        if ydim % 2 == 0:
                            ypos = yloc + ydim/2
                        else:
                            ypos = yloc + (ydim + 1)/2
                        if xdim % 2 == 0:
                            xpos = xloc + xdim/2
                        else:
                            xpos = xloc + (xdim + 1)/2
                self.roomlist[self.roomcount] = ypos,xpos,ydim,xdim
                self.roomcount += 1    
        
        
    def make_graph(self):
        """This puts out our graph to be used in the carve_hallways function.
           First it loops through our roomlist dictionary and adds each edge, 
           using the distance (pythag's theorem) as the weight.
           
           Tried to implement a little randomness to the weights, but even a
           4% variation made some really wonky stuff happen.
           
           Then the Networkx black magic outputs a minimum spanning tree 
        """
        G = nx.Graph()
        for i in range(len(self.roomlist)):
            for j in range(len(self.roomlist)):
                length = {'weight' : ((((self.roomlist[i][0] - self.roomlist[j][0]) ** 2) + ((self.roomlist[i][1] - self.roomlist[j][1]) ** 2)) ** 0.5)}
                G.add_edge(i, j, length)
        mst = nx.minimum_spanning_tree(G)
        return mst
    
    def carve_hallways(self):
        """Uses the minimum spanning tree graph from make_graph to connect each room.
           Loops through each edge listed in the graph, then from that edge pulls the
           connecting rooms from roomlist and pulls its Y and X coords out of the list.
           After that it simply loops down placing '1' tiles in the Y then X direction
           until each edge is connected.
        """
        hallwaylist = self.make_graph().edges()
        for r in hallwaylist:
            room1 = r[0]
            room2 = r[1]
            cy1 = self.roomlist[room1][0] - 1 # y value from cord1
            cy2 = self.roomlist[room2][0] - 1 # y value from cord2
            cx1 = self.roomlist[room1][1] - 1 # x value from cord1
            cx2 = self.roomlist[room2][1] - 1 # x value from cord2
            
            if cy1 - cy2 < 0:
                for i in range(cy1,cy2 + 1):
                    if not self.map[i][cx1] == '0':
                        self.map[i][cx1] = '1'
                
            elif cy1 - cy2 > 0:
                for i in range(cy2,cy1 + 1):
                    if not self.map[i][cx1] == '0':
                        self.map[i][cx1] = '1'
                
                
            if cx1 - cx2 < 0:
                for i in range(cx1,cx2 + 1):
                    if not self.map[cy2][i] == '0':
                        self.map[cy2][i] = '1'  
                
            elif cx1 - cx2 > 0:
                for i in range(cx2,cx1 + 1):
                    if not self.map[cy2][i] == '0':
                        self.map[cy2][i] = '1'
                        
    def add_doors(self):
        """This function adds doors in the hallways made by carve_hallways.
           Checks each '1' tile on the map, and depending on what's around it,
           places a '2' tile (denoting a door) in it's place.
        """
        for i in range(self.y):
            for j in range(self.x):
                if self.map[i][j] == '1' and (self.map[i][j-1] == '0' and self.map[i][j+1] == '0') and not (self.map[i-1][j] == '1' or self.map[i+1][j] == '1'):
                    self.map[i][j] = '2'
                elif self.map[i][j] == '1' and (self.map[i-1][j] == '0' and self.map[i+1][j] == '0') and not (self.map[i][j-1] == '1' or self.map[i][j+1] == '1'):
                    self.map[i][j] = '2'              
                elif self.map[i][j] == '1' and self.map[i-1][j] == '0' and self.map[i+1][j] == '1'and not (self.map[i][j-1] == '1' or self.map[i][j+1] == '1'):
                    self.map[i][j] = '2'
                elif self.map[i][j] == '1' and self.map[i][j-1] == '0' and self.map[i][j+1] == '1'and not (self.map[i-1][j] == '1' or self.map[i+1][j] == '1'):
                    self.map[i][j] = '2'
                elif self.map[i][j] == '1' and self.map[i+1][j] == '0' and self.map[i-1][j] == '1'and not (self.map[i][j-1] == '1' or self.map[i][j+1] == '1'):
                    self.map[i][j] = '2'
                elif self.map[i][j] == '1' and self.map[i][j+1] == '0' and self.map[i][j-1] == '1'and not (self.map[i-1][j] == '1' or self.map[i+1][j] == '1'):
                    self.map[i][j] = '2'
    
    def randomize_floors_and_walls(self):
        for i in range(self.y):
            for j in range(self.x):
                if self.map[i][j] == '.':
                    rand = random.randint(7,9)
                    self.map[i][j] = str(rand)
                if self.map[i][j] == '1' or self.map[i][j] == '0':
                    rand = random.randint(4,6)
                    self.map[i][j] = str(rand)
                    
    def generate_map(self):
        self.blank_map()
        self.add_rooms()
        self.carve_hallways()
        self.add_doors()
        self.randomize_floors_and_walls()    
                
    def print_map(self):
        for row in self.map:
            print row