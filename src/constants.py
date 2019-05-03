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

# Unit_types
NO_UNIT = 0
P1_TRIANGLE = 1
P1_DIAMOND = 2
P1_CIRCLE = 3
P2_TRIANGLE = 4
P2_DIAMOND = 5
P2_CIRCLE = 6

# Max. health values
TRIANGLE_HEALTH = 4
DIAMOND_HEALTH = 5
CIRCLE_HEALTH = 3

# Tile_types
BLANK = 0
HEALTH = 1
HARM = 2
MOVABLE = 3
ATTACKABLE = 4

# Move phases
NOT_TURN = 0
PLACE_TILES = 1
SELECT_UNIT_TO_MOVE = 2
MOVING = 3
ATTACKING = 4
END_TURN = 5
GAME_OVER = 6

# Grid size
GRID_COLUMNS = 14
GRID_ROWS = 12

#########################################################################