""" 
Strategy Game

Created by: Fernando Rodriguez, Charles Davis, Paul Rogers

"""

# TODO: Create Unit class for unit actions and data
# TODO: Move code from here into relevant classes
# TODO: Create window class for display surface with functions that return size, center, etc.

import sys
import pygame

#import src.pygame_input as pygame_input
import src.colors as colors
import src.gamestate as gamestate
import src.client.network as network
from src.map import Map
from src.button import Button

#########################################################################
# CONSTANTS

# Window Size
WINDOW_WIDTH = 700
WINDOW_HEIGHT = 500
WINDOW_CENTER = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)

#########################################################################


class Game:
    """
    Starts the game loop.

    The main game loop consists of an event
    loop, the tick loop (things updated every
    frame), and the draw loop.

    """

    def __init__(self, server_host, server_port, client_port):
        pygame.init()

        # Clock tracks time from beginning of game
        self.clock = pygame.time.Clock()

        # Set up display window
        pygame.display.set_caption('Strategy')
        screen_res = (WINDOW_WIDTH, WINDOW_HEIGHT)
        self.screen = pygame.display.set_mode(
            screen_res, flags=pygame.RESIZABLE)

        # Represents the state of game. Changes must be passed through here.
        self.gamestate = gamestate.GameState()

        # Set up gameplay map
        grid = self.gamestate.get_grid()
        cols = self.gamestate.get_tile_columns()
        rows = self.gamestate.get_tile_rows()
        self.map = Map(self.screen, grid, cols, rows)

        # Network connection
        self.connection = network.Network(server_host, server_port)
        #self.connection.connect()

        # List of buttons currently on screen
        self.buttons = []
        connect_button = Button(self.screen, (200, 300, 150, 30), action=lambda : print('Hi'), text="Connect")
        self.buttons.append(connect_button)

        # Textboxes
        #ip_textbox = pygame_input.TextInput()
        #port_textbox = pygame_input.TextInput

        # Not connected to another player at game start
        self.player_connected = False

        self.game_loop()

    def game_loop(self):
        while True:
            if self.player_connected:
                self.event_loop()
            else:
                self.intro_loop()

            self.tick()
            self.draw()

    def intro_loop(self):
        # Handles user input.
        #
        # Events include mouse clicks and
        # keyboard presses.

        events = pygame.event.get()
        for event in events:
            # Client closes window
            if event.type == pygame.QUIT:
                # TODO: Add code for terminating network connection
                print("Exiting game...")
                pygame.quit()
                sys.exit(0)

            # User clicks mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.buttons:
                    if button.get_rect().collidepoint(self.mousepos):
                        if button.handle_click():
                            self.player_connected = True

                

    def event_loop(self):
        # Handles user input.
        #
        # Events include mouse clicks and
        # keyboard presses.

        events = pygame.event.get()
        # TODO: if is_player_turn
        for event in events:
            # Client closes window
            if event.type == pygame.QUIT:
                # TODO: Add code for terminating network connection
                print("Exiting game...")
                pygame.quit()
                sys.exit(0)

            # User clicks mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
            
                for button in self.buttons:

                    if button.get_rect().collidepoint(self.mousepos):

                        button.handle_click()

                # Mouse clicks on game board
                if self.map.get_rect().collidepoint(self.mousepos):
                    self.map.handle_click(self.mousepos)
                    self.update_gamestate()

    def tick(self):
        # Updates variables that change every frame.

        self.ttime = self.clock.tick(30)
        self.mousepos = pygame.mouse.get_pos()
        self.keys_pressed = pygame.key.get_pressed()

    def draw(self):
        # Draw graphics and display on screen.

        self.screen.fill(colors.lightgray)

        if self.player_connected:
            self.map.draw()
        else:
            # Draw menu
            for button in self.buttons:
                button.draw()

        pygame.display.update()

    def reset(self):
        # Reset the game board.

        self.map.clear()

    def update_gamestate(self):
        self.gamestate.data["grid"] = self.map.grid
        #self.connection.send("game")
        #self.connection.send_gamestate(self.gamestate.data)