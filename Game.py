import pygame

from Tools.load_image import load_image
from Game_Stages.main_menu import main_menu
from Game_Stages.game import game_stage
from constants import DEFAULT_NAME


RUNNING = True

pygame.init()
SIZE = 600, 700
SCREEN = pygame.display.set_mode(SIZE)
CLOCK = pygame.time.Clock()

FON = pygame.sprite.Sprite()
FON.image = load_image("Fon_F.png")
FON.rect = FON.image.get_rect()
FON_PICTURE = pygame.sprite.Group()
FON_PICTURE.add(FON)

# Настройки музыки
pygame.mixer.music.load('data/music/main_theme.ogg')
pygame.mixer.music.play(-1)
MUSIC = pygame.mixer.Sound('data/music/deleting_line_sound.wav')
# Настройки музыки


while RUNNING:
    game_settings = main_menu(pygame, SCREEN, SIZE, FON_PICTURE, DEFAULT_NAME)
    game_stage(pygame, CLOCK, MUSIC, SCREEN, game_settings, FON_PICTURE)
