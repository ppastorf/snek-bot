##############################################################################
#                        # CONSTANTS FOR THE GAME ITSELF #

# Total size of the game screen
X_SIZE = 400
Y_SIZE = 400

# Size of the score display on the bottom of the screen
SCORE_SIZE = 20

# Size of a piece (block wich constitutes every part of the snake, the food and the offset borders)
PIECE_SIZE = 10

# Size of the offset border
OFFSET = PIECE_SIZE

# Size of the playable portion of the screen (game screen - offset borders)
REAL_X_SIZE = X_SIZE-OFFSET
REAL_Y_SIZE = Y_SIZE-OFFSET

# Starting values of the snake's head
START_POS = [300,200]
START_DIR = 'left'

# Timeout between every game tick in seconds 
HUMAN_TIMEOUT = 0.040
BOT_SHOW_TIMEOUT = 0.010

# Elements color
FOOD_COLOR = "#006600"
HEAD_COLOR = "#804d00"
BODY_COLOR = "#e68a00"
BORD_COLOR = "#000000"
###############################################################################W