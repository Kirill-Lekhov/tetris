import pygame
from random import choice
import time


running = True

pygame.init()
size = width, height = 600, 700
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

types = ['I', 'J', 'L', 'O', 'S', 'T', 'Z']
colors = ['purple', 'red', 'green', 'blue', 'yellow']


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


class Shape():
    def __init__(self, typ):
        self.typ = typ
        self.color = pygame.Color(choice(colors))
        self.move = True
        if self.typ == 'O':
            self.coords = [[0, 4], [0, 5], [1, 5], [1, 4]]

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


class Game(Board):
    def __init__(self):
        super().__init__()
        self.play = True
        self.shapes = []

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
            self.shapes.append(Shape('O'))

        print(all([not i.get_info()[-1] for i in self.shapes]))

        print(self.shapes)

    def get_shapes(self):
        return self.shapes


gui = GUI()
gui.add_element(Game())
gui.update(Shape('O'))

while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    gui.render(screen)
    gui.update()

    clock.tick(1)

    pygame.display.flip()
