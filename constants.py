from pygame import USEREVENT

# Constants
COLORS = ['purple', 'red', 'green', 'blue', 'yellow']
SHAPE = ['J', 'L', 'S', 'T', 'Z', 'I', 'O']
REWARD = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}
TYPES = {'J': [[[0, 5], [1, 5], [2, 5], [2, 4]], [[0, 3], [1, 3], [1, 4], [1, 5]],
               [[2, 4], [1, 4], [0, 4], [0, 5]], [[0, 3], [0, 4], [0, 5], [1, 5]]],
         'L': [[[0, 4], [1, 4], [2, 4], [2, 5]], [[1, 3], [0, 3], [0, 4], [0, 5]],
               [[0, 4], [0, 5], [1, 5], [2, 5]], [[1, 3], [1, 4], [1, 5], [0, 5]]],
         'S': [[[1, 3], [1, 4], [0, 4], [0, 5]], [[0, 4], [1, 4], [1, 5], [2, 5]]],
         'T': [[[1, 3], [1, 4], [1, 5], [0, 4]], [[0, 4], [1, 4], [2, 4], [1, 5]],
               [[0, 3], [0, 4], [0, 5], [1, 4]], [[0, 5], [1, 5], [2, 5], [1, 4]]],
         'Z': [[[0, 3], [0, 4], [1, 4], [1, 5]], [[0, 5], [1, 5], [1, 4], [2, 4]]],
         'I': [[[0, 3], [0, 4], [0, 5], [0, 6]]],
         'O': [[[0, 4], [0, 5], [1, 5], [1, 4]]]}
DEFAULT_NAME = 'NoName'

# Pygame Settings
SCREEN_SIZE = 600, 700

# TODO: Move events to a separate file
# Events
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
