"""
 Represents the game board and state of
 each tile. The GameState.data attribute
 contains the entire dictionary to be
 sent across the network.
 """

import enum

#########################################################################
# CONSTANTS

# Grid size
TILE_COLS = 14
TILE_ROWS = 10

#########################################################################


class Tiletype(enum.Enum):
    # Enum for tiletypes
    # Access with Tiletype.typename
    blank = 0
    blocked = 1
    harm = 2
    health = 3


# Initialize 2D array holding Tile locations, and fill with blank tiles.
tiles = [[Tiletype.blank for j in range(TILE_COLS)] for i in range(TILE_ROWS)]

# Main data structure (to be sent across network)
data = {
    "tiles": tiles,
}


def get_game_state():
    # Returns the entire game state.
    #
    # A dictionary holding all values
    # in game to be sent thru network.

    return data


def get_tile_columns():
    return TILE_COLS


def get_tile_rows():
    return TILE_ROWS


def set_tiletype(row, col, tiletype):
    data.get("tiles")[row][col] = tiletype
