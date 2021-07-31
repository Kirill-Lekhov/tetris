def save_game(static_pixels, score: int, time: str, save_path: str = "data/save.tsv"):
    with open(save_path, encoding="utf-8", mode='a') as f:
        f.write(str(score)+'\n')
        f.write(time+'\n')
        f.write('\n'.join([create_save_line(static_pixels_line) for static_pixels_line in static_pixels]))


def create_save_line(static_pixels_line: list) -> str:
    return f"({', '.join(map(str, static_pixels_line[0]))}, {static_pixels_line[1]})"
