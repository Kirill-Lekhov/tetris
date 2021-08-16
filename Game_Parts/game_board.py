from Game_Parts.board import Board
from Game_Parts.shape import Shape
from GUI_Parts.show_next_shape import ShowNextShape

from random import choice
from pygame import Color, Surface, KEYUP, K_UP
from pygame.key import get_pressed
from pygame.event import Event

from constants import SHAPE, REWARD
from constants import OPEN_NEW_GAME, OPEN_SAVED_GAME, PAUSING_GAME, RESUMING_GAME, PLAY_SCORE_SOUND, GAME_OVER, \
    EXIT_TO_MAIN_MENU, SENDING_DATA_TO_SAVE, UPDATE_SCORE


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

        self.update_current_shape()
        self.next_shape_render = ShowNextShape(250, 405, self.next_shape.get_shape_pixels_coord(),
                                               self.next_shape.get_color())

        self.score = 0

    def update(self, pygame, event):
        if event.type == OPEN_NEW_GAME:
            self.play_game = True
            self.load_new_game()

        if event.type == OPEN_SAVED_GAME:
            self.play_game = True
            self.load_game(event.score, event.pixels)

        if event.type == EXIT_TO_MAIN_MENU:
            self.play_game = False
            self.game_paused = False
            pygame.event.post(Event(SENDING_DATA_TO_SAVE, {"static_pixels": self.static_pixels, "score": self.score}))

        if event.type == PAUSING_GAME:
            self.game_paused = True

        if event.type == RESUMING_GAME:
            self.game_paused = False

        if self.play_game and not self.game_paused:
            if event.type == KEYUP and event.key == K_UP:
                self.current_shape.rotate(self.board)

    def update_without_event(self, pygame, *args):
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

            if self.delete_lines():
                pygame.event.post(Event(PLAY_SCORE_SOUND))
                pygame.event.post(Event(UPDATE_SCORE, {"score": self.score}))

            if not self.current_shape.get_moving_status():
                self.update_shapes()
                self.current_shape.can_it_go_down(self.board)

                if not self.current_shape.its_moving:
                    self.play_game = False
                    pygame.event.post(Event(GAME_OVER, {"score": self.score}))

    def clear_game_board(self):
        self.create_board()
        self.create_stop_line()

    def draw(self, surface: Surface):
        if self.play_game:
            self.draw_shape_on_board()
            self.render(surface, True)
            self.next_shape_render.render(surface, True)

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

    def delete_lines(self) -> int:
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

        self.pull_down_pixels(lines_for_deleting)

        if lines_number:
            self.score += REWARD[lines_number]

        return lines_number

    def pull_down_pixels(self, lines_for_deleting: list):
        for line_number, line in enumerate(lines_for_deleting):
            for pixel in sorted(self.static_pixels, key=lambda item: item.get_coord()[1]):
                x, y = pixel.get_coord()

                if y < line:
                    pixel.move((x, y + 1))

    def load_game(self, score, static_pixels):
        self.static_pixels.clear()

        for pixel in static_pixels:
            self.static_pixels.append(pixel)

        self.score = score

    def load_new_game(self):
        self.next_shape = Shape(choice(SHAPE))
        self.update_shapes()
        self.load_game(0, [])

    def get_score(self) -> int:
        return self.score

    def get_static_pixels(self) -> list:
        return self.static_pixels
