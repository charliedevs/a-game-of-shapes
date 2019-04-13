""" 
Strategy Game

Created by: Fernando Rodriguez, Charles Davis, Paul Rogers

"""

# TODO: Create Unit class for unit actions and data
# TODO: Move code from here into relevant classes
# TODO: Create window class for display surface with functions that return size, center, etc.

import sys
import pygame

from src.gamestate import GameState
from src.map import Map

# Window Size
WINDOW_WIDTH = 700
WINDOW_HEIGHT = 500
WINDOW_CENTER = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)

# DEBUG: grid size
GRID_WIDTH = 23
GRID_HEIGHT = 23
GRID_MARGIN = 2

# Constants
TILE_ROWS = 10
TILE_COLS = 10

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (30, 30, 30)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


class Game:

    def __init__(self):
        pygame.init()

        pygame.display.set_caption('Strategy')

        self.clock = pygame.time.Clock()
        self.last_tick = pygame.time.get_ticks()
        self.screen_res = (WINDOW_WIDTH, WINDOW_HEIGHT)

        self.font = pygame.font.SysFont("Courier", 55)
        self.screen = pygame.display.set_mode(self.screen_res)

        #self.entities = pygame.sprite.Group()
        # TODO: continue moving grid stuff from here to map.py
        self.map = Map(self.screen)

        self.clock.tick(30)

        self.game_loop()

    def game_loop(self):
        gameover = False
        while not gameover:
            self.event_loop()
            self.tick()
            self.draw()
            pygame.display.update()

    def event_loop(self):
        for event in pygame.event.get():
            # Client closes window
            if event.type == pygame.QUIT:
                # add code for terminating network connection
                pygame.quit()
                sys.exit(0)
            # User clicks mouse
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # TODO: Change grid clicking to be relative to map rather than display surface
                mouse_x, mouse_y = self.mousepos
                if mouse_x not in range(self.map.cell_w * (self.map.cols + 1)):
                    break
                if mouse_y not in range(self.map.cell_h * (self.map.rows + 1)):
                    break
                # DEBUG: print column and row of click
                column = mouse_x // (GRID_WIDTH + GRID_MARGIN)
                row = mouse_y // (GRID_HEIGHT + GRID_MARGIN)
                if (self.map.checkTile(column, row) == 0):
                    self.map.setTile(column, row, 1)
                elif (self.map.checkTile(column, row) == 1):
                    self.map.setTile(column, row, 2)
                else:
                    self.map.setTile(column, row, 0)
                print("Click ", self.mousepos, "Grid coords: ", row, column)

    def tick(self):
        self.ttime = self.clock.tick()
        self.mousepos = pygame.mouse.get_pos()
        self.keys_pressed = pygame.key.get_pressed()

    def draw(self):
        self.screen.fill(GRAY)

        self.map.draw()

        # TODO: Create function to place map correctly on display surface, using Surface.get_size
        self.screen.blit(self.map.surface, (0, 0))
        pygame.display.update()
        # DEBUG: display grid here

        # update map layers?

        #self.player.update(self.ttime / 1000.)

        # for e in self.entities:
        #self.screen.blit(e.image, self.camera.apply(e))

    def reset(self):
        # self.entities.empty()
        print("reset")
