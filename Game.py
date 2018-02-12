import pygame
from random import choice
import time
import timeit


running = True

pygame.init()
size = width, height = 600, 700
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

COLORS = ['purple', 'red', 'green', 'blue', 'yellow']
SHAPE = ['J', 'L', 'S', 'T', 'Z', 'I', 'O']
TYPES = {'J': [[[0, 5], [1, 5], [2, 5], [2, 4]], [[0, 3], [1, 3], [1, 4], [1, 5]],
               [[2, 4], [1, 4], [0, 4], [0, 5]], [[0, 3], [0, 4], [0, 5], [1, 5]]],
         'L': [[[0, 4], [1, 4], [2, 4], [2, 5]], [[1, 3], [0, 3], [0, 4], [0, 5]],
               [[0, 4], [0, 5], [1, 5], [2, 5]], [[1, 3], [1, 4], [1, 5], [0, 5]]],
         'S': [[[1, 3], [1, 4], [0, 4], [0, 5]], [[0, 4], [1, 4], [1, 5], [2, 5]]],
         'T': [[[1, 3], [1, 4], [1, 5], [0, 4]], [[0, 4], [1, 4], [2, 4], [1, 5]],
               [[0, 3], [0, 4], [0, 5], [1, 4]], [[0, 5], [1, 5], [2, 5], [1, 4]]],
         'Z': [[[0, 3], [0, 4], [1, 4], [1, 5]], [[0, 5], [1, 5], [1, 4], [2, 4]]],
         'I': [[[0, 3], [0, 4], [0, 5], [0, 6]]],
         'O': [[[0, 4], [0, 5], [1, 5], [1, 4]]]}


def extreme_point(lists, direction):
    ys = set(i[0][1] for i in lists)
    dots = [(i, [k[0][0] for k in lists if k[0][1] == i]) for i in ys]
    return [[i[0], max(i[1])] for i in dots] if direction == 1 else [[i[0], min(i[1])] for i in dots]


class GUI:
    def __init__(self):
        self.elements = []

    def add_element(self, element):
        self.elements.append(element)

    def render(self, surface):
        for element in self.elements:
            render = getattr(element, "render", None)
            if callable(render):
                element.render(surface)

    def update(self, new_element=None):
        for element in self.elements:
            update = getattr(element, "update", None)
            if callable(update):
                element.update(new_element)

    def get_event(self, event):
        for element in self.elements:
            get_event = getattr(element, "get_event", None)
            if callable(get_event):
                element.get_event(event)

    def get_speed(self):
        for element in self.elements:
            get_speed = getattr(element, "get_speed", None)
            if callable(get_speed):
                return element.get_speed()


class Board:
    def __init__(self):
        self.width = 10
        self.height = 20 + 1
        self.cell_size = 30
        self.top = 50
        self.left = 50
        self.board = [[(0, pygame.Color('black')) for i in range(self.width)] for k in range(self.height)]
        self.board[-1] = [(1, pygame.Color('black')) for i in range(self.width)]

    def render(self, surface):
        for i in range(self.height):
            for k in range(self.width):
                pygame.draw.rect(surface, (255, 255, 255), (
                    self.left + k * self.cell_size,
                    self.top + i * self.cell_size,
                    self.cell_size,
                    self.cell_size), 1)
                pygame.draw.rect(surface, self.board[i][k][1], (
                    self.left + k * self.cell_size + 1,
                    self.top + i * self.cell_size + 1,
                    self.cell_size - 2,
                    self.cell_size - 2))

        for k in range(self.width):
            pygame.draw.rect(surface, (255, 0, 0), (
                self.left + k * self.cell_size,
                self.top - 1 * self.cell_size,
                self.cell_size,
                self.cell_size), 1)
            pygame.draw.rect(surface, (0, 0, 0), (
                self.left + k * self.cell_size + 1,
                self.top -1 * self.cell_size + 1,
                self.cell_size - 2,
                self.cell_size - 2))

            pygame.draw.rect(surface, (255, 0, 0), (
                self.left + k * self.cell_size,
                self.top + 20 * self.cell_size,
                self.cell_size,
                self.cell_size), 1)
            pygame.draw.rect(surface, (0, 0, 0), (
                self.left + k * self.cell_size + 1,
                self.top + 20 * self.cell_size + 1,
                self.cell_size - 2,
                self.cell_size - 2))

        for i in range(self.height):
            pygame.draw.rect(surface, (255, 0, 0), (
                self.left - 1 * self.cell_size,
                self.top + i * self.cell_size,
                self.cell_size,
                self.cell_size), 1)
            pygame.draw.rect(surface, (0, 0, 0), (
                self.left - 1 * self.cell_size + 1,
                self.top + i * self.cell_size + 1,
                self.cell_size - 2,
                self.cell_size - 2))

            pygame.draw.rect(surface, (255, 0, 0), (
                self.left + self.width * self.cell_size,
                self.top + i * self.cell_size,
                self.cell_size,
                self.cell_size), 1)
            pygame.draw.rect(surface, (0, 0, 0), (
                self.left + self.width * self.cell_size + 1,
                self.top + i * self.cell_size + 1,
                self.cell_size - 2,
                self.cell_size - 2))


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


