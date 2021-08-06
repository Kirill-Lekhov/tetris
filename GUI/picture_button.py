from pygame.sprite import Sprite, Group
from pygame.rect import Rect
from Tools.load_image import load_image


# TODO: Improve for versatility


class PictureButton(Sprite):
    def __init__(self, button_filename: str, coord: tuple, group: Group):
        super().__init__(group)
        self.press = False

        self.button_image = load_image(button_filename)
        self.pressed_button_image = load_image(pressed_button_filename(button_filename))
        self.image = self.button_image

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, self.y = coord

    def update(self, press: bool):
        self.press = press

        if not self.press:
            self.image = self.button_image
            self.rect.x, self.rect.y = self.x - 5, self.y - 5
            self.press = not self.press

        else:
            self.image = self.pressed_button_image
            self.rect.x, self.rect.y = self.x, self.y
            self.press = not self.press

    def get_rect(self) -> Rect:
        return self.rect


def pressed_button_filename(source_button_name: str) -> str:
    basic_name, expansion = source_button_name.split(".")[-2:]

    return f"{basic_name}_pressed.{expansion}"
