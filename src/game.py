""" 
Strategy Game

Created by: Fernando Rodriguez, Charles Davis, Paul Rogers

"""

#TODO: Create Unit class for unit actions and data
#TODO: Move code from here into relevant classes
#TODO: Create window class for display surface with functions that return size, center, etc.

import sys
import pygame

import src.gamestate as gamestate
from src.map import Map

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

class Game:

    def __init__(self):
        pygame.init()

        pygame.display.set_caption('Strategy')
        self.font = pygame.font.SysFont("Courier", 55)

        self.clock = pygame.time.Clock()
        self.last_tick = pygame.time.get_ticks()
        self.screen_res = (WINDOW_WIDTH, WINDOW_HEIGHT)

        self.screen = pygame.display.set_mode(self.screen_res, flags=pygame.RESIZABLE)
        self.map = Map(self.screen)

        self.clock.tick(30)

        self.game_loop()

    def game_loop(self):
        gameover = False
        while not gameover:
            self.event_loop()
            self.tick()
            self.draw()

    def event_loop(self):
        for event in pygame.event.get():
            # Client closes window
            if event.type == pygame.QUIT:
                # add code for terminating network connection
                pygame.quit()
                sys.exit(0)
            # User clicks mouse
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # User clicks on gameboard
                if self.map.get_rect().collidepoint(self.mousepos):
                    self.map.handle_click(self.mousepos)

    def tick(self):
        self.ttime = self.clock.tick()
        self.mousepos = pygame.mouse.get_pos()
        self.keys_pressed = pygame.key.get_pressed()

    def draw(self):
        self.screen.fill(GRAY)
        self.map.draw()
        pygame.display.update()

    def reset(self):
        #self.entities.empty()
        print("reset")