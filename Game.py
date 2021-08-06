import pygame
from random import choice
from Template import Board, GUI
from Interface import Label, TextBox, ShowNextShape, Time

from constants import *
from Game_Parts.shape import Shape

from Tools import game_file_functions
from Tools.load_image import load_image
from Tools.os_tools import terminate

from GUI.picture_button import PictureButton
from GUI.back_button import BackButton


running = True

pygame.init()
size = width, height = 600, 700
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

# Настройки музыки
pygame.mixer.music.load('data/music/main_theme.ogg')
pygame.mixer.music.play(-1)
music = pygame.mixer.Sound('data/music/deleting_line_sound.wav')
# Настройки музыки

# Группы
fon_picture = pygame.sprite.Group()
logo_picture = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
back_button = pygame.sprite.Group()
# Группы


class Button:
    def __init__(self, x, y, text, color):
        self.text = text
        self.pressed = False
        self.last_pressed = False
        self.button = PictureButton((x, y), all_sprites)
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
            self.pressed = self.last_pressed = self.Rect.collidepoint(event.pos)

        else:
            self.pressed = False

        if self.pressed != self.last_pressed:
            return True

    def get_button(self):
        return self.button

    def default_values(self):
        self.pressed = False
        self.last_pressed = False


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
        self.statick_pixels = old_pixels[:] if old_pixels is not None else []
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

    def update(self):
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

                    with open('data/save.tsv', mode='w') as file:
                        file.write('')

            self.next_shape = Shape(choice(SHAPE))
            self.next_shape_render.update([i.get_info()[0] for i in self.next_shape.get_info()[0]],
                                          self.next_shape.get_info()[1])
            self.pixels = self.shape.get_info()[0]

        self.update_board()

    def move_shape(self):
        global SCORE
        global ROTATE

        self.clear_board()

        for pixel in self.statick_pixels:
            x, y = pixel.get_info()[0]
            color = pixel.get_info()[1]
            self.board[y][x] = (1, pygame.Color(color))

        pressed_keys = list(pygame.key.get_pressed())
        self.shape.move_sides(self.board, pressed_keys[79] - pressed_keys[80])

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

            if score_сoefficient > 0:
                music.play().set_volume(0.4)
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

    def get_shape(self):
        return self.shape

    def get_board(self):
        return self.board

    def get_statick_pixels(self):
        return [i.get_info() for i in self.statick_pixels]


