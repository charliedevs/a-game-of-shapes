"""
File: map.py
Programmers: Fernando Rodriguez, Charles Davis, Paul Rogers
"""
import pygame

import src.colors as colors
from src.unit import Unit

#########################################################################
# CONSTANTS

# Tile size
TILE_WIDTH = 23
TILE_HEIGHT = 23
TILE_MARGIN = 2

# Grid size
GRID_COLUMNS = 14
GRID_ROWS = 10

# Units per player
MAX_UNITS = 3

#########################################################################


class Map:
    """
    Represents the game board and state
    of each tile.
    
    Every tile contains a list of two
    values: [tile_type, unit_type]

    tile_type {int} --
        0 is blank
        1 is health
        2 is harm
        3 is slowdown

    unit_type {int} --
        0 is empty
        1 is player1, unit1
        2 is player1, unit2
        3 is player1, unit3
        4 is player2, unit1
        5 is player2, unit2
        6 is player2, unit3
    """

    def __init__(self, screen, network, player_num):
        """
        Set up tile grid and units.

        
        Arguments:
            screen {pygame.Surface} -- The main display window
            network {Network} -- Connection to the server
            player_num {int} -- The player identifier; 1 or 2
        """

        self.screen = screen
        self.network = network
        self.player_num = player_num

        # Create grid data structure.
        # Each element of the grid contains
        # two values: [tile_type, unit_type].
        # Both are ints; [0, 0] means the tile
        # is blank and no unit is present.
        cols = GRID_COLUMNS
        rows = GRID_COLUMNS
        self.grid = [[[0, 0] for j in range(cols)] for i in range(rows)]

        # TODO: create function to return a tile, and one to get tile based on mousepos

        # Size of individual tiles
        self.tile_w = TILE_WIDTH
        self.tile_h = TILE_HEIGHT
        self.margin = TILE_MARGIN

        # Full map size in pixels (calculated from grid and tile sizes)
        map_w = (cols * (self.tile_w + self.margin)) + self.margin
        map_h = (rows * (self.tile_h + self.margin)) + self.margin
        self.map_size = (map_w, map_h)

        # Determine placement of map within display window
        map_x = (self.screen.get_size()[0] // 2) - (self.map_size[0] // 2)
        map_y = (self.screen.get_size()[1] // 2) - (self.map_size[1] // 2)
        map_rect = pygame.Rect(map_x, map_y, map_w, map_h)

        # Create map surface
        self.surface = self.screen.subsurface(map_rect)

        # Initialize player units
        unit_offset = 0
        if player_num == 2: # units are numbered 4-6
            unit_offset = 3
        self.player_units = []
        for unit_type in range(1, MAX_UNITS + 1):
            player_unit = Unit(unit_type + unit_offset)
            self.player_units.append(player_unit)

        # Place units on grid.
        # Calculate column and row based
        # on player_num and unit_type.
        if self.player_num == 1:
            col = 0
        else:
            col = cols - 1
        row = 0
        for unit in self.player_units:
            self.move(unit.unit_type, col, row)
            # Send move to server
            network_move = {unit.unit_type : [col, row]}
            unit.pos = [col, row]
            print("[Debug]:", network_move)
            self.network.send_move(network_move)
            row += (rows // 2) - 1


    def handle_hover(self, mousepos):
        # highlights tile hovered over
        pass

    def handle_click(self, mousepos, network):
        """
        Process user clicks on game tiles

        Determines tile user clicked using mousepos.
        mousepos is a (x, y) point relative to window.

        Arguments:
            mousepos {(float, float)} -- The (x, y) position of mouse on window
            network {Network} -- Used to send commands to server
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

        # Set to True if turn ends
        finish_turn = False
        # TODO: Handle moves and send to network

        # if clicked on unit:
        #     change color of tiles around unit to matching speed



        ########################################################
        # Changes color on click
        if self.get_tile_type(column, row) == 0:
            self.set_tile_type(column, row, 1)
        elif self.get_tile_type(column, row) == 1:
            self.set_tile_type(column, row, 2)
        else:
            self.set_tile_type(column, row, 0)
        ########################################################

        # Turn is over
        return finish_turn

    def draw(self):
        """
        Draw map onto surface.
        """

        self.surface.fill(colors.white)

        # Loop through the grid data structure
        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):

                tile_type = self.grid[row][col][0]
                unit_type = self.grid[row][col][1]

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
                if unit_type == 1 or unit_type == 4:
                    # Green triangle
                    unit_color = colors.darkgreen
                    pointlist = [
                        rect.midtop,
                        rect.bottomleft,
                        rect.bottomright
                    ]
                elif unit_type == 2 or unit_type == 5:
                    # Red diamond
                    unit_color = colors.darkred
                    pointlist = [
                        rect.midtop,
                        rect.midleft,
                        rect.midbottom,
                        rect.midright
                    ]
                elif unit_type == 3 or unit_type == 6:
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
                        int(radius)
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

    def move(self, unit_type, col, row):
        """
        Move unit to given location if possible.

        Arguments:
            col {int}   -- A column on the grid
            row {int}   -- A row on the grid
            unit_type {int} -- The unit to place

        Returns:
            {unit_type : [x,y]} -- Dict representing move
        """

        move = None

        # If no unit is on desired space
        if self.grid[row][col][1] == 0:
            self.grid[row][col][1] = unit_type
            move = {unit_type : [col, row]}

        return move

    def attack(self, col, row, unit):
        pass

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

    def clear(self):
        # Resets the map.
        #
        # Removes special tile_types and
        # TODO: resets unit positions.

        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                self.set_tile_type(col, row, 0)

        print("[Debug]: Map reset.")

    
