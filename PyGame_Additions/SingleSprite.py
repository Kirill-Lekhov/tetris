from pygame.sprite import GroupSingle, Sprite

from Tools.load_image import load_image


class SingleSprite(Sprite):
    def __init__(self, image_path: str, coord=None):
        super().__init__()

        self._sprite_group = GroupSingle(self)
        self.image = load_image(image_path)
        self.rect = self.image.get_rect()
        self._sprite_group.add(self)

        if coord is not None:
            self.rect.x, self.rect.y = coord

    def draw(self, surface):
        self._sprite_group.draw(surface)
