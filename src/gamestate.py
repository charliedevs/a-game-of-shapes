import enum

# Constants
TILE_ROWS = 10
TILE_COLS = 10
    
class GameState:
# Represents the game board and state of
# each tile. The GameState.data attribute
# contains the entire dictionary to be
# sent across the network.

    # Initialize 2D array holding Tile locations.
    # Fill with blank tiles.
    tiles = [[0 for j in range(TILE_COLS)] for i in range(TILE_ROWS)]

    data = {
        "tiles" : tiles,
    }

# Enum for tiletypes
# Access with Tiletype.typename
class Tiletype(enum.Enum):
    blank = 0
    blocked = 1
    harm = 2
    health = 3