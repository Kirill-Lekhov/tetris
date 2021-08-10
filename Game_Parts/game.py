from Template import Board
from Game_Parts.shape import Shape
from Interface import ShowNextShape

from random import choice
from pygame import Color
from pygame.key import get_pressed

from constants import SHAPE, REWARD


class Game(Board):
    def __init__(self, surface, old_pixels=None):
        super().__init__()
        self.play = True
        self.shape = Shape(choice(SHAPE))
        self.speed = [False, [10, 0.1]]
        self.next_shape = Shape(choice(SHAPE))
        self.next_shape_render = ShowNextShape(250, 405, [i.get_info()[0] for i in self.next_shape.get_info()[0]],
                                               self.next_shape.get_info()[1])
        self.pixels = self.shape.get_info()[0]
        self.static_pixels = old_pixels[:] if old_pixels is not None else []
        self.surface = surface

        for pixel in self.pixels:
            x, y = pixel.get_info()[0]
            color = pixel.get_info()[1]
            self.board[y][x] = [1, Color(color)]

    def clear_board(self):
        self.board = [[(0, Color('black')) for i in range(self.width)] for k in range(self.height)]
        self.board[-1] = [(1, Color('black')) for i in range(self.width)]

    def update_board(self):
        for pixel in self.pixels + self.static_pixels:
            x, y = pixel.get_info()[0]
            color = pixel.get_info()[1]
            self.board[y][x] = (1, Color(color))

    def update(self):
        self.clear_board()

        for pixel in self.static_pixels:
            x, y = pixel.get_info()[0]
            color = pixel.get_info()[1]
            self.board[y][x] = (1, Color(color))

        if self.shape.update(self.board):
            self.static_pixels += self.pixels[:]
            self.shape = self.next_shape

            for i in self.shape.get_info()[0]:
                x, y = i.get_info()[0]

                if self.board[y][x][0] == 1:
                    self.play = False

                    with open('data/save.tsv', mode='w') as file:
                        file.write('')

            self.next_shape = Shape(choice(SHAPE))
            self.next_shape_render.update([i.get_info()[0] for i in self.next_shape.get_info()[0]],
                                          self.next_shape.get_info()[1])
            self.pixels = self.shape.get_info()[0]

        self.update_board()

    def move_shape(self, clock) -> int:
        score_reward = 0

        self.clear_board()

        for pixel in self.static_pixels:
            x, y = pixel.get_info()[0]
            color = pixel.get_info()[1]
            self.board[y][x] = (1, Color(color))

        pressed_keys = list(get_pressed())
        self.shape.move_sides(self.board, pressed_keys[79] - pressed_keys[80])

        while True:
            n = 0
            score_coefficient = 0

            while n != len(self.board[:-1]):
                if all(map(lambda x: bool(x[0]), self.board[n])):
                    self.static_pixels = list(filter(lambda x: x.get_info()[0][1] != n, self.static_pixels))

                    for i in self.static_pixels:
                        x, y = i.get_info()[0]

                        if y < n:
                            i.move((x, y + 1))

                    score_coefficient += 1

                n += 1

            if score_coefficient > 0:
                score_reward += REWARD[score_coefficient]

            break

        self.update_board()
        self.render(self.surface)
        clock.tick(10)

        return score_reward

    def get_speed(self):
        return self.speed[0], self.speed[1][1] if self.speed[0] else self.speed[1][0]

    def change_speed(self, value):
        self.speed[0] = bool(value)

    def get_next_shape(self):
        return self.next_shape_render

    def get_info(self):
        return self.play

    def get_shape(self):
        return self.shape

    def get_board(self):
        return self.board

    def get_static_pixels(self):
        return [i.get_info() for i in self.static_pixels]
