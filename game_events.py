from pygame import USEREVENT


OPEN_MAIN_MENU = USEREVENT+1
OPEN_LEADERBOARD = USEREVENT+2
OPEN_NEW_GAME = USEREVENT+3
OPEN_SAVED_GAME = USEREVENT+4
EXIT_TO_MAIN_MENU = USEREVENT+5

PAUSING_GAME = USEREVENT+6
RESUMING_GAME = USEREVENT+7

UPDATE_SCORE = USEREVENT+8
PLAY_SCORE_SOUND = USEREVENT+9
GAME_OVER = USEREVENT+10

SENDING_DATA_TO_SAVE = USEREVENT+11
