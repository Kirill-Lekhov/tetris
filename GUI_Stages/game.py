from pygame import Surface, KEYDOWN, KEYUP, K_ESCAPE, K_p, K_PAUSE
from pygame.event import Event

from GUI_Parts.label import Label
from GUI_Parts.time import Time
from GUI_Parts.MessageBox import MessageBox

from game_events import PAUSING_GAME, RESUMING_GAME, EXIT_TO_MAIN_MENU, UPDATE_SCORE


class Game:
    def __init__(self, start_time, start_score):
        self.message_box = MessageBox("Вы уверены что хотите выйти?", ["Да", "Нет"], (75, 250, 475, 175))
        self.time = Time((450, 400, 150, 50), 'white', -1, start_time)
        self.pause_label = Label((80, 200, 200, 200), "ПАУЗА", "blue", -1)
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

    def update(self, pygame, event):
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            self.show_message_box = True

        if event.type == KEYUP and (event.key == K_p or event.key == K_PAUSE):
            self.show_pause = not self.show_pause

        if event.type == UPDATE_SCORE:
            self.score_label.update(str(event.score))

        if self.show_message_box:
            update_result = self.message_box.update(event)

            if update_result == 1:
                pygame.event.post(Event(EXIT_TO_MAIN_MENU))

            elif update_result == 2:
                self.show_message_box = False

        if self.update_pause_state():
            if self.game_has_been_paused:
                pygame.event.post(Event(PAUSING_GAME))

            else:
                pygame.event.post(Event(RESUMING_GAME))

    def update_without_event(self, clock):
        if not self.game_has_been_paused:
            self.time.update(clock.get_time())

    def load_labels(self):
        self.labels.append(Label((400, 75, 150, 65), "Счет:", "White", -1))
        self.labels.append(Label((400, 220, 150, 30), "Следующая фигура", "White", -1))
        self.labels.append(Label((400, 365, 150, 50), "Время:", "white", -1))
        self.labels.append(Label((390, 450, 25, 25), "P/Pause:Пауза", "white", -1))
        self.labels.append(Label((390, 475, 25, 25), "Esc:Выход", "white", -1))
        self.labels.append(Label((390, 500, 25, 25), "Влево/вправо: Перемещение", "white", -1))
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

    def get_game_time(self) -> str:
        return self.time.get_time()
