from pygame import Color, Rect
from pygame.font import Font

from Tools.color_parser import parse_color


class Label:
    def __init__(self, rendering_place, text, color=Color("grey"), bgcolor=Color("white")):
        self.rendering_place = Rect(rendering_place)
        self.text = text
        self.fill_background = (bgcolor == -1)

        self.bgcolor = parse_color(bgcolor, self.fill_background)
        self.font_color = parse_color(color, False)

        self.font = Font(None, self.rendering_place.height - 4)
        self.rendered_text = None
        self.rendered_rect = None

    def render(self, surface):
        if not self.fill_background:
            surface.fill(self.bgcolor, self.rendering_place)

        self.rendered_text = self.font.render(self.text, 1, self.font_color)
        self.rendered_rect = self.rendered_text.get_rect(x=self.rendering_place.x + 2,
                                                         centery=self.rendering_place.centery)
        surface.blit(self.rendered_text, self.rendered_rect)

    def update(self, new_text: str = None):
        if new_text is not None:
            self.text = new_text
