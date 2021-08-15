from Game_Parts.pixel import Pixel


def load_game(save_path: str = "data/save.tsv") -> tuple:
    with open(save_path, encoding="utf-8", mode='r') as f:
        save_lines = [line.strip() for line in f.readlines()]

        score_from_save = int(save_lines[0])
        time_from_save = list(map(int, save_lines[1].split(':')))
        lines_from_save = [split_save_line(line) for line in save_lines[2:]]
        pixels_from_save = [create_pixel_from_line(line) for line in lines_from_save]

    return pixels_from_save, score_from_save, time_from_save


def split_save_line(save_line: str) -> list:
    return clean_save_line(save_line).split(', ')


def clean_save_line(save_line: str) -> str:
    return save_line.strip().strip('(').strip(')')


def create_pixel_from_line(save_line: list) -> Pixel:
    return Pixel((int(save_line[1]), int(save_line[0])), save_line[2])


def check_save_file(save_path: str = "data/save.tsv") -> bool:
    with open(save_path, encoding="utf-8", mode='r') as f:
        return bool(f.readlines())
