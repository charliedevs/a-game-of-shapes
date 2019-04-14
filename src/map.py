"""
Strategy Game

Created by: Fernando Rodriguez, Charles Davis, Paul Rogers

"""

import sys
import pygame

import src.gamestate as gamestate

# Tile size
TILE_WIDTH = 23
TILE_HEIGHT = 23
TILE_MARGIN = 2

# Grid size
TILE_COLS = gamestate.get_tile_columns()
TILE_ROWS = gamestate.get_tile_rows()

# Physical Map Size
MAP_WIDTH = (TILE_COLS * (TILE_WIDTH + TILE_MARGIN)) + TILE_MARGIN
MAP_HEIGHT = (TILE_ROWS * (TILE_HEIGHT + TILE_MARGIN)) + TILE_MARGIN
MAP_SIZE = (MAP_WIDTH, MAP_HEIGHT)

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

class Map:

    def __init__(self, screen):

        # Drawable surfaces
        self.screen = screen
        self.map_size = MAP_SIZE

        # Determine placement of map within window
        map_x = (self.screen.get_size()[0] // 2) - (self.map_size[0] // 2)
        map_y = (self.screen.get_size()[1] // 2) - (self.map_size[1] // 2)
        map_w = self.map_size[0]
        map_h = self.map_size[1]
        map_rect = pygame.Rect(map_x, map_y, map_w, map_h)

        # Create map surface
        self.surface = self.screen.subsurface(map_rect)

        # Grid data structure and size
        self.grid = gamestate.get_game_state().get("tiles")
        self.cols = TILE_COLS
        self.rows = TILE_ROWS

        # Cell size
        self.tile_w = TILE_WIDTH
        self.tile_h = TILE_HEIGHT
        self.margin = TILE_MARGIN

    def handle_click(self, mousepos):
        # mousepos is a (x, y) point relative to window.
        # To get it relative to map, we must subtract the
        # offset from the mouse position. Dividing by the
        # cell size gives us the clicked cell.
        mouse_x, mouse_y = mousepos
        offset_x = self.get_rect().x
        offset_y = self.get_rect().y

        column = (mouse_x - offset_x) // (self.tile_w + self.margin)
        row = (mouse_y - offset_y) // (self.tile_h + self.margin)

        # DEBUG: print column and row of click
        print("Click ", mousepos, "Grid coords: ", column, row)

        if (self.checkTile(column, row) == 0):
            self.setTile(column, row, 1)
        elif (self.checkTile(column, row) == 1):
            self.setTile(column, row, 2)
        else:
            self.setTile(column, row)

    def draw(self):
        self.surface.fill(WHITE)

        for row in range(self.rows):
            for col in range(self.cols):
                color = BLACK
                if self.grid[row][col] == 1:
                    color = GREEN
                elif self.grid[row][col] == 2:
                    color = RED
                pygame.draw.rect(self.surface,
                                 color,
                                 [(self.margin + self.tile_w) * col + self.margin,
                                  (self.margin + self.tile_h) *
                                  row + self.margin,
                                  self.tile_w,
                                  self.tile_h])

    def setTile(self, column, row, tiletype=0):
        try:
            self.grid[row][column] = tiletype
            gamestate.set_tile(row, column, tiletype)
        except IndexError as e:
            print("[Error]:", e)

    def checkTile(self, column, row):
        try:
            return self.grid[row][column]
        except IndexError as e:
            print("[Error]:", e)

    def get_rect(self):
        # Returns a rect with (x, y) relative to window
        x, y = self.surface.get_abs_offset()
        w, h = self.map_size
        return pygame.Rect(x, y, w, h)

    def reset(self):
        # self.entities.empty()
        print("reset")