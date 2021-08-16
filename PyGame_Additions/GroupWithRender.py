from pygame.sprite import Group
from pygame import Surface


class GroupWithRender(Group):
    def __init__(self, *sprites):
        super().__init__(sprites)

    def draw(self, surface: Surface) -> None:
        super().draw(surface)

    def render(self, surface: Surface) -> None:
        sprites = list(filter(self.check_render_method, self.sprites()))

        for sprite in sprites:
            sprite.render(surface)

    @staticmethod
    def check_render_method(sprite):
        return callable(getattr(sprite, "render", None))
