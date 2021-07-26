from random import choice

from constants import COLORS, TYPES
from pixel import Pixel
from tools import extreme_point


class Shape:
    def __init__(self, typ):
        self.move = True
        self.color = choice(COLORS)
        self.typ = typ
        self.status = choice(TYPES[self.typ])
        self.position = TYPES[self.typ].index(self.status)
        self.pixels = [Pixel(i, self.color) for i in self.status]

    def update(self, board):
        if self.move:
            for i in self.pixels:
                x, y = i.get_info()[0]

                if board[y + 1][x][0] == 1:
                    self.move = False
                    break

        if self.move:
            for i in self.pixels:
                x, y = i.get_info()[0]
                i.move((x, y + 1))

        return not self.move

    def move_sides(self, board, direction=0):
        left_f = direction == -1
        right_f = direction == 1

        if direction == 1:
            extreme_dot = extreme_point([i.get_info() for i in self.pixels], direction)

            for i in extreme_dot:
                if i[1] + 1 >= len(board[0]):
                    right_f = False
                    break

                if board[i[0]][i[1] + 1][0] == 1:
                    right_f = False

        elif direction == -1:
            extreme_dot = extreme_point([i.get_info() for i in self.pixels], direction)

            for i in extreme_dot:
                if i[1] - 1 < 0:
                    left_f = False
                    break

                if board[i[0]][i[1] - 1][0] == 1:
                    left_f = False

        if right_f:
            for i in self.pixels:
                x, y = i.get_info()[0]
                i.move((x + 1, y))

        if left_f:
            for i in self.pixels:
                x, y = i.get_info()[0]
                i.move((x - 1, y))

    def rotate(self, board):
        if not self.move:
            return

        if self.typ == 'O':
            return

        elif self.typ == 'Z':
            center = self.pixels[2].get_info()[0]

            try:
                if center[0] - 1 < 0:
                    raise IndexError

                if self.position == 0:
                    if board[center[1] - 1][center[0] + 1][0] == 0 and board[center[1] + 1][center[0]][0] == 0:
                        self.pixels[0].move((center[0], center[1] + 1))
                        self.pixels[1].move((center[0] + 1, center[1] - 1))
                        self.pixels = [self.pixels[1], self.pixels[3], self.pixels[2], self.pixels[0]]
                        self.position = 1

                elif self.position == 1:
                    if board[center[1] - 1][center[0] - 1][0] == 0 and board[center[1] - 1][center[0]][0] == 0:
                        self.pixels[0].move((center[0], center[1] - 1))
                        self.pixels[3].move((center[0] - 1, center[1] - 1))
                        self.pixels = [self.pixels[3], self.pixels[0], self.pixels[2], self.pixels[1]]
                        self.position = 0

            except IndexError:
                return

        elif self.typ == 'S':
            center = self.pixels[1].get_info()[0]

            try:
                if center[0] - 1 < 0:
                    raise IndexError

                if self.position == 0:
                    if board[center[1] + 1][center[0] + 1][0] == 0 and board[center[1]][center[0] + 1][0] == 0:
                        self.pixels[0].move((center[0] + 1, center[1] + 1))
                        self.pixels[3].move((center[0] + 1, center[1]))
                        self.pixels = [self.pixels[2], self.pixels[1], self.pixels[3], self.pixels[0]]
                        self.position = 1

                elif self.position == 1:
                    if board[center[1] - 1][center[0] + 1][0] == 0 and board[center[1]][center[0] - 1][0] == 0:
                        self.pixels[2].move((center[0] - 1, center[1]))
                        self.pixels[3].move((center[0] + 1, center[1] - 1))
                        self.pixels = [self.pixels[2], self.pixels[1], self.pixels[0], self.pixels[3]]
                        self.position = 0

            except IndexError:
                return

        elif self.typ == 'I':
            try:
                center = self.pixels[1].get_info()[0]

                if center[0] - 1 < 0:
                    raise IndexError

                if self.position == 0:
                    if board[center[1] - 1][center[0]][0] == 0 and board[center[1] + 1][center[0]][0] == 0 \
                            and board[center[1] + 2][center[0]][0] == 0:
                        self.pixels[0].move((center[0], center[1] - 1))
                        self.pixels[2].move((center[0], center[1] + 1))
                        self.pixels[3].move((center[0], center[1] + 2))
                        self.position = 1

                elif self.position == 1:
                    if board[center[1]][center[0] - 1][0] == 0 and board[center[1]][center[0] + 1][0] == 0 \
                            and board[center[1]][center[0] + 2][0] == 0:
                        self.pixels[0].move((center[0] - 1, center[1]))
                        self.pixels[2].move((center[0] + 1, center[1]))
                        self.pixels[3].move((center[0] + 2, center[1]))
                        self.position = 0

            except IndexError:
                return

        elif self.typ == 'L':
            try:
                center = self.pixels[1 if self.position == 0 or self.position == 3 else 2].get_info()[0]

                if center[0] - 1 < 0:
                    raise IndexError

                if self.position == 0:
                    if board[center[1]][center[0] + 1][0] == 0 and board[center[1]][center[0] - 1][0] == 0 and \
                            board[center[1] + 1][center[0] - 1][0] == 0:
                        self.pixels[0].move((center[0] + 1, center[1]))
                        self.pixels[2].move((center[0] - 1, center[1]))
                        self.pixels[3].move((center[0] - 1, center[1] + 1))
                        self.pixels = [self.pixels[3], self.pixels[2], self.pixels[1], self.pixels[0]]
                        self.position = 1

                elif self.position == 1:
                    if board[center[1] - 1][center[0]][0] == 0 and board[center[1] - 1][center[0] - 1][0] == 0 and \
                            board[center[1] + 1][center[0]][0] == 0:
                        self.pixels[0].move((center[0] - 1, center[1] - 1))
                        self.pixels[1].move((center[0], center[1] - 1))
                        self.pixels[3].move((center[0], center[1] + 1))
                        self.pixels = [self.pixels[0], self.pixels[3], self.pixels[2], self.pixels[1]]
                        self.position = 2

                elif self.position == 2:
                    if board[center[1]][center[0] + 1][0] == 0 and board[center[1] - 1][center[0] + 1][0] == 0 and \
                            board[center[1]][center[0] - 1][0] == 0:
                        self.pixels[0].move((center[0] + 1, center[1] - 1))
                        self.pixels[1].move((center[0] + 1, center[1]))
                        self.pixels[3].move((center[0] - 1, center[1]))
                        self.pixels = [self.pixels[3], self.pixels[2], self.pixels[1], self.pixels[0]]
                        self.position = 3

                elif self.position == 3:
                    if board[center[1] + 1][center[0]][0] == 0 and board[center[1] - 1][center[0]][0] == 0 and \
                            board[center[1] + 1][center[0] + 1][0] == 0:
                        self.pixels[0].move((center[0], center[1] - 1))
                        self.pixels[2].move((center[0], center[1] + 1))
                        self.pixels[3].move((center[0] + 1, center[1] + 1))
                        self.position = 0

            except IndexError:
                return

        elif self.typ == 'J':
            try:
                center = self.pixels[2 if self.position == 1 else 1].get_info()[0]

                if center[0] - 1 < 0:
                    raise IndexError

                if self.position == 0:
                    if board[center[1]][center[0] - 1][0] == 0 and board[center[1]][center[0] + 1][0] == 0 and \
                            board[center[1] - 1][center[0] - 1][0] == 0:
                        self.pixels[0].move((center[0] + 1, center[1]))
                        self.pixels[2].move((center[0] - 1, center[1]))
                        self.pixels[3].move((center[0] - 1, center[1] - 1))
                        self.pixels = [self.pixels[3], self.pixels[2], self.pixels[1], self.pixels[0]]
                        self.position = 1

                elif self.position == 1:
                    if board[center[1] - 1][center[0]][0] == 0 and board[center[1] - 1][center[0] + 1][0] == 0 and \
                            board[center[1] + 1][center[0]][0] == 0:
                        self.pixels[0].move((center[0] + 1, center[1] - 1))
                        self.pixels[1].move((center[0], center[1] - 1))
                        self.pixels[3].move((center[0], center[1] + 1))
                        self.pixels = [self.pixels[3], self.pixels[2], self.pixels[1], self.pixels[0]]
                        self.position = 2

                elif self.position == 2:
                    if board[center[1]][center[0] - 1][0] == 0 and board[center[1]][center[0] + 1][0] == 0 and \
                            board[center[1] + 1][center[0] + 1][0] == 0:
                        self.pixels[0].move((center[0] - 1, center[1]))
                        self.pixels[2].move((center[0] + 1, center[1]))
                        self.pixels[3].move((center[0] + 1, center[1] + 1))
                        self.position = 3

                elif self.position == 3:
                    if board[center[1] - 1][center[0]][0] == 0 and board[center[1] + 1][center[0]][0] == 0 and \
                            board[center[1] + 1][center[0] - 1][0] == 0:
                        self.pixels[0].move((center[0], center[1] - 1))
                        self.pixels[2].move((center[0], center[1] + 1))
                        self.pixels[3].move((center[0] - 1, center[1] + 1))
                        self.position = 0

            except IndexError:
                return

        elif self.typ == 'T':
            try:
                center = self.pixels[1].get_info()[0]

                if center[0] - 1 < 0:
                    raise IndexError

                if self.position == 0:
                    if board[center[1] + 1][center[0]][0] == 0:
                        self.pixels[0].move((center[0], center[1] + 1))
                        self.pixels = [self.pixels[3], self.pixels[1], self.pixels[0], self.pixels[2]]
                        self.position = 1

                elif self.position == 1:
                    if board[center[1]][center[0] - 1][0] == 0:
                        self.pixels[0].move((center[0] - 1, center[1]))
                        self.pixels = [self.pixels[0], self.pixels[1], self.pixels[3], self.pixels[2]]
                        self.position = 2

                elif self.position == 2:
                    if board[center[1] - 1][center[0]][0] == 0:
                        self.pixels[2].move((center[0], center[1] - 1))
                        self.pixels = [self.pixels[2], self.pixels[1], self.pixels[3], self.pixels[0]]
                        self.position = 3

                elif self.position == 3:
                    if board[center[1]][center[0] + 1][0] == 0:
                        self.pixels[2].move((center[0] + 1, center[1]))
                        self.pixels = [self.pixels[3], self.pixels[1], self.pixels[2], self.pixels[0]]
                        self.position = 0

            except IndexError:
                return

    def get_info(self):
        return self.pixels, self.color, self.move
