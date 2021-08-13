from pygame.sprite import Sprite, Group
from pygame.rect import Rect
from pygame import MOUSEBUTTONDOWN, MOUSEBUTTONUP
from Tools.load_image import load_image


class PictureButton(Sprite):
    def __init__(self, coord: tuple, button_group: Group, button_filename: str = "button.png"):
        super().__init__(button_group)
        self.press = self.last_pressed = False

        self.button_image = load_image(button_filename)
        self.pressed_button_image = load_image(pressed_button_filename(button_filename))
        self.image = self.button_image

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, self.y = coord

    def update(self, event) -> bool:
        returned_value = False

        if event.type == MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos):
            self.press = True
            self.image = self.pressed_button_image
            self.rect.x, self.rect.y = self.x + 5, self.y + 5

        if event.type == MOUSEBUTTONUP and event.button == 1 and self.press:
            self.press = False
            self.image = self.button_image
            self.rect.x, self.rect.y = self.x, self.y
            returned_value = True

        return returned_value

    def get_rect(self) -> Rect:
        return self.rect


class BackButton(PictureButton):
    def __init__(self, coord: tuple, button_group: Group):
        super().__init__(coord, button_group, "back.png")


def pressed_button_filename(source_button_name: str) -> str:
    basic_name, expansion = source_button_name.split(".")[-2:]

    return f"{basic_name}_pressed.{expansion}"
