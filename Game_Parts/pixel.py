class Pixel:
    def __init__(self, coord, color):
        self.x = coord[1]
        self.y = coord[0]
        self.color = color

    def get_info(self):
        return (self.x, self.y), self.color

    def move(self, new_coord):
        self.x = new_coord[0]
        self.y = new_coord[1]