def leaderboard():
    leaderboard = True
    new_screen = pygame.Surface(size)
    back_button.empty()

    logo = Label((190, 100, 100, 70), 'РЕКОРДЫ', 'white', -1)
    rec = game_file_functions.load_records()
    leaders = [Label((100, 170 + i * 50, 100, 50), rec[i], 'white', -1) for i in range(len(rec))]
    button = BackButton((50, 50), back_button)
    back_button.add(button)

    while leaderboard:
        fon_picture.draw(new_screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            if button.update(event):
                leaderboard = False
                button.default_values()

        back_button.draw(new_screen)
        logo.render(new_screen)

        for i in leaders:
            i.render(new_screen)

        screen.blit(new_screen, (0, 0, width, height))
        pygame.display.flip()


def main():
    global NAME

    all_sprites.empty()
    main = True
    old_save = bool(open('data/save.tsv', mode='r').readlines())

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

    text = Label((50, 600, 50, 50), 'Игрок: ', 'white', -1)
    name = TextBox((160, 600, 135, 50), NAME)

    fon_picture.draw(screen)
    logo_picture.draw(screen)

    old_pixels = None
    score = 0
    time = None

    if old_save:
        buttons = [Button(185, 270, "Новая Игра", 'white'),
                   Button(185, 340, "Продолжить", 'white'),
                   Button(185, 410, "Рекорды", 'white')]
    else:
        buttons = [Button(185, 270, "Новая Игра", 'white'),
                   Button(185, 340, "Рекорды", 'white')]

    for i in buttons:
        all_sprites.add(i.get_button())

    while main:
        fon_picture.draw(screen)
        logo_picture.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            name.get_event(event)

            for i in range(len(buttons)):
                if buttons[i].get_event(event) and i == 0:
                    main = False
                    all_sprites.empty()
                    buttons[i].default_values()
                    break

                elif buttons[i].get_event(event) and i == 1 and old_save:
                    old_values = game_file_functions.load_game()
                    old_pixels, score, time = old_values[0][:], old_values[1], old_values[2][:]
                    main = False
                    buttons[i].default_values()
                    break

                elif buttons[i].get_event(event) and i == 1 and not old_save:
                    buttons[i].default_values()
                    leaderboard()

                elif buttons[i].get_event(event) and i == 2:
                    buttons[i].default_values()
                    leaderboard()

        text.render(screen)
        name.render(screen)
        name.update()
        NAME = name.get_text()

        all_sprites.draw(screen)

        for i in buttons:
            i.render(screen)

        pygame.display.flip()

    return old_pixels, score, time


def game(old_pixels, score, time):
    global SCORE
    global ROTATE

    all_sprites.empty()

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

    text_help_1 = Label((390, 450, 25, 25), "P:Пауза", "white", -1)
    text_help_2 = Label((390, 475, 25, 25), "Esc:Выход", "white", -1)
    text_help_3 = Label((390, 500, 25, 25), "Влево\вправо:Перемещение", "white", -1)
    text_help_4 = Label((390, 525, 25, 25), "Вверх:Поворот", "white", -1)
    text_help_5 = Label((390, 550, 25, 25), "Вниз:Ускорить падение", "white", -1)
    dilog = Label((90, 275, 45, 45), "Вы уверены что хотите выйти?", "white", -1)
    buttons = [Button(100, 340, "Да", 'white'), Button(325, 340, "Нет", 'white')]

    for i in buttons:
        all_sprites.add(i.get_button())

    time = Time((450, 400, 150, 50), 'white', -1, time)

    gui.add_element(text_score_head)
    gui.add_element(text_score)
    gui.add_element(text_next_shape)
    gui.add_element(GAME.get_next_shape())
    gui.add_element(text_time)
    gui.add_element(text_help_1)
    gui.add_element(text_help_2)
    gui.add_element(text_help_3)
    gui.add_element(text_help_4)
    gui.add_element(text_help_5)
    gui.add_element(time)

    rungame = True

    N = 1
    pause = False
    dilog_window = False

    while rungame:
        if not GAME.get_info():
            break

        fon_picture.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if GAME.get_statick_pixels():
                    with open('data/save.tsv', 'w') as file:
                        file.write('')

                    game_file_functions.save_game(GAME.get_statick_pixels(), SCORE, time.get_time())

                else:
                    with open('data/save.tsv', 'w') as file:
                        file.write('')

                terminate()

            if event.type == pygame.KEYDOWN and event.key == 27:
                dilog_window = True

                if GAME.get_statick_pixels():
                    with open('data/save.tsv', 'w') as file:
                        file.write('')

                    game_file_functions.save_game(GAME.get_statick_pixels(), SCORE, time.get_time())

                else:
                    with open('data/save.tsv', 'w') as file:
                        file.write('')

            if not dilog_window:
                if event.type == pygame.KEYUP and event.key == pygame.K_UP:
                    GAME.get_shape().rotate(GAME.get_board())

                if event.type == pygame.KEYUP and event.key == 112:
                    pause = not pause

                if not pause:
                    # стрелка вниз, увеличение скорости падения фигур
                    GAME.change_speed(0)

            else:
                for i in range(len(buttons)):
                    if buttons[i].get_event(event) and i == 0:
                        rungame = False
                        all_sprites.empty()
                        buttons[i].default_values()
                        break

                    elif buttons[i].get_event(event) and i == 1:
                        dilog_window = False
                        buttons[i].default_values()
                        break

        gui.render(screen)

        if not pause and not dilog_window:
            GAME.move_shape()
            text_score.update(str(SCORE))
            time.update(clock.get_time())

            if not GAME.get_speed()[0]:
                if int(N % GAME.get_speed()[1]) == 0:
                    GAME.update()

            else:
                GAME.update()

            if not GAME.get_info():
                game_file_functions.push_records(NAME, SCORE, time.get_time())
            N += 1

        elif pause:
            GAME.render(screen)
            text_pause_shape.render(screen)

        elif dilog_window:
            GAME.render(screen)
            pygame.draw.rect(screen, pygame.Color("black"), (75, 250, 475, 175))
            dilog.render(screen)
            all_sprites.draw(screen)
            for i in buttons:
                i.render(screen)

        pygame.display.flip()


while running:
    old_pixels, score, time = main()
    game(old_pixels, score, time)
