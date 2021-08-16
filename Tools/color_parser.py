from pygame import Color


def parse_color(bgcolor, fill_background):
    if fill_background:
        return Color(0, 0, 0)

    else:
        if isinstance(bgcolor, Color):
            return bgcolor

        else:
            if isinstance(bgcolor, str):
                return Color(bgcolor)

            else:
                return Color(*bgcolor)
