"""
File: gamestate.py
Programmers: Fernando Rodriguez, Charles Davis, Paul Rogers


Represents the game board and state of
each tile. The GameState.data attribute
contains the entire dictionary to be
sent across the network.

    t -- tiletype
        0 is blank
        1 is health
        2 is harm
        3 is slowdown
    u -- unit
        0 is blank
        1 is player1 unit1
        2 is player1 unit2
        3 is player1 unit3
        4 is player2 unit1
        5 is player2 unit2
        6 is player2 unit3

"""
import enum

#########################################################################
# CONSTANTS

# Grid size
TILE_COLS = 14
TILE_ROWS = 10

#########################################################################


class GameState:

    def __init__(self):
        # Initialize 2D array holding Tile locations, and fill with blank tiles.
        self.grid = [[[0, 0] for j in range(TILE_COLS)] for i in range(TILE_ROWS)]

        # Main data structure (to be sent across network)
        self.data = {
            "grid": self.grid,
            "client_addr": None
        }


    def get_grid(self):
        # Returns the entire game state.
        #
        # A dictionary holding all values
        # in game to be sent thru network.

        return self.data["grid"]

    def get_tile_columns(self):
        return TILE_COLS

    def get_tile_rows(self):
        return TILE_ROWS

    def set_tiletype(self, col, row, tiletype):
        self.data["grid"][row][col][0] = tiletype
