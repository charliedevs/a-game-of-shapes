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
        self.game_font = pygame.font.Font(GAME_FONT, 40)

        # Set up gameplay map
        self.map = Map(self.screen, self.player_num, self.network)

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

        # Let the starting player begin moving units
        if is_turn:
            self.turn["phase"] = SELECT_UNIT_TO_MOVE

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
                self.exit_game()

            # Only process events if it's your turn
            if self.gamestate.is_players_turn(self.player_num):
                # User hovers over tile
                if event.type == pygame.MOUSEMOTION:
                    self.map.handle_hover(self.mouse_position)
                # User is placing tiles
                if self.turn["phase"] == PLACE_TILES:
                    pass # TODO: Add tile placement
                else: # Attack!
                    # User clicks button
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.turn = self.map.handle_click(self.mouse_position, self.turn)
                    # User presses a key
                    # TODO: Delete or implement keydown
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.turn["phase"] == END_TURN

    def update(self):
        """
        Update variables that change every frame.
        """
        self.time = self.clock.tick(60)
        self.mouse_position = pygame.mouse.get_pos()

        # Other player's turn
        if not self.gamestate.is_players_turn(self.player_num):
            rps_in_session = self.network.check_for_rps()
            if rps_in_session:
                self.map.rps_loop()
                # self.network.finish_rps()
            players_turn = self.network.request_turn()
            if players_turn == self.player_num:
                self.update_gamestate()
                self.turn["phase"] = SELECT_UNIT_TO_MOVE

        # Check if turn ended
        if self.turn["phase"] == END_TURN:
            # Send moves and attacks made to server
            self.network.send_turn(self.turn)
            self.gamestate.change_turns()
            self.turn["phase"] = NOT_TURN

        # Check if someone has won
        if self.gamestate.game_is_over:
            self.gameover()

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
        SIZE = 16

        font = pygame.font.Font(GAME_FONT, SIZE)
        turn_font = pygame.font.Font(GAME_FONT, SIZE+10)

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
        textsurface = turn_font.render(turn_text, False, text_color)
        text_rect = textsurface.get_rect(center=[WINDOW_WIDTH/2, SIZE*3])
        self.screen.blit(textsurface, text_rect)

        # Display unit statistics
        if self.player_num == 1:
            # Display "Unit Information"
            location = [20, SIZE*5]  # Beginning of unit info.
            textsurface = font.render("Your Health", False, colors.white)
            self.screen.blit(textsurface, location)
            for unit in self.map.players_units:
                # Increment horizontal placement
                location[1] += SIZE + 8
                health = str(unit.health) + "/" + str(unit.max_health)
                textsurface = font.render(unit.archetype + ": " + health, False, unit.color)
                self.screen.blit(textsurface, location)

            # Display "Enemy Unit Information"
            location = [self.screen.get_width() - 150, SIZE*5]  # Beginning of unit info.
            textsurface = font.render("Enemy Health", False, colors.white)
            self.screen.blit(textsurface, location)
            for unit in self.map.enemy_units:
                # Increment horizontal placement
                location[1] += SIZE + 8
                health = str(unit.health) + "/" + str(unit.max_health)
                textsurface = font.render(unit.archetype + ": " + health, False, unit.color)
                self.screen.blit(textsurface, location)

        elif self.player_num == 2:
             # Display "Unit Information"
            location = [self.screen.get_width() - 150, SIZE*5]  # Beginning of unit info.
            textsurface = font.render("Your Health", False, colors.white)
            self.screen.blit(textsurface, location)
            for unit in self.map.players_units:
                # Increment horizontal placement
                location[1] += SIZE + 8
                health = str(unit.health) + "/" + str(unit.max_health)
                textsurface = font.render(unit.archetype + ": " + health, False, unit.color)
                self.screen.blit(textsurface, location)

            # Display "Enemy Information"
            location = [20, SIZE*5]  # Beginning of unit info.
            textsurface = font.render("Enemy Health", False, colors.white)
            self.screen.blit(textsurface, location)
            for unit in self.map.enemy_units:
                # Increment horizontal placement
                location[1] += SIZE + 8
                health = str(unit.health) + "/" + str(unit.max_health)
                textsurface = font.render(unit.archetype + ": " + health, False, unit.color)
                self.screen.blit(textsurface, location)

    def display_help(self):
        """
        Display help text.
        """
        LOCATION = [0,WINDOW_HEIGHT-25]
        SIZE = 12
        font = pygame.font.Font(GAME_FONT, SIZE)
        phase_text = ""
        
        # Change help text based on phase
        if self.turn["phase"] == SELECT_UNIT_TO_MOVE:
            phase_text = "HELP: Select a unit to move by clicking on it with your mouse."
        elif self.turn["phase"] == MOVING:
            phase_text = "HELP: Click a tile to move your unit, or click same unit to deselect."
        elif self.turn["phase"] == ATTACKING:
            phase_text = "HELP: Attack by clicking an enemy unit. (Must attack if enemy is in range)"
        elif self.turn["phase"] == NOT_TURN:
            phase_text = "HELP: Wait for your enemy to make their move."

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
                    self.exit_game()

            # Display waiting text
            self.screen.fill(colors.darkgray)
            textsurface = self.game_font.render("Waiting for player 2...", False, colors.white)
            text_rect = textsurface.get_rect(center=(WINDOW_CENTER))
            self.screen.blit(textsurface, text_rect)
            pygame.display.update()

            # Update gamestate to check if other player is connected
            self.gamestate = self.network.get_gamestate()

    def gameover(self):
        """
        Gameover loop. 
        TODO: Allow clients to restart game.
        """
        self.network.send_turn(self.turn)
        # Loop until player resets or quits
        while True:

            # Show text and how to reset
            self.display_endgame_results()

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.exit_game()

                # Press space to restart or esc to exit
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        # Tell server that you're ready
                        self.network.send_command("start")
                    elif event.key == pygame.K_ESCAPE:
                        self.exit_game()

            # Update gamestate to check if other player is ready
            self.gamestate = self.network.get_gamestate()

        # Clear the map
        self.map.reset()    

        # Determine turn to start back with
        is_turn = self.gamestate.is_players_turn(self.player_num)
        if is_turn:
            self.turn["phase"] = SELECT_UNIT_TO_MOVE

    def display_endgame_results(self):
        """
        Display winning/losing text.
        """
        self.screen.fill(colors.lightgray)

        # Show results
        if self.gamestate.winner == self.player_num:
            textsurface = self.game_font.render("You won!", False, colors.darkgreen)
        else:
            textsurface = self.game_font.render("You lost...", False, colors.darkred)
        text_rect = textsurface.get_rect(center=(WINDOW_CENTER))
        self.screen.blit(textsurface, text_rect)

        pygame.display.update()

    def exit_game(self):
        print("Exiting game...")
        self.network.close()
        pygame.quit()
        sys.exit(0)