from os.path import join as os_join
from pygame.image import load
from pygame import error
from pygame import Surface


def load_image(name: str, colorkey=None) -> Surface:
    fullname = os_join('data', name)

    try:
        image = load(fullname)

    except error as message:
        print('Cannot load image:', name)

        raise SystemExit(message)

    image = image.convert_alpha()

    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))

        image.set_colorkey(colorkey)

    return image
