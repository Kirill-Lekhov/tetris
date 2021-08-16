from pygame import Color
from Game_Parts import Board


class ShowNextShape(Board):
    def __init__(self, top, left, shape_pixels, shape_color):
        super().__init__()

        self.cell_size = 25
        self.board_size = 4, 4  # width, height
        self.top, self.left = top, left

        self.update(shape_pixels, shape_color)

    def render(self, surface, draw_red_borders: bool = True):
        super().render(surface, False)

    def update(self, shape_pixels, shape_color):
        self.create_board()
        self.add_shape_pixels_to_board(shape_pixels, shape_color)

    def add_shape_pixels_to_board(self, shape_pixels, shape_color):
        for pixel_coord in shape_pixels:
            self.board[pixel_coord[1]][pixel_coord[0] - 3] = (1, Color(shape_color))
