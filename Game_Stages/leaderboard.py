from Tools.game_file_functions import load_records
from GUI.picture_button import BackButton
from GUI.label import Label
from Tools.os_tools import terminate

from constants import SCREEN_SIZE

import pygame


def leaderboard(game_pygame, screen, fon_picture):
    leaderboard_is_running = True
    leaderboard_screen = pygame.Surface(SCREEN_SIZE)

    logo = Label((190, 100, 100, 70), 'РЕКОРДЫ', 'white', -1)
    records_table = load_records_table()

    back_button = pygame.sprite.Group()
    back_button.empty()
    button = BackButton((50, 50), back_button)
    back_button.add(button)

    while leaderboard_is_running:
        fon_picture.draw(leaderboard_screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            if button.update(event):
                leaderboard_is_running = False

        back_button.draw(leaderboard_screen)
        logo.render(leaderboard_screen)

        for i in records_table:
            i.render(leaderboard_screen)

        screen.blit(leaderboard_screen, (0, 0, *SCREEN_SIZE))
        game_pygame.display.flip()


def load_records_table() -> list:
    records = load_records()
    records_table = []

    for record_index, record in enumerate(records):
        records_table.append(Label((100, 170 + record_index * 50, 100, 50), record, 'white', -1))

    return records_table
