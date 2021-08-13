from pygame import Surface

from constants import DEFAULT_NAME
from GUI.text_box import TextBox
from PyGame_Additions.SingleSprite import SingleSprite
from PyGame_Additions.GroupWithRender import GroupWithRender
from GUI.label import Label
from GUI.text_button import TextButton


from GUI.picture_button import BackButton
from pygame.sprite import Group
from Tools.game_file_functions.records import load_records


from pygame.draw import rect
from pygame import Color
from GUI.time import Time

from pygame import KEYDOWN, KEYUP, K_ESCAPE, K_p, K_PAUSE


class GameInterface:
    def __init__(self, start_stage="main_menu", *stage_args):
        self.stages = {"main_menu": MainMenu, "leaderboard": Leaderboard, "game": Game}
        self.current_stage = self.stages[start_stage](*stage_args)

        # TODO: delete this variables
        self.start_stage_args = stage_args

    def update(self, event, *args):
        update_result = self.current_stage.update(event)

        if isinstance(self.current_stage, MainMenu):
            if update_result == 1:
                # TODO: Cleaning old stage
                self.current_stage = self.stages["game"](None, 0)

            if update_result == 3:
                # TODO: Cleaning old stage
                self.current_stage = self.stages["leaderboard"]()

        elif isinstance(self.current_stage, Leaderboard):
            if update_result:
                # TODO: Cleaning old stage
                self.current_stage = self.stages["main_menu"](*args)

        elif isinstance(self.current_stage, Game):
            if update_result == 1:
                # game paused
                pass

            elif update_result == 2:
                # TODO: Cleaning old stage
                self.current_stage = self.stages["main_menu"](*args)

    def update_without_event(self):
        self.current_stage.update_without_event()

    def draw(self, surface: Surface):
        self.current_stage.draw(surface)


class MainMenu:
    def __init__(self, there_is_an_old_save=False):
        self.nickname_enter = TextBox((160, 600, 135, 50), DEFAULT_NAME)
        self.game_logo = SingleSprite("logo.png", (60, 100))
        self.player_label = Label((50, 600, 50, 50), 'Игрок: ', 'white', -1)
        self.there_is_an_old_save = there_is_an_old_save

        self.buttons = GroupWithRender()
        self.load_buttons()

    def draw(self, surface: Surface):
        self.game_logo.draw(surface)

        self.nickname_enter.render(surface)
        self.player_label.render(surface)
        self.buttons.draw(surface)
        self.buttons.render(surface)

    def update(self, event):
        self.nickname_enter.get_event(event)

        buttons = self.buttons.sprites()

        for button_number, button in enumerate(buttons):
            if button.update(event):
                if button_number == 0:
                    return 1

                elif button_number == 1 and self.there_is_an_old_save:
                    return 2

                else:
                    return 3

    def update_without_event(self):
        self.nickname_enter.update()

    def load_buttons(self):
        button_positions = [(185, 270), (185, 340), (185, 410)]
        button_names = ["Новая игра", "Продолжить", "Рекорды"]

        if not self.there_is_an_old_save:
            del button_names[1]

        for button_number, button_name in enumerate(button_names):
            TextButton(button_positions[button_number], self.buttons, button_name, "white")


class Leaderboard:
    def __init__(self):
        self.records_label = Label((190, 100, 100, 70), 'РЕКОРДЫ', 'white', -1)
        self.records_table = self.load_records_table()
        self.buttons = Group()
        self.back_button = BackButton((50, 50), self.buttons)

    def draw(self, surface: Surface):
        self.records_label.render(surface)
        self.buttons.draw(surface)

        for records_line in self.records_table:
            records_line.render(surface)

    def update(self, event) -> bool:
        return self.back_button.update(event)

    def update_without_event(self):
        pass

    @staticmethod
    def load_records_table() -> list:
        records = load_records()
        records_table = []

        for record_index, record in enumerate(records):
            records_table.append(Label((100, 170 + record_index * 50, 100, 50), record, 'white', -1))

        return records_table


class Game:
    def __init__(self, start_time, start_score):
        self.message_box = MessageBox("Вы уверены что хотите выйти?", ["Да", "Нет"], (75, 250, 475, 175))
        self.time = Time((450, 400, 150, 50), 'white', -1, start_time)
        self.pause_label = Label((80, 200, 200, 200), "PAUSE", "blue", -1)
        self.score_label = Label((400, 135, 150, 50), str(start_score), "White", -1)
        self.labels = []
        self.load_labels()

        self.game_paused = False
        self.show_pause = False
        self.show_message_box = False

    def draw(self, surface: Surface):
        self.time.render(surface)
        self.score_label.render(surface)

        for label in self.labels:
            label.render(surface)

        if self.show_pause:
            self.pause_label.render(surface)

        if self.show_message_box:
            self.message_box.draw(surface)

    def update(self, event) -> int:
        status_changed = 0
        # status 1 - game not/paused
        # status 2 - exit the game

        if event.type == KEYDOWN and event.key == K_ESCAPE:
            self.show_message_box = True

        if event.type == KEYUP and (event.key == K_p or event.key == K_PAUSE):
            self.show_pause = not self.show_pause

        if self.show_message_box:
            update_result = self.message_box.update(event)

            if update_result == 1:
                status_changed = 2

            elif update_result == 2:
                self.show_message_box = False

        return status_changed

    def update_without_event(self):
        pass

    def load_labels(self):
        self.labels.append(Label((400, 75, 150, 65), "Score:", "White", -1))
        self.labels.append(Label((400, 200, 150, 50), "Next Shape", "White", -1))
        self.labels.append(Label((400, 365, 150, 50), "Time:", "white", -1))
        self.labels.append(Label((390, 450, 25, 25), "P:Пауза", "white", -1))
        self.labels.append(Label((390, 475, 25, 25), "Esc:Выход", "white", -1))
        self.labels.append(Label((390, 500, 25, 25), "Влево\вправо: Перемещение", "white", -1))
        self.labels.append(Label((390, 525, 25, 25), "Вверх: Поворот", "white", -1))
        self.labels.append(Label((390, 550, 25, 25), "Вниз: Ускорить падение", "white", -1))


class MessageBox:
    def __init__(self, label_text, buttons_text, message_box_size, background_color=Color("black")):
        self.label = Label((90, 275, 45, 45), label_text, "white", -1)
        self.buttons = GroupWithRender()
        self.load_buttons(buttons_text)

        self.message_box_size = message_box_size
        self.color = background_color

    def draw(self, surface: Surface):
        rect(surface, self.color, self.message_box_size)
        self.label.render(surface)
        self.buttons.draw(surface)
        self.buttons.render(surface)

    def update(self, event):
        buttons = self.buttons.sprites()

        for button_number, button in enumerate(buttons):
            if button.update(event):
                if button_number == 0:
                    return 1

                elif button_number == 1:
                    return 2

    def update_without_event(self):
        pass

    def load_buttons(self, buttons_text):
        button_positions = [(100, 340), (325, 340)]
        button_names = buttons_text

        for button_number, button_name in enumerate(button_names):
            TextButton(button_positions[button_number], self.buttons, button_name, "white")
