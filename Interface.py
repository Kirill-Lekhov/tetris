import pygame
import os


class Label:
    def __init__(self, rect, text, color=pygame.Color("grey"), bgcolor=pygame.Color("white")):
        self.Rect = pygame.Rect(rect)
        self.text = text
        self.fil = bgcolor == -1

        if bgcolor == -1:
            self.bgcolor = pygame.Color(0, 0, 0)
        else:
            if isinstance(bgcolor, pygame.Color):
                self.bgcolor = bgcolor
            else:
                if isinstance(bgcolor, str):
                    self.bgcolor = pygame.Color(bgcolor)
                else:
                    self.bgcolor = pygame.Color(*bgcolor)

        if isinstance(color, pygame.Color):
            self.font_color = color
        else:
            if isinstance(color, str):
                self.font_color = pygame.Color(color)
            else:
                self.font_color = pygame.Color(*color)

        self.font = pygame.font.Font(None, self.Rect.height - 4)
        self.rendered_text = None
        self.rendered_rect = None

    def render(self, surface):
        if not self.fil:
            surface.fill(self.bgcolor, self.Rect)
        self.rendered_text = self.font.render(self.text, 1, self.font_color)
        self.rendered_rect = self.rendered_text.get_rect(x=self.Rect.x + 2, centery=self.Rect.centery)
        surface.blit(self.rendered_text, self.rendered_rect)

    def update(self, new_text=None):
        if new_text is not None: self.text = new_text


class Show_Next_Shape:
    def __init__(self, top, left, coords_point, color):
        self.width = 4
        self.height = 4
        self.cell_size = 25
        self.top = top
        self.left = left
        self.board = [[(0, pygame.Color('black')) for i in range(self.width)] for k in range(self.height)]
        for i in coords_point:
            x, y = i
            self.board[y][x - 3] = (1, pygame.Color(color))

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

    def update(self, coords_point, color):
        self.board = [[(0, pygame.Color('black')) for i in range(self.width)] for k in range(self.height)]
        for i in coords_point:
            x, y = i
            self.board[y][x - 3] = (1, pygame.Color(color))


class Time(Label):
    def __init__(self, rect, color=pygame.Color("white"), bgcolor=pygame.Color("black"), last_values=None):

        self.time = {'h': 0, 'm': 0, 's': 0, 'ms': 0} if last_values is None else \
            {'h': last_values[0], 'm': last_values[1], 's': last_values[2], 'ms': 0}
        super().__init__(rect, '{}:{}:{}'.format(self.time["h"], self.time["m"], self.time['s']), color, bgcolor)

    def update(self, ms):
        self.time['ms'] += ms
        if self.time['ms'] >= 1000:
            self.time['s'] += 1
            self.time['ms'] = 0
        if self.time['s'] == 60:
            self.time['m'] += 1
            self.time['s'] = 0
        if self.time['m'] == 60:
            self.time['h'] += 1
            self.time['m'] = 0
        self.text = '{}:{}:{}'.format(self.time["h"], self.time["m"], self.time['s'])

    def get_time(self):
        return '{}:{}:{}'.format(self.time["h"], self.time["m"], self.time['s'])
