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


class GameInterface:
    def __init__(self, start_stage="main_menu", *stage_args):
        self.stages = {"main_menu": MainMenu, "leaderboard": Leaderboard}
        self.current_stage = self.stages[start_stage](*stage_args)

        # TODO: delete this variables
        self.start_stage_args = stage_args

    def update(self, event):
        update_result = self.current_stage.update(event)

        if isinstance(self.current_stage, MainMenu):
            if update_result == 3:
                # TODO: Cleaning old stage
                self.current_stage = self.stages["leaderboard"]()

        elif isinstance(self.current_stage, Leaderboard):
            if update_result:                # TODO: Cleaning old stage
                self.current_stage = self.stages["main_menu"](*self.start_stage_args)

    def update_without_event(self):
        self.current_stage.update_without_event()

    def draw(self, surface: Surface):
        self.current_stage.draw(surface)


class MainMenu:
    def __init__(self, there_is_an_old_save=False):
        super().__init__()

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

        for i in range(len(self.buttons)):
            if buttons[i].update(event):
                if i == 0:
                    return 1

                elif i == 1 and self.there_is_an_old_save:
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
