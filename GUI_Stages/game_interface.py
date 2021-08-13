from pygame import Surface

from GUI_Stages.game import Game
from GUI_Stages.main_menu import MainMenu
from GUI_Stages.leaderboard import Leaderboard

from constants import DEFAULT_NAME


class GameInterface:
    def __init__(self, player_nickname=DEFAULT_NAME):
        self.stages = {"main_menu": MainMenu, "leaderboard": Leaderboard, "game": Game}
        self.current_stage = self.stages["main_menu"](player_nickname)

        self.player_nickname = player_nickname

    def update(self, event, *args) -> int:
        update_result = self.current_stage.update(event)

        if isinstance(self.current_stage, MainMenu):
            if update_result == 1:
                # TODO: Cleaning old stage
                self.player_nickname = self.current_stage.get_player_nickname()
                self.current_stage = self.stages["game"](None, 0)
                return 0

            if update_result == 3:
                # TODO: Cleaning old stage
                self.player_nickname = self.current_stage.get_player_nickname()
                self.current_stage = self.stages["leaderboard"]()

        elif isinstance(self.current_stage, Leaderboard):
            if update_result:
                # TODO: Cleaning old stage
                self.current_stage = self.stages["main_menu"](self.player_nickname)

        elif isinstance(self.current_stage, Game):
            if update_result == 1:
                return 2    # stop/resume this game

            elif update_result == 2:
                # TODO: Cleaning old stage
                self.current_stage = self.stages["main_menu"](self.player_nickname)
                return 1

    def update_without_event(self, *args):
        self.current_stage.update_without_event(*args)

    def draw(self, surface: Surface):
        self.current_stage.draw(surface)

    def get_player_nickname(self) -> str:
        return self.player_nickname
