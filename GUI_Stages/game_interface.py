from pygame import Surface

from GUI_Stages.game import Game
from GUI_Stages.main_menu import MainMenu
from GUI_Stages.leaderboard import Leaderboard

from Tools.game_file_functions.records import push_records
from Tools.game_file_functions.save_game import save_game

from constants import OPEN_MAIN_MENU, OPEN_LEADERBOARD, OPEN_SAVED_GAME, OPEN_NEW_GAME, GAME_OVER, SENDING_DATA_TO_SAVE


class GameInterface:
    def __init__(self):
        self.stages = {"main_menu": MainMenu, "leaderboard": Leaderboard, "game": Game}
        self.current_stage = self.stages["main_menu"]()
        self.player_nickname = self.current_stage.get_player_nickname()

    def update(self, pygame, event):
        self.current_stage.update(pygame, event)

        if event.type == OPEN_MAIN_MENU:
            self.current_stage = self.stages["main_menu"]()

        if event.type == OPEN_LEADERBOARD:
            self.player_nickname = self.current_stage.get_player_nickname()
            self.current_stage = self.stages["leaderboard"]()

        if event.type == OPEN_NEW_GAME:
            self.player_nickname = self.current_stage.get_player_nickname()
            self.current_stage = self.stages["game"](None, 0)

        if event.type == OPEN_SAVED_GAME:
            self.player_nickname = self.current_stage.get_player_nickname()
            self.current_stage = self.stages["game"](event.time, event.score)

        if event.type == SENDING_DATA_TO_SAVE:
            save_game(event.static_pixels, event.score, self.current_stage.get_game_time())
            self.current_stage = self.stages["main_menu"](self.player_nickname)

        if event.type == GAME_OVER:
            push_records(self.player_nickname, event.score, self.current_stage.get_game_time())
            self.current_stage = self.stages["main_menu"](self.player_nickname)

    def update_without_event(self, *args):
        self.current_stage.update_without_event(*args)

    def draw(self, surface: Surface):
        self.current_stage.draw(surface)

    def get_player_nickname(self) -> str:
        return self.player_nickname
