""" 
Strategy Game

Created by: Fernando Rodriguez, Charles Davis, Paul Rogers

"""

import sys
import pygame

# Constants
import src.colors as colors
from src.constants import *

# Classes
from src.gamestate import GameState
from src.network import Network
from src.map import Map
from src.unit import Unit

class Game:
    """
    Starts the game loop.

    The main game loop consists of an event
    loop, the update loop (things updated every
    frame), and the draw loop.

    """

    def __init__(self, network):
        """
        Set up display and game map.
        
        Arguments:
            network {Network} -- Connection to server
        """
        pygame.init()

        # Connection to the server
        self.network = network
        self.player_num = self.network.get_player_num()
        print("You are player", self.player_num)

        # Set up display window
        pygame.display.set_caption("A Game of Shapes - Player " + str(self.player_num))     # NOTE: Display player num here?
        screen_res = (WINDOW_WIDTH, WINDOW_HEIGHT)
        self.screen = pygame.display.set_mode(
            screen_res, flags=pygame.RESIZABLE)
        
        # Set up font
        pygame.font.init()
        self.game_font = pygame.font.SysFont("Verdana", 60)

        # Set up gameplay map
        self.map = Map(self.screen, self.player_num)

        # Represents the state of game
        # Modified by server and sent to clients
        self.gamestate = self.network.get_gamestate()
        is_turn = self.gamestate.is_players_turn(self.player_num)

        # The gamephase determines whether game is started, over, etc.
        self.gamephase = "start_screen"

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

        # Keep track of user's cursor. Updates every frame
        self.mouse_position = pygame.mouse.get_pos()

        # Show waiting screen until other player connects
        self.waiting_screen()
        # Start the game
        self.game_loop()

    def game_loop(self):
        """
        Loop until window is closed.
        """
        while True:
            self.event_loop()
            self.update()
            self.draw()


    def event_loop(self):
        """
        Handle user input.

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
                self.map.handle_hover(self.mouse_position)

            # Only process clicks if it's this player's turn
            if self.gamestate.is_players_turn(self.player_num):
                if self.turn["phase"] == PLACE_TILES:
                    pass
                elif self.turn["phase"] == GAME_OVER:
                    pass
                else: # Attack!
                    # User clicks button
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.turn = self.map.handle_click(self.mouse_position, self.turn)
                    # User presses a key
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.turn["phase"] == SHOW_MOVE_RANGE
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
        self.time = self.clock.tick(30)
        self.mouse_position = pygame.mouse.get_pos()


    def update_gamestate(self):
        """
        Pull in new information from server and apply changes.
        """
        new_gamestate = self.network.get_gamestate()

        self.update_health(new_gamestate)
        self.update_positions(new_gamestate)

        self.turn["attack"] = None
        self.turn["move"] = None

        self.gamestate = new_gamestate

    # TODO: Create display function?

    def update_health(self, new_gamestate):
        """
        Update units with any health changes.
        """
        if new_gamestate.unit_health != self.gamestate.unit_health:
            for unit_type, health in new_gamestate.unit_health.items():
                unit = self.map.get_unit_by_type(unit_type)
                if unit:
                    unit.change_health(health)
                    if not unit.is_alive:
                        self.map.kill_unit(unit)

    def update_positions(self, new_gamestate):
        """
        Update units with changes in position.
        """
        if new_gamestate.unit_locations != self.gamestate.unit_locations:
            # Update map with any moved units
            for unit_type, location in new_gamestate.unit_locations.items():
                if location:
                    col, row = location
                    unit = self.map.get_unit_by_type(unit_type)
                    self.map.move(unit, col, row)

    def draw(self):
        """
        Draw graphics and display on screen.
        """
        self.screen.fill(colors.lightgray)

        # Display player statistics
        self.display_statistics()
        self.display_help()


        # Display game board
        self.map.draw()

        pygame.display.update()

    def display_statistics(self):
        """
        Display player information.
        """
        #TODO:  Generalize the placement of text.
        #       Create function for reused code.
        #       Set alignment of text.

        # Font size is equal to line spacing 
        SIZE = 20

        font = pygame.font.SysFont("Verdana", SIZE)

        # Display player turn
        is_turn = self.gamestate.is_players_turn(self.player_num)
        turn_text = ""
        text_color = ""
        if is_turn:
            turn_text = "Your Turn"
            text_color = colors.darkgreen
        else:
            turn_text = "Enemy Turn"
            text_color = colors.darkred
        textsurface = font.render(turn_text, False, text_color)
        text_rect = textsurface.get_rect(center=[WINDOW_WIDTH/2, SIZE*3])
        self.screen.blit(textsurface, text_rect)

        # Display unit statistics
        if self.player_num == 1:
            # Display "Unit Information"
            location = [20, SIZE*5]  # Beginning of unit info.
            textsurface = font.render("Unit Info", False, colors.white)
            self.screen.blit(textsurface, location)
            for unit in self.map.players_units:
                # Increment horizontal placement
                location[1] += SIZE
                health = str(unit.health) + "/" + str(unit.max_health)
                textsurface = font.render(unit.archetype + ": " + health, False, unit.color)
                self.screen.blit(textsurface, location)

            # Display "Enemy Unit Information"
            location = [self.screen.get_width() - 150, SIZE*5]  # Beginning of unit info.
            textsurface = font.render("Enemy Info", False, colors.white)
            self.screen.blit(textsurface, location)
            for unit in self.map.enemy_units:
                # Increment horizontal placement
                location[1] += SIZE
                health = str(unit.health) + "/" + str(unit.max_health)
                textsurface = font.render(unit.archetype + ": " + health, False, unit.color)
                self.screen.blit(textsurface, location)

        elif self.player_num == 2:
             # Display "Unit Information"
            location = [self.screen.get_width() - 150, SIZE*5]  # Beginning of unit info.
            textsurface = font.render("Unit Info", False, colors.white)
            self.screen.blit(textsurface, location)
            for unit in self.map.players_units:
                # Increment horizontal placement
                location[1] += SIZE
                health = str(unit.health) + "/" + str(unit.max_health)
                textsurface = font.render(unit.archetype + ": " + health, False, unit.color)
                self.screen.blit(textsurface, location)

            # Display "Enemy Information"
            location = [20, SIZE*5]  # Beginning of unit info.
            textsurface = font.render("Enemy Info", False, colors.white)
            self.screen.blit(textsurface, location)
            for unit in self.map.enemy_units:
                # Increment horizontal placement
                location[1] += SIZE
                health = str(unit.health) + "/" + str(unit.max_health)
                textsurface = font.render(unit.archetype + ": " + health, False, unit.color)
                self.screen.blit(textsurface, location)

    def display_help(self):
        """
        Display help text.
        """
        LOCATION = [0,WINDOW_HEIGHT-30]
        SIZE = 18
        font = pygame.font.SysFont("Verdana", SIZE)
        phase_text = ""
        
        # Change help text based on phase
        if self.turn["phase"] == SHOW_MOVE_RANGE:
            phase_text = "HELP: Select a unit by clicking on it with your mouse."
        elif self.turn["phase"] == MOVING:
            phase_text = "HELP: Choose a tile to move your unit to."
        elif self.turn["phase"] == ATTACKING:
            phase_text = "HELP: Attack by clicking an emeny unit"
        textsurface = font.render(phase_text, False, colors.white)
        self.screen.blit(textsurface, LOCATION)
        
    def waiting_screen(self):
        """
        Display a waiting message until
        other client connects.
        """
        self.network.send_command("start")
        reply = self.network.receive()
        self.gamestate = self.network.get_gamestate()

        while not self.gamestate.ready():
            # Update events so window can be closed
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    print("Exiting game...")
                    self.network.close()
                    pygame.quit()
                    sys.exit(0)

            # Display waiting text
            self.screen.fill(colors.darkgray)
            textsurface = self.game_font.render("Waiting...", False, colors.white)
            text_rect = textsurface.get_rect(center=(WINDOW_CENTER))
            self.screen.blit(textsurface, text_rect)
            pygame.display.update()

            # Update gamestate to check if other player is connected
            self.gamestate = self.network.get_gamestate()
