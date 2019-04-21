""" 
Strategy Game

Created by: Fernando Rodriguez, Charles Davis, Paul Rogers

"""

import sys
import pygame

import src.colors as colors
from src.gamestate import GameState
from src.network import Network
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
    loop, the update loop (things updated every
    frame), and the draw loop.

    """

    def __init__(self, network):
        """
        Set up display and game map
        
        Arguments:
            network {Network} -- Connection to server
        """
        pygame.init()

        # Connection to the server
        self.network = network
        self.player_num = self.network.get_player_num()
        print("You are player", self.player_num)

        # Represents the state of game
        # Created by server and sent to clients
        self.gamestate = None

        # Set up display window
        pygame.display.set_caption('Strategy')
        screen_res = (WINDOW_WIDTH, WINDOW_HEIGHT)
        self.screen = pygame.display.set_mode(
            screen_res, flags=pygame.RESIZABLE)

        # Set up gameplay map
        self.map = Map(self.screen, self.network, self.player_num)

        # List of buttons currently on screen
        self.buttons = []
        # connect_button = Button(self.screen, (200, 300, 150, 30), action=lambda : print('Hi'), text="Connect")
        # self.buttons.append(connect_button)

        # Clock tracks time from beginning of game
        self.clock = pygame.time.Clock()

        self.mousepos = pygame.mouse.get_pos()

        # Show waiting screen until other player connects
        self.waiting_screen()
        # Start the game
        self.game_loop()

    def game_loop(self):
        """
        Loops until window is closed.
        """
        while True:
            self.event_loop()
            self.update()
            self.draw()


    def event_loop(self):
        """
        Handles user input.

        Events include mouse clicks
        and keyboard presses.
        """
        # finish_turn is true when current player's turn ends
        finish_turn = False

        events = pygame.event.get()
        for event in events:
            # Client closes window
            if event.type == pygame.QUIT:
                print("Exiting game...")
                self.network.close()
                pygame.quit()
                sys.exit(0)

            # User hovers over tile
            if event.type == pygame.MOUSEMOTION:
                if self.map.get_rect().collidepoint(self.mousepos):
                    self.map.handle_hover(self.mousepos)

            # Only process clicks if it's this player's turn
            if self.gamestate.is_players_turn(self.player_num):
                # User clicks mouse
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self.buttons:
                        # Mouse clicks button
                        if button.get_rect().collidepoint(self.mousepos):
                            button.handle_click(self.network)
                    # Mouse clicks on game board
                    if self.map.get_rect().collidepoint(self.mousepos):
                        finish_turn = self.map.handle_click(self.mousepos, self.network)
            else: # Other player's turn
                pass

        if finish_turn:
            self.network.send_command("end_turn")

    def update(self):
        """
        Update variables that change every frame.
        """
        self.ttime = self.clock.tick(30)
        self.mousepos = pygame.mouse.get_pos()
        new_gamestate = self.network.get_gamestate()

        # Update map with any moved units
        for unit_type, location in new_gamestate.locations.items():
            if location != self.gamestate.locations[unit_type]:
                col, row = location
                self.map.move(unit_type, col, row)

        self.gamestate = new_gamestate

    def draw(self):
        """
        Draw graphics and display on screen.
        """
        self.screen.fill(colors.lightgray)

        # Display game board
        self.map.draw()

        # Show buttons
        for button in self.buttons:
            button.draw()
        
        # TODO: Draw other lables

        pygame.display.update()

    def waiting_screen(self):
        """
        Displays a waiting message until
        other client connects.
        """
        self.gamestate = self.network.get_gamestate()
        while not self.gamestate.connected():
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    print("Exiting game...")
                    self.network.close()
                    pygame.quit()
                    sys.exit(0)

            self.screen.fill(colors.purple)
            #TODO: Add text "waiting"
            self.gamestate = self.network.get_gamestate()
            pygame.display.update()