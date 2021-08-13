from GUI_Parts.label import Label

from pygame import KEYDOWN, K_KP_ENTER, K_RETURN, K_BACKSPACE, MOUSEBUTTONDOWN
from pygame.time import get_ticks
from pygame import draw, Color


class TextBox(Label):
    # TODO: Update TextBox

    def __init__(self, rect, text):
        super().__init__(rect, text, 'white', -1)
        self.focus = True
        self.blink = True
        self.blink_timer = 0

    def get_event(self, event):
        if event.type == KEYDOWN and self.focus:
            if event.key in (K_KP_ENTER, K_RETURN):
                self.focus = False

            elif event.key == K_BACKSPACE:
                if len(self.text) > 0:
                    self.text = self.text[:-1]

            else:
                if len(self.text) + 1 != 13:
                    self.text += event.unicode

        elif event.type == MOUSEBUTTONDOWN and event.button == 1:
            self.focus = self.rendering_place.collidepoint(event.pos)

    def update(self, new_text: str = None):
        # TODO: Add event processing here & delete get_event method

        super().update(new_text)

        if get_ticks() - self.blink_timer > 200:
            self.blink = not self.blink
            self.blink_timer = get_ticks()

    def render(self, surface):
        super(TextBox, self).render(surface)

        if self.focus and self.blink:
            draw.line(surface, Color("black"), (self.rendered_rect.right + 2, self.rendered_rect.top + 2),
                      (self.rendered_rect.right + 2, self.rendered_rect.bottom - 2))

    def get_text(self) -> str:
        return self.text
