import pygame
from random import choice
import time


running = True

pygame.init()
size = width, height = 600, 700
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

TYPES = ['I', 'J', 'L', 'O', 'S', 'T', 'Z']
COLORS = ['purple', 'red', 'green', 'blue', 'yellow']
PIXELS = []
STANDARD_ROTATE_J = [[[0, 4], [0, 5], [1, 4], [2, 4]], [[0, 3], [0, 4], [0, 5], [1, 5]],
                     [[0, 5], [1, 5], [2, 5], [2, 4]], [[0, 3], [1, 3], [1, 4], [1, 5]]]
STANDARD_ROTATE_L = [[[0, 4], [0, 5], [1, 5], [1, 6]], [[1, 3], [0, 3], [0, 4], [0, 5]],
                     [[0, 4], [1, 4], [2, 4], [2, 5]], [[1, 3], [1, 4], [1, 5], [0, 5]]]
STANDARD_ROTATE_S = [[[1, 3], [1, 4], [0, 4], [0, 5]], [[0, 4], [1, 4], [1, 5], [2, 5]]]
STANDARD_ROTATE_T = [[[1, 3], [1, 4], [1, 5], [0, 4]], [[0, 4], [1, 4], [2, 4], [1, 5]],
                     [[0, 3], [0, 4], [0, 5], [1, 4]], [[0, 5], [1, 5], [2, 5], [1, 4]]]
STANDARD_ROTATE_Z = [[[0, 3], [0, 4], [1, 4], [1, 5]], [[0, 5], [1, 5], [1, 4], [2, 4]]]


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
        self.coord = coord
        self.color = color

    def get_info(self):
        return self.coord, self.color


class Shape():
    def __init__(self, typ):
        self.typ = typ
        self.color = pygame.Color(choice(COLORS))
        self.move = True
        if self.typ == 'O':
            self.coords = [[0, 4], [0, 5], [1, 5], [1, 4]]
        elif self.typ == 'I':
            self.coords = [[0, 3], [0, 4], [0, 5], [0, 6]]
        elif self.typ == 'J':
            self.coords = choice(STANDARD_ROTATE_J)
        elif self.typ == 'L':
            self.coords = choice(STANDARD_ROTATE_L)
        elif self.typ == 'S':
            self.coords = choice(STANDARD_ROTATE_S)
        elif self.typ == 'T':
            self.coords = choice(STANDARD_ROTATE_T)
        elif self.typ == 'Z':
            self.coords = choice(STANDARD_ROTATE_Z)

    def get_info(self):
        return self.coords, self.color, self.move

    def update_shape(self, board, direction=0):
        new_coords, move = [], True
        for i in self.coords:
            if [i[0] + 1, i[1]] not in self.coords:
                if board[i[0] + 1][i[1]][0] == 1:
                    move = False
                    self.move = False
                    break
        if move:
            for i in self.coords:
                new_coords.append([i[0] + 1, i[1]])
            self.coords = [i[:] for i in new_coords]

    def destroy(self):
        global PIXELS

        for i in self.coords:
            PIXELS.append((i, self.color))


class Game(Board):
    def __init__(self):
        super().__init__()
        self.play = True
        self.shapes = []
        self.speed = [1, False]

    def update(self, new_shape=None):
        self.board = [[(0, pygame.Color('black')) for i in range(self.width)] for k in range(self.height)]
        self.board[-1] = [(1, pygame.Color('black')) for i in range(self.width)]

        for shape in self.shapes:
            coords, color, move = shape.get_info()
            shape.update_shape(self.board)

            for i in coords:
                self.board[i[0]][i[1]] = (1, color)

        if new_shape is not None:
            self.shapes.append(new_shape)

        if all([not i.get_info()[-1] for i in self.shapes]):
            self.shapes.append(Shape(choice(TYPES)))

        # print(all([not i.get_info()[-1] for i in self.shapes]))
        #
        # print(self.shapes)

    def get_shapes(self):
        return self.shapes

    def get_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == 273:
            self.speed[1] = True
        elif event.type == pygame.KEYUP and event.key == 273:
            self.speed[1] = False

    def get_speed(self):
        return 15 if self.speed[1] else self.speed[0]


gui = GUI()
gui.add_element(Game())
gui.update(Shape(choice(TYPES)))

while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        gui.get_event(event)

    gui.render(screen)
    gui.update()

    clock.tick(gui.get_speed())

    pygame.display.flip()
