from pygame import draw, Color


class Board:
    def __init__(self):
        self.cell_size = 30
        self.border_width = 1
        self.board_size = 10, 21    # width, height
        self.top, self.left = 50, 50
        self.board = None

        self.create_board()
        self.create_stop_line()

    def render(self, surface, draw_red_borders: bool = True):
        self.draw_board(surface)

        if draw_red_borders:
            self.draw_red_borders(surface)

    def draw_board(self, surface):
        for i in range(self.board_size[1]):
            for k in range(self.board_size[0]):
                draw.rect(surface, (255, 255, 255), (self.left + k * self.cell_size,
                                                     self.top + i * self.cell_size,
                                                     self.cell_size,
                                                     self.cell_size))

                draw.rect(surface, self.board[i][k][1], (self.left + k * self.cell_size + 1,
                                                         self.top + i * self.cell_size + 1,
                                                         self.cell_size - self.border_width * 2,
                                                         self.cell_size - self.border_width * 2))

    def draw_red_borders(self, surface):
        for k in range(self.board_size[0]):
            draw.rect(surface, (255, 0, 0), (self.left + k * self.cell_size,
                                             self.top - 1 * self.cell_size,
                                             self.cell_size, self.cell_size))

            draw.rect(surface, (0, 0, 0), (self.left + k * self.cell_size + 1,
                                           self.top - 1 * self.cell_size + 1,
                                           self.cell_size - self.border_width * 2,
                                           self.cell_size - self.border_width * 2))

            draw.rect(surface, (255, 0, 0), (self.left + k * self.cell_size,
                                             self.top + 20 * self.cell_size,
                                             self.cell_size, self.cell_size))

            draw.rect(surface, (0, 0, 0), (self.left + k * self.cell_size + 1,
                                           self.top + 20 * self.cell_size + 1,
                                           self.cell_size - self.border_width * 2,
                                           self.cell_size - self.border_width * 2))

        for i in range(self.board_size[1]):
            draw.rect(surface, (255, 0, 0), (self.left - 1 * self.cell_size,
                                             self.top + i * self.cell_size,
                                             self.cell_size, self.cell_size))

            draw.rect(surface, (0, 0, 0), (self.left - 1 * self.cell_size + 1,
                                           self.top + i * self.cell_size + 1,
                                           self.cell_size - self.border_width * 2,
                                           self.cell_size - self.border_width * 2))

            draw.rect(surface, (255, 0, 0), (self.left + self.board_size[0] * self.cell_size,
                                             self.top + i * self.cell_size,
                                             self.cell_size,
                                             self.cell_size))

            draw.rect(surface, (0, 0, 0), (self.left + self.board_size[0] * self.cell_size + 1,
                                           self.top + i * self.cell_size + 1,
                                           self.cell_size - self.border_width * 2,
                                           self.cell_size - self.border_width * 2))

    def create_board(self):
        self.board = []

        for k in range(self.board_size[1]):
            line = []

            for i in range(self.board_size[0]):
                line.append((0, Color("black")))

            self.board.append(line[:])

    def create_stop_line(self):
        stop_line = []

        for i in range(self.board_size[0]):
            stop_line.append((1, Color('black')))

        self.board[-1] = stop_line[:]
