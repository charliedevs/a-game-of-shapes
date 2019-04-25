"""
File: map.py
Programmers: Fernando Rodriguez, Charles Davis, Paul Rogers
"""
import pygame

import src.colors as colors
from src.unit import Unit
from src.grid import Grid
from src.unit import Unit

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
    The surface on which gameplay occurs.
    
    Comprised of a grid of tiles, where each tile
    has a tile_type and a unit_type. Units move
    across tiles and are affected by tile_type.

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

        # The grid is a 2D array with columns and rows
        self.grid = Grid()
        cols = self.grid.cols
        rows = self.grid.rows

        # TODO: create function to return a tile, and one to get tile based on mouse_position

        # The dimensions of each tile
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

        # Set up player units
        self.player_units = []
        self.initialize_units()



    def handle_hover(self, mouse_position):
        # highlights tile hovered over
        pass

    def handle_click(self, mouse_position):
        """
        Process user clicks on game tiles.

        Arguments:
            mouse_position {(float, float)} -- The (x, y) position of mouse on window
        """

        column, row = self.determine_tile_from_mouse_position(mouse_position)
        print("[Debug]: Click", mouse_position, "Grid coords:", column, row)

        # Set to True if turn ends
        finish_turn = False
        # TODO: Handle moves and send to network

        # if clicked on unit:
        #     change color of tiles around unit to matching speed

        ########################################################
        # Changes color on click
        if self.grid.get_tile_type(column, row) == 0:
            self.grid.set_tile_type(column, row, 1)
        elif self.grid.get_tile_type(column, row) == 1:
            self.grid.set_tile_type(column, row, 2)
        else:
            self.grid.set_tile_type(column, row, 0)
        ########################################################

        finish_turn = True
        # Turn is over
        return finish_turn

    def determine_tile_from_mouse_position(self, mouse_position):
        """
        To get position relative to map, we must subtract the
        offset from the mouse position. Dividing by the tile
        size gives us the clicked tile.
        
        Arguments:
            mouse_position {(float, float)} -- Position (x, y) of mouse on game window in pixels

        Returns:
            tile_position {(int, int)} -- Column and row of tile on grid
        """
        mouse_x, mouse_y = mouse_position
        offset_x, offset_y = self.get_rect().topleft

        col = (mouse_x - offset_x) // (self.tile_w + self.margin)
        row = (mouse_y - offset_y) // (self.tile_h + self.margin)

        return (col, row)

    def draw(self):
        """
        Draw map onto surface.
        """

        self.surface.fill(colors.white)

        # Loop through the grid data structure
        for row in range(self.grid.rows):
            for col in range(self.grid.cols):

                unit_type = self.grid.get_unit_type(col, row)
                unit = self.get_unit_by_type(unit_type)
                tile_type = self.grid.get_tile_type(col, row)

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
                if unit is not None:
                    if unit.is_triangle():
                        # Green triangle
                        unit_color = colors.darkgreen
                        pointlist = [
                            rect.midtop,
                            rect.bottomleft,
                            rect.bottomright
                        ]
                    elif unit.is_diamond():
                        # Red diamond
                        unit_color = colors.darkred
                        pointlist = [
                            rect.midtop,
                            rect.midleft,
                            rect.midbottom,
                            rect.midright
                        ]
                    elif unit.is_circle():
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
        """
        unit = self.get_unit_by_type(unit_type)

        if self.grid.get_unit_type(col, row) == 0:
            self.grid.set_unit_type(col, row, unit_type)
            unit.pos = [col, row]
            move = {unit_type : [col, row]}
            self.network.send_move(move)

    def attack(self, col, row, unit):
        pass


    def get_unit_by_type(self, unit_type):
        target_unit = None
        for unit in self.player_units:
            if unit.unit_type == unit_type:
                target_unit = unit
                break

        return target_unit

    def initialize_units(self):
        """
        Place all units on map in initial positions.
        """
        # Create Unit objects and add to list
        total_units = (2 * MAX_UNITS)
        for unit_type in range(1, total_units + 1):
            player_unit = Unit(unit_type)
            self.player_units.append(player_unit)

        # Place units on grid
        col = 0
        row = 0
        for unit in self.player_units:
            if unit.unit_type == 4:
                # Place player 2's units (4-6) on rhs
                col = self.grid.cols - 1
                row = 0
            self.move(unit.unit_type, col, row)
            # Place units on separate rows
            row += (self.grid.rows // 2) - 1

    def clear(self):
        # Resets the map.
        #
        # Removes special tile_types and
        # TODO: resets unit positions.

        for row in range(self.grid.rows):
            for col in range(self.grid.cols):
                self.grid.set_tile_type(col, row, 0)

        self.initialize_units()

        print("[Debug]: Map reset.")
