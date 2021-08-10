import pygame

from Game_Stages.main_menu import main_menu
from Game_Stages.game import game_stage
from constants import DEFAULT_NAME

from PyGame_Additions.SingleSprite import SingleSprite

from constants import SCREEN_SIZE


RUNNING = True

pygame.init()
SCREEN = pygame.display.set_mode(SCREEN_SIZE)
CLOCK = pygame.time.Clock()

FON = SingleSprite("Fon_F.png")

pygame.mixer.music.load('data/music/main_theme.ogg')
pygame.mixer.music.play(-1)
MUSIC = pygame.mixer.Sound('data/music/deleting_line_sound.wav')
MUSIC.set_volume(0.4)


while RUNNING:
    game_settings = main_menu(pygame, SCREEN, FON, DEFAULT_NAME)
    game_stage(pygame, CLOCK, MUSIC, SCREEN, game_settings, FON)
