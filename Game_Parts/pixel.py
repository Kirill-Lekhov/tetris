class Pixel:
    def __init__(self, coord: tuple, color):
        self.y, self.x = coord
        self.color = color

    def get_info(self) -> tuple:
        return (self.x, self.y), self.color

    def move(self, new_coord: tuple):
        self.x, self.y = new_coord
