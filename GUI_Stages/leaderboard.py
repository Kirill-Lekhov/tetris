from pygame import Surface
from pygame.sprite import Group

from GUI_Parts.label import Label
from GUI_Parts.picture_button import BackButton

from Tools.game_file_functions.records import load_records


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

    def update_without_event(self, *args):
        pass

    @staticmethod
    def load_records_table() -> list:
        records = load_records()
        records_table = []

        for record_index, record in enumerate(records):
            records_table.append(Label((100, 170 + record_index * 50, 100, 50), record, 'white', -1))

        return records_table
