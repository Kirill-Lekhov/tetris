from Game_Parts.board import Board
from Game_Parts.shape import Shape
from Game_Parts.pixel import Pixel
from GUI_Parts.show_next_shape import ShowNextShape

from random import choice
from pygame import Color

from constants import SHAPE, REWARD

from pygame import Surface
from pygame.key import get_pressed
from pygame import KEYUP, K_UP


class GameBoard(Board):
    def __init__(self):
        super().__init__()
        self.play_game = False
        self.game_paused = False
        self.pixels = []
        self.current_shape = Shape(choice(SHAPE))
        self.next_shape = Shape(choice(SHAPE))
        self.static_pixels = []

        self.move_shape_ticks = 0
        self.shape_drop_ticks = 0

        # TODO: Rework this calls
        self.update_current_shape()
        self.next_shape_render = ShowNextShape(250, 405, self.next_shape.get_shape_pixels_coord(),
                                               self.next_shape.get_color())

        self.score = 0

    def update(self, event, *args):
        if self.play_game and not self.game_paused:
            if event.type == KEYUP and event.key == K_UP:
                self.current_shape.rotate(self.board)

    def update_without_event(self, *args):
        game_ticks = args[0]

        if self.play_game and not self.game_paused:
            self.clear_game_board()
            self.draw_static_pixels_on_board()

            pressed_keys = list(get_pressed())

            if game_ticks - self.move_shape_ticks > 90:
                self.current_shape.move_to_side(self.board, pressed_keys[79] - pressed_keys[80])
                self.move_shape_ticks = game_ticks

            if pressed_keys[81]:
                self.current_shape.lower_it_down(self.board)
                pass

            if game_ticks - self.shape_drop_ticks > 500:
                self.current_shape.lower_it_down(self.board)
                self.shape_drop_ticks = game_ticks

            self.update_current_shape()
            self.delete_lines()

            if not self.current_shape.get_moving_status():
                self.update_shapes()

    def clear_game_board(self):
        self.create_board()
        self.create_stop_line()

    def draw(self, surface: Surface):
        if self.play_game:
            self.draw_shape_on_board()
            self.render(surface, True)
            self.next_shape_render.render(surface, True)

    def play(self):
        self.play_game = not self.play_game

    def game_pause(self):
        self.game_paused = not self.game_paused

    def update_current_shape(self):
        self.pixels = self.current_shape.get_pixels()

    def draw_shape_on_board(self):
        for pixel in self.pixels:
            x, y = pixel.get_coord()
            color = pixel.get_color()
            self.board[y][x] = (1, Color(color))

    def draw_static_pixels_on_board(self):
        for pixel in self.static_pixels:
            x, y = pixel.get_coord()
            color = pixel.get_color()
            self.board[y][x] = (1, Color(color))

    def update_shapes(self):
        self.static_pixels.extend(self.current_shape.get_pixels())
        self.current_shape = self.next_shape
        self.pixels = self.current_shape.get_pixels()
        self.next_shape = Shape(choice(SHAPE))
        self.update_current_shape()
        self.next_shape_render.update(self.next_shape.get_shape_pixels_coord(), self.next_shape.get_color())

    def delete_lines(self):
        lines_number = 0
        lines_for_deleting = []
        old_static_pixels = self.static_pixels.copy()
        self.static_pixels = []

        for board_line in self.board[:-1]:
            if all(map(lambda pixel: pixel[0] and (not Color("black") == pixel[1]), board_line)):
                lines_number += 1
                lines_for_deleting.append(self.board.index(board_line))

        for old_pixel in old_static_pixels:
            if not (old_pixel.get_coord()[1] in lines_for_deleting):
                self.static_pixels.append(old_pixel)

        self.pull_down_pixels(lines_number, lines_for_deleting)

        if lines_number:
            self.score += REWARD[lines_number]

    def pull_down_pixels(self, empty_lines_number: int, empty_lines: list):
        for line in range(empty_lines_number):
            self.pull_down_static_pixels(empty_lines[line])

    def pull_down_static_pixels(self, stop_line: int):
        # TODO: Rename this method

        for pixel in sorted(self.static_pixels, key=lambda item: item.get_coord()[1]):
            x, y = pixel.get_coord()

            if y < stop_line:
                pixel.move((x, y+1))

    def load_game(self, score, static_pixels):
        for pixel_coord, color in static_pixels:
            self.static_pixels.append(Pixel(pixel_coord, color))

        self.score = score

    def get_score(self) -> int:
        return self.score

