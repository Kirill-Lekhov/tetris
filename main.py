import pygame
from pygame.mixer import find_channel

from Tools import terminate
from Tools.Image import load_image

from PyGame_Additions import SingleSprite

from GUI_Stages.game_interface import GameInterface
from Game_Parts import GameBoard

from constants import SCREEN_SIZE
from game_events import PLAY_SCORE_SOUND

RUNNING = True

pygame.init()
SCREEN = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_icon(load_image("icon.png", -1))
pygame.display.set_caption("Python Tetris v2.0")
CLOCK = pygame.time.Clock()
FRAMERATE_LOCK = 60

FON = SingleSprite("background.png")

pygame.mixer.music.load('data/music/main_theme.ogg')
pygame.mixer.music.play(-1)
SCORE_SOUND = pygame.mixer.Sound('data/music/deleting_line_sound.wav')
SCORE_SOUND.set_volume(0.4)

INTERFACE = GameInterface()
GAME = GameBoard()


while RUNNING:
    FON.draw(SCREEN)

    INTERFACE.update_without_event(CLOCK)
    GAME.update_without_event(pygame, pygame.time.get_ticks())

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()

        if event.type == PLAY_SCORE_SOUND:
            channel = find_channel(True)
            channel.play(SCORE_SOUND)

        INTERFACE.update(pygame, event)
        GAME.update(pygame, event)

    GAME.draw(SCREEN)
    INTERFACE.draw(SCREEN)

    CLOCK.tick(60)
    pygame.display.flip()
