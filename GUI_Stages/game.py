from pygame import Surface
from pygame import KEYDOWN, KEYUP, K_ESCAPE, K_p, K_PAUSE

from GUI_Parts.label import Label
from GUI_Parts.time import Time
from GUI_Parts.MessageBox import MessageBox


class Game:
    def __init__(self, start_time, start_score):
        self.message_box = MessageBox("Вы уверены что хотите выйти?", ["Да", "Нет"], (75, 250, 475, 175))
        self.time = Time((450, 400, 150, 50), 'white', -1, start_time)
        self.pause_label = Label((80, 200, 200, 200), "PAUSE", "blue", -1)
        self.score_label = Label((400, 135, 150, 50), str(start_score), "White", -1)
        self.labels = []
        self.load_labels()

        self.game_has_been_paused = False
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

        if self.update_pause_state():
            status_changed = 1

        return status_changed

    def update_without_event(self, clock, new_score: int):
        if not self.game_has_been_paused:
            self.time.update(clock.get_time())

            if new_score:
                self.score_label.update(str(new_score))

    def load_labels(self):
        self.labels.append(Label((400, 75, 150, 65), "Score:", "White", -1))
        self.labels.append(Label((400, 200, 150, 50), "Next Shape", "White", -1))
        self.labels.append(Label((400, 365, 150, 50), "Time:", "white", -1))
        self.labels.append(Label((390, 450, 25, 25), "P:Пауза", "white", -1))
        self.labels.append(Label((390, 475, 25, 25), "Esc:Выход", "white", -1))
        self.labels.append(Label((390, 500, 25, 25), "Влево\вправо: Перемещение", "white", -1))
        self.labels.append(Label((390, 525, 25, 25), "Вверх: Поворот", "white", -1))
        self.labels.append(Label((390, 550, 25, 25), "Вниз: Ускорить падение", "white", -1))

    def update_pause_state(self) -> bool:
        if (self.show_pause or self.show_message_box) and not self.game_has_been_paused:
            self.game_has_been_paused = True
            return True

        if (not self.show_pause) and (not self.show_message_box) and self.game_has_been_paused:
            self.game_has_been_paused = False
            return True

        return False
