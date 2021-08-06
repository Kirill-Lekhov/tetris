from pygame.sprite import Sprite, Group
from pygame import MOUSEBUTTONDOWN
from Tools.load_image import load_image


# TODO: Inherit from PictureButton


class BackButton(Sprite):
    def __init__(self, coord: tuple, group: Group):
        super().__init__(group)
        self.press = self.last_pressed = False

        self.button_image = load_image('back.png')
        self.pressed_button_image = load_image('back_pressed.png')
        self.image = self.button_image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, self.y = coord

    def update(self, event):
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            self.press = self.last_pressed = self.rect.collidepoint(event.pos)
            self.image = self.pressed_button_image
            self.rect.x, self.rect.y = self.x + 5, self.y + 5

        else:
            self.press = False
            self.image = self.button_image
            self.rect.x, self.rect.y = self.x, self.y

        return self.press != self.last_pressed

    def default_values(self):
        self.press = False
        self.last_pressed = False
