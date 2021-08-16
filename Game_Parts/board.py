from pygame import draw, Color


class Board:
    def __init__(self):
        self.cell_size = 30
        self.border_width = 1
        self.board_size = 10, 21    # width, height
        self.top, self.left = 50, 50
        self.board = None

        self.create_board()

    def render(self, surface, draw_red_borders: bool = True):
        self.draw_board(surface)

        if draw_red_borders:
            self.draw_red_borders(surface)

    def draw_board(self, surface):
        for i in range(self.board_size[1]):
            for k in range(self.board_size[0]):
                self.draw_cell(surface, self.left + k * self.cell_size, self.top + i * self.cell_size,
                               self.board[i][k][1], (255, 255, 255))

    def draw_red_borders(self, surface):
        border_color = (255, 0, 0)
        body_color = (0, 0, 0)

        for k in range(self.board_size[0]):
            self.draw_cell(surface, self.left + k * self.cell_size, self.top - 1 * self.cell_size,
                           body_color, border_color)
            self.draw_cell(surface, self.left + k * self.cell_size, self.top + (self.board_size[1]-1) * self.cell_size,
                           body_color, border_color)

        for i in range(self.board_size[1]):
            self.draw_cell(surface, self.left - 1 * self.cell_size, self.top + i * self.cell_size,
                           body_color, border_color)
            self.draw_cell(surface, self.left + self.board_size[0] * self.cell_size, self.top + i * self.cell_size,
                           body_color, border_color)

    def draw_cell(self, surface, x, y, color: tuple, border_color: tuple):
        cell_rect = (x, y, self.cell_size, self.cell_size)
        cell_body = (x + self.border_width, y + self.border_width,
                     self.cell_size - self.border_width * 2, self.cell_size - self.border_width * 2)

        draw.rect(surface, border_color, cell_rect)
        draw.rect(surface, color, cell_body)

    def create_board(self):
        self.board = []

        for k in range(self.board_size[1]):
            line = []

            for i in range(self.board_size[0]):
                line.append((int(k == self.board_size[1]-1), Color("black")))

            self.board.append(line[:])
