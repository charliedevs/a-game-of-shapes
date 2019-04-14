"""
 Represents the game board and state of
 each tile. The GameState.data attribute
 contains the entire dictionary to be
 sent across the network.
 """

import enum

# Grid size
TILE_COLS = 14
TILE_ROWS = 10

# Initialize 2D array holding Tile locations.
# Fill with blank tiles.
tiles = [[0 for j in range(TILE_COLS)] for i in range(TILE_ROWS)]

data = {
    "tiles": tiles,
}

def get_game_state():
    return data

def get_tile_columns():
    return TILE_COLS

def get_tile_rows():
    return TILE_ROWS

def set_tile(row, col, tiletype):
    data.get("tiles")[row][col] = tiletype

class Tiletype(enum.Enum):
# Enum for tiletypes
# Access with Tiletype.typename
    blank = 0
    blocked = 1
    harm = 2
    health = 3
