from pygame.mixer import find_channel
from pygame import QUIT, K_UP, KEYUP, KEYDOWN, Color, K_DOWN, K_ESCAPE, K_p, K_PAUSE

from Tools.game_file_functions import save_game, push_records
from Tools.os_tools import terminate
from Game_Parts.game_board import Game


def game_stage(game_pygame, clock, music, screen, game_settings, fon_picture):
    old_pixels, score, time, player_nickname = game_settings
    game = Game(screen, old_pixels)

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
            moving_result = game.move_shape(clock)
            game_score += moving_result

            if moving_result:
                channel = find_channel(True)
                channel.play(music)

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
