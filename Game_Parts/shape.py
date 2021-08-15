from random import choice

from constants import COLORS, TYPES
from Game_Parts.pixel import Pixel


class Shape:
    def __init__(self, shape_type):
        self.its_moving = True
        self.color = choice(COLORS)
        self.shape_type = shape_type
        self.attitude = choice(TYPES[self.shape_type])
        self.pixels_position = TYPES[self.shape_type].index(self.attitude)
        self.pixels = [Pixel(i, self.color) for i in self.attitude]

    def get_pixels(self):
        return self.pixels

    def get_color(self):
        return self.color

    def get_moving_status(self):
        return self.its_moving

    def get_shape_pixels_coord(self):
        return [i.get_coord() for i in self.pixels]

    def lower_it_down(self, board):
        self.can_it_go_down(board)

        if self.its_moving:
            for i in self.pixels:
                x, y = i.get_coord()
                i.move((x, y + 1))

    def can_it_go_down(self, board):
        if self.its_moving:
            for i in self.pixels:
                x, y = i.get_coord()

                if board[y + 1][x][0] == 1:
                    self.its_moving = False
                    break

    def move_to_side(self, board, direction=0):
        direction = self.can_it_move_to_side(board, direction)

        if direction != 0:
            for i in self.pixels:
                x, y = i.get_coord()
                i.move((x + direction, y))

    def can_it_move_to_side(self, board, direction) -> int:
        if direction == 1:
            for x, y in self.get_shape_pixels_coord():
                if x + 1 >= len(board[0]):
                    return 0

                if board[y][x+1][0] == 1:
                    return 0

        elif direction == -1:
            for x, y in self.get_shape_pixels_coord():
                if x - 1 < 0:
                    return 0

                if board[y][x-1][0] == 1:
                    return 0

        return direction

    def rotate(self, board):
        if not self.its_moving:
            return

        if self.shape_type == 'O':
            return

        elif self.shape_type == 'Z':
            center = self.pixels[2].get_coord()

            try:
                if center[0] - 1 < 0:
                    raise IndexError

                if self.pixels_position == 0:
                    if board[center[1] - 1][center[0] + 1][0] == 0 and board[center[1] + 1][center[0]][0] == 0:
                        self.pixels[0].move((center[0], center[1] + 1))
                        self.pixels[1].move((center[0] + 1, center[1] - 1))
                        self.pixels = [self.pixels[1], self.pixels[3], self.pixels[2], self.pixels[0]]
                        self.pixels_position = 1

                elif self.pixels_position == 1:
                    if board[center[1] - 1][center[0] - 1][0] == 0 and board[center[1] - 1][center[0]][0] == 0:
                        self.pixels[0].move((center[0], center[1] - 1))
                        self.pixels[3].move((center[0] - 1, center[1] - 1))
                        self.pixels = [self.pixels[3], self.pixels[0], self.pixels[2], self.pixels[1]]
                        self.pixels_position = 0

            except IndexError:
                return

        elif self.shape_type == 'S':
            center = self.pixels[1].get_coord()

            try:
                if center[0] - 1 < 0:
                    raise IndexError

                if self.pixels_position == 0:
                    if board[center[1] + 1][center[0] + 1][0] == 0 and board[center[1]][center[0] + 1][0] == 0:
                        self.pixels[0].move((center[0] + 1, center[1] + 1))
                        self.pixels[3].move((center[0] + 1, center[1]))
                        self.pixels = [self.pixels[2], self.pixels[1], self.pixels[3], self.pixels[0]]
                        self.pixels_position = 1

                elif self.pixels_position == 1:
                    if board[center[1] - 1][center[0] + 1][0] == 0 and board[center[1]][center[0] - 1][0] == 0:
                        self.pixels[2].move((center[0] - 1, center[1]))
                        self.pixels[3].move((center[0] + 1, center[1] - 1))
                        self.pixels = [self.pixels[2], self.pixels[1], self.pixels[0], self.pixels[3]]
                        self.pixels_position = 0

            except IndexError:
                return

        elif self.shape_type == 'I':
            try:
                center = self.pixels[1].get_coord()

                if center[0] - 1 < 0:
                    raise IndexError

                if self.pixels_position == 0:
                    if board[center[1] - 1][center[0]][0] == 0 and board[center[1] + 1][center[0]][0] == 0 \
                            and board[center[1] + 2][center[0]][0] == 0:
                        self.pixels[0].move((center[0], center[1] - 1))
                        self.pixels[2].move((center[0], center[1] + 1))
                        self.pixels[3].move((center[0], center[1] + 2))
                        self.pixels_position = 1

                elif self.pixels_position == 1:
                    if board[center[1]][center[0] - 1][0] == 0 and board[center[1]][center[0] + 1][0] == 0 \
                            and board[center[1]][center[0] + 2][0] == 0:
                        self.pixels[0].move((center[0] - 1, center[1]))
                        self.pixels[2].move((center[0] + 1, center[1]))
                        self.pixels[3].move((center[0] + 2, center[1]))
                        self.pixels_position = 0

            except IndexError:
                return

        elif self.shape_type == 'L':
            try:
                center = self.pixels[1 if self.pixels_position == 0 or self.pixels_position == 3 else 2].get_coord()

                if center[0] - 1 < 0:
                    raise IndexError

                if self.pixels_position == 0:
                    if board[center[1]][center[0] + 1][0] == 0 and board[center[1]][center[0] - 1][0] == 0 and \
                            board[center[1] + 1][center[0] - 1][0] == 0:
                        self.pixels[0].move((center[0] + 1, center[1]))
                        self.pixels[2].move((center[0] - 1, center[1]))
                        self.pixels[3].move((center[0] - 1, center[1] + 1))
                        self.pixels = [self.pixels[3], self.pixels[2], self.pixels[1], self.pixels[0]]
                        self.pixels_position = 1

                elif self.pixels_position == 1:
                    if board[center[1] - 1][center[0]][0] == 0 and board[center[1] - 1][center[0] - 1][0] == 0 and \
                            board[center[1] + 1][center[0]][0] == 0:
                        self.pixels[0].move((center[0] - 1, center[1] - 1))
                        self.pixels[1].move((center[0], center[1] - 1))
                        self.pixels[3].move((center[0], center[1] + 1))
                        self.pixels = [self.pixels[0], self.pixels[3], self.pixels[2], self.pixels[1]]
                        self.pixels_position = 2

                elif self.pixels_position == 2:
                    if board[center[1]][center[0] + 1][0] == 0 and board[center[1] - 1][center[0] + 1][0] == 0 and \
                            board[center[1]][center[0] - 1][0] == 0:
                        self.pixels[0].move((center[0] + 1, center[1] - 1))
                        self.pixels[1].move((center[0] + 1, center[1]))
                        self.pixels[3].move((center[0] - 1, center[1]))
                        self.pixels = [self.pixels[3], self.pixels[2], self.pixels[1], self.pixels[0]]
                        self.pixels_position = 3

                elif self.pixels_position == 3:
                    if board[center[1] + 1][center[0]][0] == 0 and board[center[1] - 1][center[0]][0] == 0 and \
                            board[center[1] + 1][center[0] + 1][0] == 0:
                        self.pixels[0].move((center[0], center[1] - 1))
                        self.pixels[2].move((center[0], center[1] + 1))
                        self.pixels[3].move((center[0] + 1, center[1] + 1))
                        self.pixels_position = 0

            except IndexError:
                return

        elif self.shape_type == 'J':
            try:
                center = self.pixels[2 if self.pixels_position == 1 else 1].get_coord()

                if center[0] - 1 < 0:
                    raise IndexError

                if self.pixels_position == 0:
                    if board[center[1]][center[0] - 1][0] == 0 and board[center[1]][center[0] + 1][0] == 0 and \
                            board[center[1] - 1][center[0] - 1][0] == 0:
                        self.pixels[0].move((center[0] + 1, center[1]))
                        self.pixels[2].move((center[0] - 1, center[1]))
                        self.pixels[3].move((center[0] - 1, center[1] - 1))
                        self.pixels = [self.pixels[3], self.pixels[2], self.pixels[1], self.pixels[0]]
                        self.pixels_position = 1

                elif self.pixels_position == 1:
                    if board[center[1] - 1][center[0]][0] == 0 and board[center[1] - 1][center[0] + 1][0] == 0 and \
                            board[center[1] + 1][center[0]][0] == 0:
                        self.pixels[0].move((center[0] + 1, center[1] - 1))
                        self.pixels[1].move((center[0], center[1] - 1))
                        self.pixels[3].move((center[0], center[1] + 1))
                        self.pixels = [self.pixels[3], self.pixels[2], self.pixels[1], self.pixels[0]]
                        self.pixels_position = 2

                elif self.pixels_position == 2:
                    if board[center[1]][center[0] - 1][0] == 0 and board[center[1]][center[0] + 1][0] == 0 and \
                            board[center[1] + 1][center[0] + 1][0] == 0:
                        self.pixels[0].move((center[0] - 1, center[1]))
                        self.pixels[2].move((center[0] + 1, center[1]))
                        self.pixels[3].move((center[0] + 1, center[1] + 1))
                        self.pixels_position = 3

                elif self.pixels_position == 3:
                    if board[center[1] - 1][center[0]][0] == 0 and board[center[1] + 1][center[0]][0] == 0 and \
                            board[center[1] + 1][center[0] - 1][0] == 0:
                        self.pixels[0].move((center[0], center[1] - 1))
                        self.pixels[2].move((center[0], center[1] + 1))
                        self.pixels[3].move((center[0] - 1, center[1] + 1))
                        self.pixels_position = 0

            except IndexError:
                return

        elif self.shape_type == 'T':
            try:
                center = self.pixels[1].get_coord()

                if center[0] - 1 < 0:
                    raise IndexError

                if self.pixels_position == 0:
                    if board[center[1] + 1][center[0]][0] == 0:
                        self.pixels[0].move((center[0], center[1] + 1))
                        self.pixels = [self.pixels[3], self.pixels[1], self.pixels[0], self.pixels[2]]
                        self.pixels_position = 1

                elif self.pixels_position == 1:
                    if board[center[1]][center[0] - 1][0] == 0:
                        self.pixels[0].move((center[0] - 1, center[1]))
                        self.pixels = [self.pixels[0], self.pixels[1], self.pixels[3], self.pixels[2]]
                        self.pixels_position = 2

                elif self.pixels_position == 2:
                    if board[center[1] - 1][center[0]][0] == 0:
                        self.pixels[2].move((center[0], center[1] - 1))
                        self.pixels = [self.pixels[2], self.pixels[1], self.pixels[3], self.pixels[0]]
                        self.pixels_position = 3

                elif self.pixels_position == 3:
                    if board[center[1]][center[0] + 1][0] == 0:
                        self.pixels[2].move((center[0] + 1, center[1]))
                        self.pixels = [self.pixels[3], self.pixels[1], self.pixels[2], self.pixels[0]]
                        self.pixels_position = 0

            except IndexError:
                return
