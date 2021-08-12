import pygame

from PyGame_Additions.SingleSprite import SingleSprite
from constants import SCREEN_SIZE
from Tools.os_tools import terminate

from TestGUI import GameInterface


RUNNING = True

pygame.init()
SCREEN = pygame.display.set_mode(SCREEN_SIZE)
CLOCK = pygame.time.Clock()
FRAMERATE_LOCK = 60

FON = SingleSprite("Fon_F.png")

pygame.mixer.music.load('data/music/main_theme.ogg')
pygame.mixer.music.play(-1)
SCORE_SOUND = pygame.mixer.Sound('data/music/deleting_line_sound.wav')
SCORE_SOUND.set_volume(0.4)


interface = GameInterface("main_menu", True)


while RUNNING:
    FON.draw(SCREEN)

    interface.update_without_event()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()

        interface.update(event)

    interface.draw(SCREEN)

    CLOCK.tick(60)
    pygame.display.flip()
