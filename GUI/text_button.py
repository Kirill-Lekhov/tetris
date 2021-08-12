from GUI.picture_button import PictureButton

from pygame.sprite import Group
from pygame.font import Font
from pygame import Color


class TextButton(PictureButton):
    def __init__(self, coord: tuple, button_group: Group, text: str, color):
        super().__init__(coord, button_group)

        self.text = text
        self.font = Font(None, self.rect.height - 15)
        self.font_color = Color(color)
        self.rendered_text = None
        self.rendered_rect = None

    def update(self, event) -> bool:
        update_result = super().update(event)
        return update_result

    def render(self, surface):
        button_pressed_offset = 0

        if not self.press:
            self.font = Font(None, self.rect.height - 15)

        else:
            button_pressed_offset = -5
            self.font = Font(None, self.rect.height - 20)

        self.rendered_text = self.font.render(self.text, 1, self.font_color)
        self.rendered_rect = self.rendered_text.get_rect(center=self.rect.center)
        self.rendered_rect.x += button_pressed_offset
        self.rendered_rect.y += button_pressed_offset

        surface.blit(self.rendered_text, self.rendered_rect)
