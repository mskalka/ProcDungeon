from Map import Map


class Camera(object):

    def __init__(self, current_map):
        self.current_map = current_map
        self.x_offset = 0
        self.y_offset = 0
