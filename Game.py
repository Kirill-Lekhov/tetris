import pygame

from PyGame_Additions.SingleSprite import SingleSprite
from constants import SCREEN_SIZE
from Tools.os_tools import terminate

from GUI_Stages.game_interface import GameInterface


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

# TODO: Add game support
GAME = None


def interface_update_result_parser(update_result: int):
    if update_result == 0:
        print(INTERFACE.get_player_nickname())
        print("Game has been started!")

    elif update_result == 1:
        print("Game has been ended!")

    elif update_result == 2:
        print("Game has been paused!")


while RUNNING:
    FON.draw(SCREEN)

    INTERFACE.update_without_event(CLOCK, 100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()

        interface_update_result_parser(INTERFACE.update(event))

    INTERFACE.draw(SCREEN)

    CLOCK.tick(60)
    pygame.display.flip()
