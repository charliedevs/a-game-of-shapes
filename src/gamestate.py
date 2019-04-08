import enum

class GameState:
""" Represents the game board and state of
    each tile. The GameState.data attribute
    contains the entire dictionary to be
    sent across the network.
"""
    # Constants
    TILE_ROWS = 5
    TILE_COLS = 9

    def __init__(self):

        # Initialize 2D array holding Tile locations.
        # Fill with blank tiles.
        self.tiles = [[Tiletype.blank for j in range(TILE_COLS)] for i in range(TILE_ROWS)]

        # Array holding locations of player1's
        # three characters.

        # Main data structure
        # 
        self.data = {
            "tiles" : self.tiles,
        }

# Enum for tiletypes
# Access with Tiletype.typename
class Tiletype(enum.Enum):
    blank = 0
    blocked = 1
    harm = 2
    health = 3