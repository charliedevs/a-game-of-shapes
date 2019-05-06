"""
File: grid.py
Programmers: Fernando Rodriguez, Charles Davis

"""
import pygame

import src.colors as colors
from src.constants import *
from src.unit import Unit

class Grid:
    """
    Data structure representing the game
    board and the state of each tile.

    Every tile contains a list of two
    values: [tile_type, unit_type]

    tile_type {int} --
        0 is blank
        1 is health
        2 is harm
        3 is movable
        4 is attackable

    unit_type {int} --
        0 is empty
        1 is player1, unit1
        2 is player1, unit2
        3 is player1, unit3
        4 is player2, unit1
        5 is player2, unit2
        6 is player2, unit3
    """

    def __init__(self):
        """
        Set up tile grid and units.
        """
        # Create grid data structure.
        # Each element of the grid contains
        # two values: [tile_type, unit_type].
        # Both are ints; [0, 0] means the tile
        # is blank and no unit is present.
        self.cols = GRID_COLUMNS
        self.rows = GRID_ROWS
        self.grid = [[[0, 0] for j in range(self.cols)] for i in range(self.rows)]

    def tile_in_move_range(self, col, row):
        return self.get_tile_type(col, row) == 3

    def tile_in_attack_range(self, col, row):
        return self.get_tile_type(col, row) == 4

    def set_tile_type(self, col, row, tile_type=0):
        """
        Change the type of a given tile.

        Arguments:
            col {int} -- The column of the tile to change
            row {int} -- The row of the tile to change

        Keyword Arguments:
            tile_type {int} -- 0=blank, 1=health, 2=harm (default: {0})
        """

        try:
            self.grid[row][col][0] = tile_type
        except IndexError as e:
            print("[Error]: Tile at Column: {0} Row: {1} doesn't exist.".format(
                col, row))
            print("       ", e)

    def get_tile_type(self, col, row):
        """
        Returns the type of tile at given column and row.

        Arguments:
            col {int} -- The column of the tile
            row {int} -- The row of the tile

        Returns:
            int -- The tile_type of given tile
                   Will be -1 if tile doesn't exist
        """

        try:
            return self.grid[row][col][0]
        except IndexError as e:
            print("[Error]: Tile at Column: {0} Row: {1} doesn't exist.".format(
                col, row))
            print("       ", e)
            return -1

    def get_unit_type(self, col, row):
        """
        Returns the unit type at given column and row.

        Arguments:
            column {int} -- The column of the tile
            row {int} -- The row of the tile

        Returns:
            int -- The unit_type at a given tile
                   Will be -1 if tile doesn't exist
        """
        try:
            return self.grid[row][col][1]
        except IndexError as e:
            print("[Error]: Tile at Column: {0} Row: {1} doesn't exist.".format(
                col, row))
            print("       ", e)
            return -1

    def set_unit_type(self, col, row, unit_type):
        """
        Change the unit_type on a given grid tile.

        Arguments:
            col {int} -- The column of the tile
            row {int} -- The row of the tile
            unit_type {int} -- 0=blank, 1-3=player1, 4-6=player2
        """

        try:
            self.grid[row][col][1] = unit_type
        except IndexError as e:
            print("[Error]: Tile at Column: {0} Row: {1} doesn't exist.".format(
                col, row))
            print("       ", e)