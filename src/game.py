""" 
Strategy Game

Created by: Fernando Rodriguez, Charles Davis, Paul Rogers

"""

#TODO: Create Map class that will draw the grid and hold tiles
#TODO: Create Unit class for unit actions and data
#TODO: Move code from here into relevant classes

import sys
import pygame

from src.gamestate import GameState

# Window Size
WINDOW_WIDTH = 255
WINDOW_HEIGHT = 255

#DEBUG: grid size
GRID_WIDTH = 23
GRID_HEIGHT = 23
GRID_MARGIN = 2

# Constants
TILE_ROWS = 10
TILE_COLS = 10

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
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
        self.rows = TILE_ROWS
        self.cols = TILE_COLS
        self.game_state = GameState()
        self.grid = self.game_state.tiles

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
                if self.mousepos[0] not in range(GRID_WIDTH * (self.cols + 1)):
                    break
                if self.mousepos[1] not in range(GRID_HEIGHT * (self.rows + 1)):
                    break
                #DEBUG: print column and row of click
                column = self.mousepos[0] // (GRID_WIDTH + GRID_MARGIN)
                row = self.mousepos[1] // (GRID_HEIGHT + GRID_MARGIN)
                if (self.grid[row][column] == 0):
                    self.grid[row][column] = 1
                elif (self.grid[row][column] == 1):
                    self.grid[row][column] = 2
                else:
                    self.grid[row][column] = 0
                print("Click ", self.mousepos, "Grid coords: ", row, column)
                
    
    def tick(self):
        self.ttime = self.clock.tick()
        self.mousepos = pygame.mouse.get_pos()
        self.keys_pressed = pygame.key.get_pressed()

    def draw(self):
        self.screen.fill(WHITE)

        for row in range(self.rows):
            for col in range(self.cols):
                color = BLACK
                if self.grid[row][col] == 1:
                    color = GREEN
                elif self.grid[row][col] == 2:
                    color = RED
                pygame.draw.rect(self.screen,
                                 color,
                                 [(GRID_MARGIN + GRID_WIDTH) * col + GRID_MARGIN,
                                  (GRID_MARGIN + GRID_HEIGHT) * row + GRID_MARGIN,
                                  GRID_WIDTH,
                                  GRID_HEIGHT])

        pygame.display.update()
        #DEBUG: display grid here

        #update map layers?

        #self.player.update(self.ttime / 1000.)

        #for e in self.entities:
            #self.screen.blit(e.image, self.camera.apply(e))

    def reset(self):
        #self.entities.empty()
        print("reset")