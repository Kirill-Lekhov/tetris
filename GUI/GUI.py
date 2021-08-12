from pygame import Surface


class GUI:
    def __init__(self):
        self.elements = []
        self.first_draw_elements = []

    def add_element(self, *elements):
        for element in elements:
            self.first_draw_elements.append(element)

    def add_first_draw_element(self, *elements):
        for element in elements:
            self.first_draw_elements.append(element)

    def render(self, surface: Surface, render_first_elements: bool = False):
        if render_first_elements:
            elements_for_rendering = self.first_draw_elements

        else:
            elements_for_rendering = self.elements

        for element in elements_for_rendering:
            if self.check_method(element, "draw"):
                element.draw(surface)

            if self.check_method(element, "render"):
                element.render(surface)

    def clear(self):
        self.first_draw_elements.clear()
        self.elements.clear()

    @staticmethod
    def check_method(element, desired_method) -> bool:
        return callable(getattr(element, desired_method, None))
