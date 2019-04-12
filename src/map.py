""" 
Strategy Game

Created by: Fernando Rodriguez, Charles Davis, Paul Rogers

"""

import sys
import pygame

from src.gamestate import GameState

# Physical Map Size
MAP_WIDTH = 255
MAP_HEIGHT = 255
MAP_SIZE = (MAP_WIDTH, MAP_HEIGHT)

#DEBUG: grid size
CELL_WIDTH = 23
CELL_HEIGHT = 23
CELL_MARGIN = 2

# Constants
TILE_ROWS = 10
TILE_COLS = 10

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

class Map:

    def __init__(self, screen):

        self.map_size = MAP_SIZE
        self.surface = pygame.Surface(self.map_size)

        self.grid = GameState.tiles
        self.rows = TILE_ROWS
        self.cols = TILE_COLS

        self.cell_w = CELL_WIDTH
        self.cell_h = CELL_HEIGHT
        self.margin = CELL_MARGIN

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
                                 [(CELL_MARGIN + CELL_WIDTH) * col + CELL_MARGIN,
                                  (CELL_MARGIN + CELL_HEIGHT) * row + CELL_MARGIN,
                                  CELL_WIDTH,
                                  CELL_HEIGHT])

        #for e in self.entities:
            #self.screen.blit(e.image, self.camera.apply(e))

    def setTile(self, column, row, tiletype=0):
        self.grid[row][column] = tiletype
        GameState.tiles = self.grid
    
    def checkTile(self, column, row):
        return self.grid[row][column]
    
    def reset(self):
        #self.entities.empty()
        print("reset")