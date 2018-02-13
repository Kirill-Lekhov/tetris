import pygame


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
