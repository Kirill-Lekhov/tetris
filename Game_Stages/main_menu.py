from pygame.sprite import Group, Sprite

from Tools.load_image import load_image
from Interface import Label, TextBox
from GUI.text_button import TextButton
from Game_Stages.leaderboard import leaderboard
from Tools.os_tools import terminate
from Tools.game_file_functions.load_game import load_game


# TODO: Fix situation with closing program


def main_menu(game_pygame, screen, fon_picture, player_nickname):
    main_menu_is_running = True
    main_menu_buttons = Group()

    logo_picture = Group()
    logo = Sprite()
    logo.image = load_image('logo.png')
    logo.rect = logo.image.get_rect()
    logo.rect.x, logo.rect.y = 60, 100
    logo_picture.add(logo)

    text = Label((50, 600, 50, 50), 'Игрок: ', 'white', -1)
    name = TextBox((160, 600, 135, 50), player_nickname)

    old_pixels = None
    score = 0
    time = None

    there_is_an_old_save = bool(open('data/save.tsv', mode='r').readlines())

    if there_is_an_old_save:
        buttons = [TextButton((185, 270), main_menu_buttons, "Новая Игра", 'white'),
                   TextButton((185, 340), main_menu_buttons, "Продолжить", 'white'),
                   TextButton((185, 410), main_menu_buttons, "Рекорды", 'white')]
    else:
        buttons = [TextButton((185, 270), main_menu_buttons, "Новая Игра", 'white'),
                   TextButton((185, 340), main_menu_buttons, "Рекорды", 'white')]

    while main_menu_is_running:
        fon_picture.draw(screen)
        logo_picture.draw(screen)

        for event in game_pygame.event.get():
            if event.type == game_pygame.QUIT:
                terminate()

            name.get_event(event)

            for i in range(len(buttons)):
                if buttons[i].update(event):
                    if i == 0:
                        main_menu_is_running = False
                        main_menu_buttons.empty()
                        break

                    elif i == 1:
                        if there_is_an_old_save:
                            old_values = load_game()
                            old_pixels, score, time = old_values[0][:], old_values[1], old_values[2][:]
                            main_menu_is_running = False
                            break

                        leaderboard(game_pygame, screen, fon_picture)

                    elif i == 2:
                        leaderboard(game_pygame, screen, fon_picture)

        text.render(screen)
        name.render(screen)
        name.update()
        player_nickname = name.get_text()

        main_menu_buttons.draw(screen)

        for i in buttons:
            i.render(screen)

        game_pygame.display.flip()

    return old_pixels, score, time, player_nickname
