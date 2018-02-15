import pygame
import os
import sys
from random import choice
from Template import Board, GUI
from Interface import Label, Show_Next_Shape, Time


running = True

pygame.init()
size = width, height = 600, 700
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
pygame.mixer.music.load('data/Tetris.ogg')
pygame.mixer.music.play(-1)

COLORS = ['purple', 'red', 'green', 'blue', 'yellow']
SHAPE = ['J', 'L', 'S', 'T', 'Z', 'I', 'O']
REWARD = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}
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
SCORE = 0

fon_picture = pygame.sprite.Group()
logo_picture = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
back_button = pygame.sprite.Group()


def load_image(name, colorkey = None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


def extreme_point(lists, direction):
    ys = set(i[0][1] for i in lists)
    dots = [(i, [k[0][0] for k in lists if k[0][1] == i]) for i in ys]
    return [[i[0], max(i[1])] for i in dots] if direction == 1 else [[i[0], min(i[1])] for i in dots]


def terminate():
    pygame.quit()
    sys.exit()


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


class ImageButton(pygame.sprite.Sprite):
    button = load_image('button.png')
    pressed_button = load_image('button_1.png')
    back_b = load_image('back.png')

    def __init__(self, group, x, y, ty=None):
        super().__init__(group)
        self.image = ImageButton.button if ty is None else ImageButton.back_b
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.press = False

    def update(self, press):
        self.press = press
        if not self.press:
            self.image = ImageButton.button
            self.rect.x = self.x - 5
            self.rect.y = self.y - 5
            self.press = not self.press
        else:
            self.image = ImageButton.pressed_button
            self.rect.x = self.x
            self.rect.y = self.y
            self.press = not self.press

    def get_rect(self):
        return self.rect


class Button:
    def __init__(self, x, y, text, color):
        self.text = text
        self.pressed = False
        self.last_pressed = False
        self.button = ImageButton(all_sprites, x, y)
        self.Rect = self.button.get_rect()
        self.font = pygame.font.Font(None, self.Rect.height - 15)
        self.font_color = pygame.Color(color)
        self.rendered_text = None
        self.rendered_rect = None

    def render(self, surface):
        self.rendered_text = self.font.render(self.text, 1, self.font_color)
        if not self.pressed:
            self.font = pygame.font.Font(None, self.Rect.height - 15)
            self.rendered_rect = self.rendered_text.get_rect(center=self.Rect.center)
            self.button.update(self.pressed)
        else:
            self.font = pygame.font.Font(None, self.Rect.height - 20)
            self.rendered_rect = self.rendered_text.get_rect(center=self.Rect.center)
            self.button.update(self.pressed)
        surface.blit(self.rendered_text, self.rendered_rect)

    def get_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.pressed = self.Rect.collidepoint(event.pos)
            self.last_pressed = self.pressed
        else:
            self.pressed = False

        return self.pressed != self.last_pressed

    def get_button(self):
        return self.button


class Game(Board):
    def __init__(self, surface, old_pixels=None):
        super().__init__()
        self.play = True
        self.shape = Shapes(choice(SHAPE))
        self.speed = [False, [10, 0.1]]
        self.next_shape = Shapes(choice(SHAPE))
        self.next_shape_render = Show_Next_Shape(250, 405, [i.get_info()[0] for i in self.next_shape.get_info()[0]],
                                                 self.next_shape.get_info()[1])
        self.pixels = self.shape.get_info()[0]
        self.statick_pixels = old_pixels[:] if old_pixels is not None else []
        self.overturn = False
        self.surface = surface

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

    def update(self, pas=None):
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
                    self.play = False

            self.next_shape = Shapes(choice(SHAPE))
            self.next_shape_render.update([i.get_info()[0] for i in self.next_shape.get_info()[0]],
                                          self.next_shape.get_info()[1])
            self.pixels = self.shape.get_info()[0]

        self.update_board()

    def move_shape(self):
        global SCORE

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
            score_сoefficient = 0
            while n != len(self.board[:-1]):
                if all(map(lambda x: bool(x[0]), self.board[n])):
                    self.statick_pixels = list(filter(lambda x: x.get_info()[0][1] != n, self.statick_pixels))
                    for i in self.statick_pixels:
                        x, y = i.get_info()[0]
                        if y < n:
                            i.move((x, y + 1))
                    score_сoefficient += 1

                n += 1
            SCORE += REWARD[score_сoefficient]
            break

        self.update_board()
        self.render(self.surface)
        clock.tick(10)

    def get_speed(self):
        return self.speed[0], self.speed[1][1] if self.speed[0] else self.speed[1][0]

    def change_speed(self, value):
        self.speed[0] = bool(value)

    def get_next_shape(self):
        return self.next_shape_render

    def get_info(self):
        return self.play

    def get_statick_pixels(self):
        return [i.get_info() for i in self.statick_pixels]


def load_old_game():
    with open('data/save.txt', mode='r') as f:
        lines = [i.strip() for i in f.readlines()]
        score = int(lines[0])
        time = list(map(int, lines[1].split(':')))
        lines = [i.strip().strip('(').strip(')').split(', ') for i in lines[2:]]
        old_pixels = [Pixel((int(i[1]), int(i[0])), i[2]) for i in lines]
    return old_pixels, score, time


def save_game(statick_pixels, score, time):
    with open('data/save.txt', mode='a') as f:
        f.write(str(score)+'\n')
        f.write(time+'\n')
        f.write('\n'.join(['('+', '.join(map(str, i[0]))+', '+i[1]+')' for i in statick_pixels]))


def add_record(new_value):
    with open('data/records.txt', mode='r') as file:
        lines = [i.strip().split()[1:] for i in file.readlines()]
        lines.append(new_value.split())
    with open('data/records.txt', mode='w') as file:
        file.write('\n'.join(map(lambda x: str(lines.index(x)+1) + ') ' + ' '.join(x), lines)))


def show_records():
    show_record = True
    with open('data/records.txt', mode='r') as file:
        lines = [i.strip().split()[1:] for i in file.readlines()]

    fon = pygame.sprite.Sprite()
    fon.image = load_image("Fon_F.png")
    fon.rect = fon.image.get_rect()
    fon_picture.add(fon)

    labels = [Label((200, 100 + 20 * i, 200, 50), lines[i]) for i in range(len(lines))]

    button_back = ImageButton(back_button, 50, 50, True)

    while show_record:
        back_button.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                show_record = False
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and \
                    button_back.get_rect().collidepoint(event.pos):
                show_record = False

        for i in labels:
            i.render(screen)
        pygame.display.flip()


def main():
    all_sprites.empty()
    main = True
    old_save = bool(open('data/save.txt', mode='r').readlines())

    fon = pygame.sprite.Sprite()
    logo = pygame.sprite.Sprite()
    fon.image = load_image("Fon_F.png")
    logo.image = load_image('logo.png')
    fon.rect = fon.image.get_rect()
    logo.rect = logo.image.get_rect()
    logo.rect.y = 100
    logo.rect.x = 60
    fon_picture.add(fon)
    logo_picture.add(logo)

    fon_picture.draw(screen)
    logo_picture.draw(screen)

    old_pixels = None
    score = 0
    time = None

    if old_save:
        buttons = [Button(185, 270, "Новая Игра", 'white'), Button(185, 340, "Продолжить", 'white'),
                   Button(185, 410, "Рекорды", 'white')]
    else:
        buttons = [Button(185, 270, "Новая Игра", 'white'), Button(185, 340, "Рекорды", 'white')]

    for i in buttons:
        all_sprites.add(i.get_button())

    while main:
        fon_picture.draw(screen)
        logo_picture.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            for i in range(len(buttons)):
                if buttons[i].get_event(event) and i == 0:
                    main = False
                    all_sprites.empty()
                    break
                elif buttons[i].get_event(event) and i == 1 and old_save:
                    old_values = load_old_game()
                    old_pixels, score, time = old_values[0][:], old_values[1], old_values[2][:]
                    main = False
                    break
                elif buttons[i].get_event(event) and i == 1 and not old_save:
                    # show_records()
                    pass
                elif buttons[i].get_event(event) and i == 2:
                    # show_records()
                    pass

        all_sprites.draw(screen)
        for i in buttons:
            i.render(screen)

        pygame.display.flip()
    return old_pixels, score, time


def game(old_pixels, score, time):
    global SCORE
    fon = pygame.sprite.Sprite()
    fon.image = load_image("Fon_F.png")
    fon.rect = fon.image.get_rect()
    fon_picture.add(fon)
    SCORE = score
    gui = GUI()
    GAME = Game(screen, old_pixels)
    text_score_head = Label((400, 75, 150, 65), "Score:", "White", -1)
    text_score = Label((400, 135, 150, 50), str(SCORE), "White", -1)
    text_next_shape = Label((400, 200, 150, 50), "Next Shape", "White", -1)
    text_pause_shape = Label((80, 200, 200, 200), "PAUSE", "blue", -1)
    text_time = Label((400, 365, 150, 50), "Time:", "white", -1)

    time = Time((450, 400, 150, 50), 'white', -1, time)

    gui.add_element(text_score_head)
    gui.add_element(text_score)
    gui.add_element(text_next_shape)
    gui.add_element(GAME.get_next_shape())
    gui.add_element(text_time)
    gui.add_element(time)

    rungame = True

    N = 1
    pause = False

    while rungame:
        if not GAME.get_info(): break
        fon_picture.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rungame = False
                if GAME.get_statick_pixels():
                    with open('data/save.txt', 'w') as file:
                        file.write('')
                    save_game(GAME.get_statick_pixels(), SCORE, time.get_time())
                    all_sprites.empty()
                else:
                    with open('data/save.txt', 'w') as file:
                        file.write('')
                break
            if event.type == pygame.KEYUP and event.key == 112:
                pause = not pause
            if not pause:
                GAME.change_speed(pygame.key.get_pressed()[274])

        gui.render(screen)
        if not pause:
            GAME.move_shape()
            text_score.update(str(SCORE))
            time.update(clock.get_time())
            if not GAME.get_speed()[0]:
                if int(N % GAME.get_speed()[1]) == 0:
                    GAME.update()
            else:
                GAME.update()
            N += 1

        else:
            GAME.render(screen)
            text_pause_shape.render(screen)
        pygame.display.flip()


while running:
    old_pixels, score, time = main()
    game(old_pixels, score, time)
