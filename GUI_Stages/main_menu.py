from pygame import Surface
from pygame.event import Event

from GUI_Parts.text_box import TextBox
from GUI_Parts.text_button import TextButton
from GUI_Parts.label import Label

from PyGame_Additions.SingleSprite import SingleSprite
from PyGame_Additions.GroupWithRender import GroupWithRender

from constants import DEFAULT_NAME
from constants import OPEN_NEW_GAME, OPEN_SAVED_GAME, OPEN_LEADERBOARD

from Tools.game_file_functions.load_game import check_save_file, load_game


class MainMenu:
    def __init__(self, player_nickname=DEFAULT_NAME):
        self.nickname_enter = TextBox((160, 600, 135, 50), player_nickname)
        self.game_logo = SingleSprite("logo.png", (60, 100))
        self.player_label = Label((50, 600, 50, 50), 'Игрок: ', 'white', -1)

        self.there_is_an_old_save = check_save_file()

        self.buttons = GroupWithRender()
        self.load_buttons()

    def draw(self, surface: Surface):
        self.game_logo.draw(surface)
        self.nickname_enter.render(surface)
        self.player_label.render(surface)
        self.buttons.draw(surface)
        self.buttons.render(surface)

    def update(self, pygame, event):
        self.nickname_enter.update(event)

        buttons = self.buttons.sprites()

        for button_number, button in enumerate(buttons):
            if button.update(event):
                if button_number == 0:
                    pygame.event.post(Event(OPEN_NEW_GAME))

                elif button_number == 1 and self.there_is_an_old_save:
                    pixels, score, time = load_game()
                    pygame.event.post(Event(OPEN_SAVED_GAME, {"pixels": pixels, "score": int(score), "time": time}))

                else:
                    pygame.event.post(Event(OPEN_LEADERBOARD))

    def update_without_event(self, *args):
        self.nickname_enter.update_without_event()

    def load_buttons(self):
        button_positions = [(185, 270), (185, 340), (185, 410)]
        button_names = ["Новая игра", "Продолжить", "Рекорды"]

        if not self.there_is_an_old_save:
            del button_names[1]

        for button_number, button_name in enumerate(button_names):
            TextButton(button_positions[button_number], self.buttons, button_name, "white")

    def get_player_nickname(self) -> str:
        return self.nickname_enter.get_text()
