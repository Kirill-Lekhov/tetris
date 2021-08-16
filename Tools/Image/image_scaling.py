from pygame.transform import scale
from pygame import Color, Surface


def scale_image(source_button_image, scale_value=10) -> Surface:
    pressed_button_size = tuple(map(lambda x: x - scale_value, source_button_image.get_size()))
    pressed_button_image = Surface(pressed_button_size).convert_alpha()

    colorkey = Color(*source_button_image.get_colorkey())
    scale(source_button_image, pressed_button_size, pressed_button_image)
    pressed_button_image.set_colorkey(colorkey)

    return pressed_button_image
