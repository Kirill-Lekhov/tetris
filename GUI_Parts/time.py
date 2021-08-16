from GUI_Parts.label import Label

from pygame import Color


class Time:
    def __init__(self, rect, color=Color("white"), bgcolor=Color("black"), last_values=None):
        self.time = self._set_last_time(last_values)
        self.label = Label(rect, self.convert_time_to_text(), color, bgcolor)

    def convert_time_to_text(self):
        return f'{self.time["h"]}:{self.time["m"]}:{self.time["s"]}'

    def update(self, ms):
        self.time['ms'] += ms

        if self.time['ms'] >= 1000:
            self.time['s'] += 1
            self.time['ms'] = 0

        if self.time['s'] == 60:
            self.time['m'] += 1
            self.time['s'] = 0

        if self.time['m'] == 60:
            self.time['h'] += 1
            self.time['m'] = 0

        self.label.update(self.convert_time_to_text())

    def render(self, surface):
        self.label.render(surface)

    def get_time(self):
        return self.convert_time_to_text()

    @staticmethod
    def _set_last_time(last_values):
        if last_values is None:
            return {'h': 0, 'm': 0, 's': 0, 'ms': 0}

        return {'h': last_values[0], 'm': last_values[1], 's': last_values[2], 'ms': 0}
