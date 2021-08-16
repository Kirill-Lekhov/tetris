from GUI_Parts.label import Label

from pygame import KEYDOWN, K_KP_ENTER, K_RETURN, K_BACKSPACE, MOUSEBUTTONDOWN
from pygame.time import get_ticks
from pygame import draw, Color


class TextBox:
    def __init__(self, rect, text):
        self.label = Label(rect, text, 'white', -1)
        self.focus = True
        self.blink = True
        self.blink_timer = 0

    def update(self, event):
        if event.type == KEYDOWN and self.focus:
            if event.key in (K_KP_ENTER, K_RETURN):
                self.focus = False

            elif event.key == K_BACKSPACE:
                if len(self.label.text) > 0:
                    self.label.text = self.label.text[:-1]

            else:
                if len(self.label.text) + 1 != 13:
                    self.label.text += event.unicode

        elif event.type == MOUSEBUTTONDOWN and event.button == 1:
            self.focus = self.label.rendering_place.collidepoint(event.pos)

    def update_without_event(self):
        if get_ticks() - self.blink_timer > 200:
            self.blink = not self.blink
            self.blink_timer = get_ticks()

    def render(self, surface):
        self.label.render(surface)

        if self.focus and self.blink:
            draw.line(surface, Color("black"), (self.label.rendered_rect.right + 2, self.label.rendered_rect.top + 2),
                      (self.label.rendered_rect.right + 2, self.label.rendered_rect.bottom - 2))

    def get_text(self) -> str:
        return self.label.text