class Shapes:
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
                if center[0] - 1 < 0: raise IndexError
                if self.position == 0:
                    if board[center[1] - 1][center[0] + 1][0] == 0 and board[center[1] - 1][center[0]][0] == 0:
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
                if center[0] - 1 < 0: raise IndexError
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
                if center[0] - 1 < 0: raise IndexError
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
                if center[0] - 1 < 0: raise IndexError
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
                if center[0] - 1 < 0: raise IndexError
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
                if center[0] - 1 < 0: raise IndexError
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


class Game(Board):
    def __init__(self):
        super().__init__()
        self.play = True
        self.shape = Shapes(choice(SHAPE))
        self.speed = [False, [10, 0.1]]
        self.next_shape = Shapes(choice(SHAPE))
        self.pixels = self.shape.get_info()[0]
        self.statick_pixels = []
        self.overturn = False

        for pixel in self.pixels:
            x, y = pixel.get_info()[0]
            color = pixel.get_info()[1]
            self.board[y][x] = [1, pygame.Color(color)]

    def clear_board(self):
        self.board = [[(0, pygame.Color('black')) for i in range(self.width)] for k in range(self.height)]
        self.board[-1] = [(1, pygame.Color('black')) for i in range(self.width)]

    def update_board(self):
        for pixel in self.pixels + self.statick_pixels:
            x, y = pixel.get_info()[0]
            color = pixel.get_info()[1]
            self.board[y][x] = (1, pygame.Color(color))

    def game_over(self):
        self.__init__()

    def update(self, screen):
        self.clear_board()

        for pixel in self.statick_pixels:
            x, y = pixel.get_info()[0]
            color = pixel.get_info()[1]
            self.board[y][x] = (1, pygame.Color(color))

        if self.shape.update(self.board):
            self.statick_pixels += self.pixels[:]
            self.shape = self.next_shape

            for i in self.shape.get_info()[0]:
                x, y = i.get_info()[0]
                if self.board[y][x][0] == 1:
                    self.game_over()

            self.next_shape = Shapes(choice(SHAPE))
            self.pixels = self.shape.get_info()[0]

        # pygame.key.get_pressed()[276], pygame.key.get_pressed()[273],
        # pygame.key.get_pressed()[274], pygame.key.get_pressed()[275]

        self.update_board()
        self.render(screen)

    def move_shape(self, screen):
        self.clear_board()
        for pixel in self.statick_pixels:
            x, y = pixel.get_info()[0]
            color = pixel.get_info()[1]
            self.board[y][x] = (1, pygame.Color(color))

        self.shape.move_sides(self.board,
                              pygame.key.get_pressed()[275] - pygame.key.get_pressed()[276])

        if self.overturn and not bool(pygame.key.get_pressed()[273]):
            self.shape.rotate(self.board)
            self.overturn = not self.overturn

        if pygame.key.get_pressed()[273]: self.overturn = not self.overturn

        while True:
            n = 0
            while n != len(self.board[:-1]):
                if all(map(lambda x: bool(x[0]), self.board[n])):
                    self.statick_pixels = list(filter(lambda x: x.get_info()[0][1] != n, self.statick_pixels))
                    for i in self.statick_pixels:
                        x, y = i.get_info()[0]
                        if y < n:
                            i.move((x, y + 1))
                n += 1
            break

        self.update_board()
        self.render(screen)
        clock.tick(10)

    def get_speed(self):
        return self.speed[0], self.speed[1][1] if self.speed[0] else self.speed[1][0]

    def change_speed(self, value):
        self.speed[0] = bool(value)


gui = GUI()
GAME = Game()
gui.add_element(GAME)
gui.render(screen)
N = 0

while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        GAME.change_speed(pygame.key.get_pressed()[274])

    GAME.move_shape(screen)

    if not GAME.get_speed()[0]:
        if int(N % GAME.get_speed()[1]) == 0:
            gui.update(screen)
    else:
        gui.update(screen)

    N += 1
    pygame.display.flip()
