import pygame

from PyGame_Additions.SingleSprite import SingleSprite
from constants import SCREEN_SIZE
from Tools.os_tools import terminate

from GUI_Stages.game_interface import GameInterface
from Game_Parts.game_board import GameBoard
from pygame.mixer import find_channel

from Tools.game_file_functions.records import push_records
from Tools.game_file_functions.save_game import save_game


RUNNING = True

pygame.init()
SCREEN = pygame.display.set_mode(SCREEN_SIZE)
CLOCK = pygame.time.Clock()
FRAMERATE_LOCK = 60

FON = SingleSprite("Fon_F.png")

# pygame.mixer.music.load('data/music/main_theme.ogg')
# pygame.mixer.music.play(-1)
SCORE_SOUND = pygame.mixer.Sound('data/music/deleting_line_sound.wav')
SCORE_SOUND.set_volume(0.4)

INTERFACE = GameInterface()
GAME = GameBoard()

CURRENT_PLAYER = ""


def interface_update_parser(update_result: int):
    global CURRENT_PLAYER

    if update_result == 0:
        CURRENT_PLAYER = INTERFACE.get_player_nickname()
        GAME.load_new_game()
        GAME.play()

    elif update_result == 1:
        save_game(GAME.get_static_pixels(), GAME.get_score(), INTERFACE.get_game_time())
        GAME.game_pause()
        GAME.play()

    elif update_result == 2:
        GAME.game_pause()


def game_uwe_parser(update_result: int):
    if update_result == 1:
        channel = find_channel(True)
        channel.play(SCORE_SOUND)

    elif update_result == 2:
        INTERFACE.set_main_menu(player_nickname=CURRENT_PLAYER)
        push_records(CURRENT_PLAYER, GAME.get_score(), INTERFACE.get_game_time())
        GAME.play()


while RUNNING:
    FON.draw(SCREEN)

    INTERFACE.update_without_event(CLOCK, GAME.get_score())
    game_uwe_parser(GAME.update_without_event(pygame.time.get_ticks()))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()

        interface_update_parser(INTERFACE.update(event))
        GAME.update(event)

    GAME.draw(SCREEN)
    INTERFACE.draw(SCREEN)

    CLOCK.tick(60)
    pygame.display.flip()
