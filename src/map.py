"""
File: map.py
Programmers: Fernando Rodriguez, Charles Davis, Paul Rogers
"""
import pygame

import src.colors as colors
import src.unit as unit

#########################################################################
# CONSTANTS

# Tile size
TILE_WIDTH = 23
TILE_HEIGHT = 23
TILE_MARGIN = 2

# Units per player
MAX_UNITS = 3

#########################################################################


class Map:
    """
    Represents the game board.

    screen -- pygame display surface
    """

    def __init__(self, screen, grid, cols, rows, player_num):
        # Main window surface
        self.screen = screen

        # Grid data structure
        self.grid = grid
        cols = cols
        rows = rows

        # Size of individual tiles
        self.tile_w = TILE_WIDTH
        self.tile_h = TILE_HEIGHT
        self.margin = TILE_MARGIN

        # Full map size in pixels (calculated from grid and tile sizes)
        map_w = (cols * (self.tile_w + self.margin)) + self.margin
        map_h = (rows * (self.tile_h + self.margin)) + self.margin
        self.map_size = (map_w, map_h)

        # Determine placement of map within window
        map_x = (self.screen.get_size()[0] // 2) - (self.map_size[0] // 2)
        map_y = (self.screen.get_size()[1] // 2) - (self.map_size[1] // 2)
        map_rect = pygame.Rect(map_x, map_y, map_w, map_h)

        # Create map surface
        self.surface = self.screen.subsurface(map_rect)

        # Initialize player units
        self.player_units = []
        for unit_type in range(1, MAX_UNITS + 1):
            player_unit = unit.Unit(unit_type)
            self.player_units.append(player_unit)

        # Place units on grid
        if player_num == 1:
            col = 0
        else:
            col = cols
        grid[0][col] = self.player_units[0].unit_type
        grid[rows // 2][col] = self.player_units[1].unit_type
        grid[rows][col] = self.player_units[2].unit_type

    def handle_click(self, mousepos):
        """
        Process user clicks on game tiles

        Determines tile user clicked using mousepos.
        mousepos is a (x, y) point relative to window.

        Arguments:
            mousepos {(float, float)} -- The (x, y) position of mouse on window
        """

        mouse_x, mouse_y = mousepos

        # To get position relative to map, we must subtract the
        # offset from the mouse position. Dividing by the tile
        # size gives us the clicked tile.

        offset_x, offset_y = self.get_rect().topleft

        # Column and row of tile clicked by user
        column = (mouse_x - offset_x) // (self.tile_w + self.margin)
        row = (mouse_y - offset_y) // (self.tile_h + self.margin)

        # DEBUG: print column and row of click
        print("[Debug]: Click", mousepos, "Grid coords:", column, row)

        if self.get_tile_type(column, row) == 0:
            self.set_tile_type(column, row, 1)
        elif self.get_tile_type(column, row) == 1:
            self.set_tile_type(column, row, 2)
        else:
            self.set_tile_type(column, row, 0)

    def place_unit(self, col, row, unit):
        """
        Move unit to given location if possible.

        Arguments:
            col {int}   -- A column on the grid
            row {int}   -- A row on the grid
            unit {Unit} -- The unit to place

        Returns:
            bool -- whether the move was sucessful or not
        """

        success = False

        if self.grid[row][col][1] == 0:
            self.grid[row][col][1] = unit.unit_type
            success = True

        return success

    def draw(self):
        """
        Draw map onto surface.
        """

        self.surface.fill(colors.white)

        # Loop through the grid data structure
        for row in range(len(self.grid)):
            for (col, (tile_type, unit_type)) in enumerate(self.grid[row]):

                # Determine color of tiles
                tile_color = colors.darkgray
                if tile_type == 1:
                    tile_color = colors.green
                elif tile_type == 2:
                    tile_color = colors.red

                # Display tiles
                rect = pygame.draw.rect(self.surface,
                                        tile_color,
                                        [(self.margin + self.tile_w) * col + self.margin,
                                         (self.margin + self.tile_h) * row + self.margin,
                                         self.tile_w,
                                         self.tile_h])

                # Determine unit color and shape
                # using tile's rect as reference
                unit_color = colors.white
                pointlist = None
                if unit_type == 1:
                    # Green triangle
                    unit_color = colors.darkgreen
                    pointlist = [
                        rect.midtop,
                        rect.bottomleft,
                        rect.bottomright
                    ]
                elif unit_type == 2:
                    # Red diamond
                    unit_color = colors.darkred
                    pointlist = [
                        rect.midtop,
                        rect.midleft,
                        rect.midbottom,
                        rect.midright
                    ]
                elif unit_type == 3:
                    # Blue circle
                    unit_color = colors.darkblue
                    pos = rect.center
                    radius = rect.width / 2

                # Draw unit
                if unit_color == colors.white:
                    continue # No unit in this tile
                if pointlist is not None:
                    pygame.draw.polygon(
                        self.surface,
                        unit_color,
                        pointlist
                    )
                else:
                    pygame.draw.circle(
                        self.surface,
                        unit_color,
                        pos,
                        radius
                    )

    def get_rect(self):
        """
        Return rect with (x, y) relative to window.

        Returns:
            Rect -- The rectangle bounding map grid
        """

        x, y = self.surface.get_abs_offset()
        w, h = self.map_size
        return pygame.Rect(x, y, w, h)

    def set_tile_type(self, column, row, tile_type=0):
        """
        Change the type of a given tile.

        Arguments:
            column {int} -- The column of the tile to change
            row {int} -- The row of the tile to change

        Keyword Arguments:
            tile_type {int} -- 0=blank, 1=health, 2=harm (default: {0})
        """

        try:
            self.grid[row][column][0] = tile_type
        except IndexError as e:
            print("[Error]: Tile at Column: {0} Row: {1} doesn't exist.".format(
                column, row))
            print("       ", e)

    def get_tile_type(self, column, row):
        """
        Returns the type of tile at given column and row.

        Arguments:
            column {int} -- The column of the tile
            row {int} -- The row of the tile

        Returns:
            int -- The tile_type of given tile
                   Will be -1 if tile doesn't exist
        """

        try:
            return self.grid[row][column][0]
        except IndexError as e:
            print("[Error]: Tile at Column: {0} Row: {1} doesn't exist.".format(
                column, row))
            print("       ", e)
            return -1

    def clear(self):
        # Resets the map.
        #
        # Removes special tile_types and
        # TODO: resets unit positions.

        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                self.set_tile_type(col, row, 0)

        print("[Debug]: Map reset.")
