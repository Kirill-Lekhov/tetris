def save_game(static_pixels, score: int, time: str, save_path: str = "data/save.tsv"):
    with open(save_path, encoding="utf-8", mode='w') as f:
        f.write(str(score)+'\n')
        f.write(time+'\n')
        f.write('\n'.join([create_save_line(static_pixel) for static_pixel in static_pixels]))


def create_save_line(static_pixel) -> str:
    return f"({', '.join(map(str, static_pixel.get_coord()))}, {static_pixel.get_color()})"


def save_empty_file(save_path: str = "data/save.tsv"):
    with open(save_path, encoding="utf-8", mode='w') as f:
        f.write("")
