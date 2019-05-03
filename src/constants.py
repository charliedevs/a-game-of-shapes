"""
File: colors.py
Programmers: Fernando Rodriguez, Charles Davis
"""

#########################################################################
# CONSTANTS

# Window Size
WINDOW_WIDTH = 700
WINDOW_HEIGHT = 500
WINDOW_CENTER = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)

# Tile size
TILE_WIDTH = 23
TILE_HEIGHT = 23
TILE_MARGIN = 2

# Units per player
MAX_UNITS = 3

# Move phases
NOT_TURN = 0
PLACE_TILES = 1
SHOW_MOVE_RANGE = 2
MOVING = 3
ATTACKING = 4
END_TURN = 5
GAME_OVER = 6

#########################################################################