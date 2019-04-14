""" 
Strategy Game

Created by: Fernando Rodriguez, Charles Davis, Paul Rogers

"""

# TODO: Create Unit class for unit actions and data
# TODO: Move code from here into relevant classes
# TODO: Create window class for display surface with functions that return size, center, etc.

import sys
import pygame

import src.gamestate as gamestate
from src.map import Map

#########################################################################
# CONSTANTS

# Window Size
WINDOW_WIDTH = 700
WINDOW_HEIGHT = 500
WINDOW_CENTER = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (30, 30, 30)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

#########################################################################


class Game:
    """Starts the game loop.

    The main game loop consists of an event
    loop, the tick loop (things updated every
    frame), and the draw loop.

    """

    def __init__(self):
        pygame.init()

        # Window title and in-game font
        pygame.display.set_caption('Strategy')
        self.font = pygame.font.SysFont("Courier", 55)

        # Clock tracks time from beginning of game
        self.clock = pygame.time.Clock()

        # Drawable surfaces
        screen_res = (WINDOW_WIDTH, WINDOW_HEIGHT)
        self.screen = pygame.display.set_mode(screen_res, flags=pygame.RESIZABLE)
        self.map = Map(self.screen)

        self.game_loop()

    def game_loop(self):
        while True:
            self.event_loop()
            self.tick()
            self.draw()

    def event_loop(self):
        # Handles user input.
        #
        # Events include mouse clicks and
        # keyboard presses.

        events = pygame.event.get()
        for event in events:
            # Client closes window
            if event.type == pygame.QUIT:
                # TODO: Add code for terminating network connection
                pygame.quit()
                sys.exit(0)
            # User clicks mouse
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # User clicks on gameboard
                if self.map.get_rect().collidepoint(self.mousepos):
                    self.map.handle_click(self.mousepos)

    def tick(self):
        # Updates variables that change every frame.

        self.ttime = self.clock.tick(30)
        self.mousepos = pygame.mouse.get_pos()
        self.keys_pressed = pygame.key.get_pressed()

    def draw(self):
        # Draw graphics and display on screen.

        self.screen.fill(GRAY)
        self.map.draw()
        pygame.display.update()

    def reset(self):
        # Reset the game board.

        self.map.clear()
