from pygame import Color, Surface
from pygame.draw import rect

from GUI_Parts.label import Label
from GUI_Parts.text_button import TextButton
from PyGame_Additions.GroupWithRender import GroupWithRender


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
