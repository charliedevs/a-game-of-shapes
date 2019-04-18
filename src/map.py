"""
File: map.py
Programmers: Fernando Rodriguez, Charles Davis, Paul Rogers
"""
import pygame
import src.colors as colors
from src.game import set_tiletype
#from src.gamestate import Tiletype

#########################################################################
# CONSTANTS

# Tile size
TILE_WIDTH = 23
TILE_HEIGHT = 23
TILE_MARGIN = 2

#########################################################################


class Map:
    """Represents the game board.

    screen -- pygame display surface
    """

    def __init__(self, screen):
        # Main window surface
        self.screen = screen

        # Grid data structure
        self.grid = gamestate.get_game_state().get("tiles")
        cols = gamestate.get_tile_columns()
        rows = gamestate.get_tile_rows()

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

    def handle_click(self, mousepos):
        # Processes user clicks on game tiles.
        #
        # Determines tile user clicked using mousepos.
        # mousepos is a (x, y) point relative to window.
        # To get it relative to map, we must subtract the
        # offset from the mouse position. Dividing by the
        # tile size gives us the clicked tile.

        mouse_x, mouse_y = mousepos
        offset_x, offset_y = self.get_rect().topleft
        # offset_x = self.get_rect().x
        # offset_y = self.get_rect().y

        # Column and row of tile clicked by user
        column = (mouse_x - offset_x) // (self.tile_w + self.margin)
        row = (mouse_y - offset_y) // (self.tile_h + self.margin)

        # DEBUG: print column and row of click
        print("[Debug]: Click", mousepos, "Grid coords:", column, row)

        if self.get_tiletype(column, row) == Tiletype.blank:
            self.set_tiletype(column, row, Tiletype.health)
        elif self.get_tiletype(column, row) == Tiletype.health:
            self.set_tiletype(column, row, Tiletype.harm)
        else:
            self.set_tiletype(column, row, Tiletype.blank)

    def draw(self):
        # Draw tiles onto screen.
        #
        # Loops through the grid data structure
        # and determines color based on tiletype.

        self.surface.fill(colors.white)
        for row in range(len(self.grid)):
            for (col, tiletype) in enumerate(self.grid[row]):
                color = colors.darkgray
                if tiletype == Tiletype.health:
                    color = colors.green
                elif tiletype == Tiletype.harm:
                    color = colors.red
                pygame.draw.rect(self.surface,
                                 color,
                                 [(self.margin + self.tile_w) * col + self.margin,
                                  (self.margin + self.tile_h) * row + self.margin,
                                  self.tile_w,
                                  self.tile_h])

    def get_rect(self):
        # Returns a rect with (x, y) relative to window.

        x, y = self.surface.get_abs_offset()
        w, h = self.map_size
        return pygame.Rect(x, y, w, h)

    def set_tiletype(self, column, row, tiletype=Tiletype.blank):
        # Change the type of a tile.
        #
        # Tiletype is passed in as
        # parameter. If given tile exists,
        # sets its type to tyletype.
        # Updates gamestate.

        try:
            self.grid[row][column] = tiletype
            set_tiletype(row, column, tiletype)
        except IndexError as e:
            print("[Error]: Tile at Column: {0} Row: {1} doesn't exist.".format(
                column, row))
            print("       ", e)

    def get_tiletype(self, column, row):
        # Returns tiletype at [column, row].
        # If tile doesn't exist, returns None.

        try:
            return self.grid[row][column]
        except IndexError as e:
            print("[Error]: Tile at Column: {0} Row: {1} doesn't exist.".format(
                column, row))
            print("       ", e)
            return None

    def clear(self):
        # Resets the map.
        #
        # Removes special tiletypes and
        # TODO: resets unit positions.

        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                self.set_tiletype(col, row, Tiletype.blank)

        print("[Debug]: Map reset.")
