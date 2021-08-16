class Pixel:
    def __init__(self, coord: tuple, color: str):
        self.y, self.x = coord
        self.color = color

    def get_coord(self) -> tuple:
        return self.x, self.y

    def get_color(self) -> str:
        return self.color

    def move(self, new_coord: tuple):
        self.x, self.y = new_coord
