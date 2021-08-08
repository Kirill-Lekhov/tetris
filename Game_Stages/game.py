from Interface import Label, Time
from GUI.text_button import TextButton

from pygame.sprite import Group
from pygame import QUIT, K_UP, KEYUP, KEYDOWN, Color, K_DOWN, K_ESCAPE, K_p, K_PAUSE

from Tools.game_file_functions import save_game, push_records
from Tools.os_tools import terminate
from Game_Parts.game import Game
from Template import GUI


def game_stage(game_pygame, clock, music, screen, game_settings, fon_picture):
    old_pixels, score, time, player_nickname = game_settings

    #
    buttons = Group()
    #

    game_score = score
    gui = GUI()

    game = Game(screen, old_pixels)
    text_score_head = Label((400, 75, 150, 65), "Score:", "White", -1)
    text_score = Label((400, 135, 150, 50), str(game_score), "White", -1)
    text_next_shape = Label((400, 200, 150, 50), "Next Shape", "White", -1)
    text_pause_shape = Label((80, 200, 200, 200), "PAUSE", "blue", -1)
    text_time = Label((400, 365, 150, 50), "Time:", "white", -1)

    text_help_1 = Label((390, 450, 25, 25), "P:Пауза", "white", -1)
    text_help_2 = Label((390, 475, 25, 25), "Esc:Выход", "white", -1)
    text_help_3 = Label((390, 500, 25, 25), "Влево\вправо:Перемещение", "white", -1)
    text_help_4 = Label((390, 525, 25, 25), "Вверх:Поворот", "white", -1)
    text_help_5 = Label((390, 550, 25, 25), "Вниз:Ускорить падение", "white", -1)
    dilog = Label((90, 275, 45, 45), "Вы уверены что хотите выйти?", "white", -1)
    choice_buttons = [TextButton((100, 340), buttons, "Да", 'white'), TextButton((325, 340), buttons, "Нет", 'white')]

    time = Time((450, 400, 150, 50), 'white', -1, time)

    gui.add_element(text_score_head)
    gui.add_element(text_score)
    gui.add_element(text_next_shape)
    gui.add_element(game.get_next_shape())
    gui.add_element(text_time)
    gui.add_element(text_help_1)
    gui.add_element(text_help_2)
    gui.add_element(text_help_3)
    gui.add_element(text_help_4)
    gui.add_element(text_help_5)
    gui.add_element(time)

    rungame = True

    N = 1
    pause = False
    dialog_window = False

    while rungame:
        if not game.get_info():
            break

        fon_picture.draw(screen)

        for event in game_pygame.event.get():
            if event.type == QUIT:
                if game.get_static_pixels():
                    with open('data/save.tsv', 'w') as file:
                        file.write('')

                    save_game(game.get_static_pixels(), game_score, time.get_time())

                else:
                    with open('data/save.tsv', 'w') as file:
                        file.write('')

                terminate()

            if event.type == KEYDOWN and event.key == K_ESCAPE:
                dialog_window = True

                if game.get_static_pixels():
                    with open('data/save.tsv', 'w') as file:
                        file.write('')

                    save_game(game.get_static_pixels(), game_score, time.get_time())

                else:
                    with open('data/save.tsv', 'w') as file:
                        file.write('')

            if not dialog_window:
                if event.type == KEYUP and event.key == K_UP:
                    game.get_shape().rotate(game.get_board())

                if event.type == KEYUP and (event.key == K_p or event.key == K_PAUSE):
                    pause = not pause

                if event.type == KEYDOWN and event.key == K_DOWN and not pause:
                    game.change_speed(1)

                if event.type == KEYUP and event.key == K_DOWN and not pause:
                    game.change_speed(0)

            else:
                for i in range(len(choice_buttons)):
                    if choice_buttons[i].update(event):
                        if i == 0:
                            rungame = False
                            break

                        if i == 1:
                            dialog_window = False
                            break

        gui.render(screen)

        if not pause and not dialog_window:
            game_score += game.move_shape(music, clock)
            text_score.update(str(game_score))
            time.update(clock.get_time())

            if not game.get_speed()[0]:
                if int(N % game.get_speed()[1]) == 0:
                    game.update()

            else:
                game.update()

            if not game.get_info():
                push_records(player_nickname, game_score, time.get_time())

            N += 1

        elif pause:
            game.render(screen)
            text_pause_shape.render(screen)

        elif dialog_window:
            game.render(screen)
            game_pygame.draw.rect(screen, Color("black"), (75, 250, 475, 175))
            dilog.render(screen)
            buttons.draw(screen)

            for i in choice_buttons:
                i.render(screen)

        game_pygame.display.flip()
