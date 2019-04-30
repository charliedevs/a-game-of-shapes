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
from src.unit import Unit

#########################################################################
# CONSTANTS

# Window Size
WINDOW_WIDTH = 700
WINDOW_HEIGHT = 500
WINDOW_CENTER = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)

# Move phases
# TODO: if click on same unit, set phase back to show move range
NOT_TURN = 0
SHOW_MOVE_RANGE = 1
MOVING = 2
ATTACKING = 3
END_TURN = 4


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

        # Set up display window
        pygame.display.set_caption("Strategy Game")     # NOTE: Display player num here?
        screen_res = (WINDOW_WIDTH, WINDOW_HEIGHT)
        self.screen = pygame.display.set_mode(
            screen_res, flags=pygame.RESIZABLE)
        
        # Set up font
        pygame.font.init()
        self.game_font = pygame.font.SysFont("Comic Sans MS", 60)

        # Set up gameplay map
        self.map = Map(self.screen, self.player_num)

        # Represents the state of game
        # Modified by server and sent to clients
        self.gamestate = self.network.get_gamestate()
        is_turn = self.gamestate.is_players_turn(self.player_num)

        # Effects of turn that are sent across network
        self.turn = {
            "move" : None,
            "attack" : None,
            "phase" : NOT_TURN
        }

        if is_turn:
            self.turn["phase"] = SHOW_MOVE_RANGE

        # Clock tracks time from beginning of game
        self.clock = pygame.time.Clock()

        self.mouse_position = pygame.mouse.get_pos()

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
                if self.map.get_rect().collidepoint(self.mouse_position):
                    self.map.handle_hover(self.mouse_position)

            # Only process clicks if it's this player's turn
            if self.gamestate.is_players_turn(self.player_num):
                # User clicks button
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.turn["phase"] == SHOW_MOVE_RANGE:
                        # show move range and stuff
                        # Mouse clicks on game board
                        self.turn = self.map.handle_click(self.mouse_position, self.turn)
                    elif self.turn["phase"] == MOVING:
                        # clicks will move unit
                        self.turn = self.map.handle_click(self.mouse_position, self.turn)
                    elif self.turn["phase"] == ATTACKING:
                        # show attack range
                        # and clicks will attack unit
                        # if no enemy unit in attack range, end turn
                        self.turn = self.map.handle_click(self.mouse_position, self.turn)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        #TODO: end turn on space key press
                        self.turn["phase"] = END_TURN
            else: # Other player's turn
                players_turn = self.network.request_turn()
                if players_turn == self.player_num:
                    self.update_gamestate()
                    self.turn["phase"] = SHOW_MOVE_RANGE

        # End players turn
        if self.turn["phase"] == END_TURN:
            # Send moves and attacks made to server
            self.network.send_turn(self.turn)
            self.gamestate.change_turns()
            self.turn["phase"] = NOT_TURN

    def update(self):
        """
        Update variables that change every frame.
        """
        self.ttime = self.clock.tick(30)
        self.mouse_position = pygame.mouse.get_pos()


    def update_gamestate(self):
        new_gamestate = self.network.get_gamestate()

        if new_gamestate.locations != self.gamestate.locations:
            # Update map with any moved units
            for unit_type, location in new_gamestate.locations.items():
                if location:
                    col, row = location
                    unit = self.map.get_unit_by_type(unit_type)
                    self.map.move(unit, col, row)

        if new_gamestate.unit_health != self.gamestate.unit_health:
            # Update units with any health changes
            #TODO: if we want animations, we'll have to encapsulate this health change rather than accessing it directly
            for unit_type, health in new_gamestate.unit_health.items():
                unit = self.map.get_unit_by_type(unit_type)
                unit.health = health
                
        self.turn["attack"] = None
        self.turn["move"] = None

        self.gamestate = new_gamestate

    def display_statistics(self):
        '''
        Display player information.
        '''
        # Font size is equal to line spacing 
        SIZE = 20

        # TODO: Player display/statistics
        font = pygame.font.SysFont("Comic Sans MS", SIZE)

        # Display player number
        textsurface = font.render("Player: " + str(self.player_num), False, colors.white)
        self.screen.blit(textsurface, [0, 0])

        # Display "Unit Information"
        location = [0, SIZE*3]  # Beginning of unit info.
        textsurface = font.render("Unit Information", False, colors.white)
        self.screen.blit(textsurface, location)

        # Display unit statistics
        for unit in self.map.players_units:
            # Increment horizontal placement
            location[1] += SIZE
            health = str(unit.health) + "/" + str(unit.max_health)
            textsurface = font.render(unit.archetype + ": " + health, False, unit.color)
            self.screen.blit(textsurface, location)
            


    def draw(self):
        """
        Draw graphics and display on screen.
        """
        self.screen.fill(colors.lightgray)

        # Display player statistics
        self.display_statistics()

        # Display game board
        self.map.draw()

        pygame.display.update()

    def waiting_screen(self):
        """
        Displays a waiting message until
        other client connects.
        """
        self.network.send_command("start")
        reply = self.network.receive()
        self.gamestate = self.network.get_gamestate()
        while not self.gamestate.ready():
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    print("Exiting game...")
                    self.network.close()
                    pygame.quit()
                    sys.exit(0)

            self.screen.fill(colors.purple)

            # Add text "waiting"
            textsurface = self.game_font.render("Waiting...", False, colors.white)
            text_rect = textsurface.get_rect(center=(WINDOW_CENTER))
            self.screen.blit(textsurface, text_rect)

            self.gamestate = self.network.get_gamestate()
            pygame.display.update()
