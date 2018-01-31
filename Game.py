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
        self.height = 20
        self.cell_size = 30
        self.top = 50
        self.left = 50
        self.board = [[(0, pygame.Color('black')) for i in range(width)] for k in range(height+2)]
        self.board[-1] = [(1, pygame.Color('black')) for i in range(width)]

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
        if self.typ == 'O':
            self.coords = [[0, 4], [0, 5], [1, 5], [1, 4]]

    def get_info(self):
        return self.coords, self.color

    def update_shape(self, direction=0, next_line=[]):
        for i in self.coords:
            i[1] += 1 * direction
            i[0] += 1


class Game(Board):
    def __init__(self):
        super().__init__()
        self.play = True
        self.shapes = []

    def update(self, new_shape=None):
        for shape in self.shapes:
            coords, color = shape.get_info()
            shape.update_shape(self.board[max(coords, key=lambda x: x[0])+1])

            self.board = [[(0, pygame.Color('black')) for i in range(width)] for k in range(height + 2)]
            self.board[-1] = [(1, pygame.Color('black')) for i in range(width)]

            for i in coords:
                self.board[i[0]][i[1]] = (1, color)

        if new_shape is not None:
            self.shapes.append(new_shape)

    def get_shapes(self):
        return self.shapes


gui = GUI()
game = Game()
gui.add_element(game)
shape = Shape('O')
print(shape.get_info())
gui.update(shape)
print(game.get_shapes())


while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    gui.render(screen)
    gui.update()
    clock.tick(1)

    pygame.display.flip()
