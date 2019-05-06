"""
File: map.py
Programmers: Fernando Rodriguez, Charles Davis

"""
# TODO: Abstract tiles into a class holding tile_type and whether the tile is hovered over

import pygame
import sys
import time
import random

# Constants
import src.colors as colors
from src.constants import *

# Classes
from src.grid import Grid
from src.unit import Unit
from src.rockpaperscissors import RPS

class Map:
    """
    The surface on which gameplay occurs.
    
    Comprised of a grid of tiles, where each tile
    has a tile_type and a unit_type. Units move
    across tiles and are affected by tile_type.

    """

    def __init__(self, screen, player_num, network):
        """
        Set up tile grid and units.

        
        Arguments:
            screen {pygame.Surface} -- The main display window
            player_num {int} -- The player identifier; 1 or 2
            network {Network} -- Connection to the server
        """

        self.screen = screen
        self.player_num = player_num
        self.network = network

        # The grid is a 2D array with columns and rows
        self.grid = Grid()
        cols = self.grid.cols
        rows = self.grid.rows

        # The dimensions of each tile
        self.tile_w = TILE_WIDTH
        self.tile_h = TILE_HEIGHT
        self.margin = TILE_MARGIN

        # Full map size in pixels (calculated from grid and tile sizes)
        map_w = (cols * (self.tile_w + self.margin)) + self.margin
        map_h = (rows * (self.tile_h + self.margin)) + self.margin
        self.map_size = (map_w, map_h)

        # Determine placement of map within display window
        map_x = (self.screen.get_size()[0] // 2) - (self.map_size[0] // 2)
        map_y = (self.screen.get_size()[1] // 2) - (self.map_size[1] // 2)
        map_rect = pygame.Rect(map_x, map_y, map_w, map_h)

        # Create map surface
        self.surface = self.screen.subsurface(map_rect)

        # Keep track of unit that was last clicked on
        # and last tile hovered over
        self.selected_unit = None
        self.hover_location = None

        # Set up player units
        self.all_units = []
        self.players_units = []
        self.enemy_units = []
        self.initialize_units()

        # The rock paper scissors class
        self.rps = RPS(self.screen)
        

    def handle_hover(self, mouse_position):
        """
        Highlight tile hovered over by user.
        """
        if self.mouse_position_inside_map(mouse_position):
            # Record position of hovered tile
            tile_col, tile_row = self.determine_tile_from_mouse_position(mouse_position)
            self.hover_location = (tile_col, tile_row)
        else:
            # Remove hover if off map
            self.hover_location = None

    def handle_click(self, mouse_position, turn):
        """
        Process user clicks on game tiles.
        Modifies turn and returns back to Game class.

        TODO: Separate different levels of abstraction into separate methods.

        Arguments:
            mouse_position {(float, float)} -- The (x, y) position of mouse on window
            turn {dict} -- Contains keys move and attack. Both are lists: [unit_type, col, row]
        """

        if not self.mouse_position_inside_map(mouse_position):
            return turn

        clicked_column, clicked_row = self.determine_tile_from_mouse_position(mouse_position)

        clicked_unit = None
        for unit in self.players_units:
            if unit.pos == [clicked_column, clicked_row]:
                clicked_unit = unit

        # Player hasn't moved yet
        if turn["phase"] == SELECT_UNIT_TO_MOVE:
            if clicked_unit:
                self.highlight_tiles(clicked_unit, "move")
                self.selected_unit = clicked_unit
                turn["phase"] = MOVING

        # Player has clicked unit to move
        elif turn["phase"] == MOVING:
            if self.grid.tile_in_move_range(clicked_column, clicked_row):
                movable_unit = self.selected_unit
                # Allow user to click on self to back out of moving
                if movable_unit.pos == [clicked_column, clicked_row]:
                    turn["phase"] = SELECT_UNIT_TO_MOVE
                else:
                    move = self.move(movable_unit, clicked_column, clicked_row)
                    if move:
                        turn["move"] = move

                        # Go into attack phase if enemy is within range
                        if self.enemy_in_attack_range():
                            turn["phase"] = ATTACKING
                            self.highlight_tiles(movable_unit, "attack")
                        else:
                            # No enemy in range, so turn is over
                            self.selected_unit = None
                            turn["phase"] = END_TURN
                    else:
                        # Move is invalid, allow client to select another unit to move
                        turn["phase"] = SELECT_UNIT_TO_MOVE

                self.remove_highlight("move")
                
        # Player is attacking
        elif turn["phase"] == ATTACKING:
            enemy_unit = self.get_clicked_enemy(clicked_column, clicked_row)
            if enemy_unit:
                # Rock paper scissors!
                winner = self.rps_loop("attacker")

                # If this player wins (or ties), apply attack
                if winner == self.player_num:
                    turn["attack"] = self.attack(enemy_unit)

                # End attack
                self.remove_highlight("attack")
                turn["phase"] = END_TURN
                self.selected_unit = None

        return turn

    def move(self, unit, col, row):
        """
        Move unit to given location if possible.

        Arguments:
            unit {Unit} -- The unit to move
            col {int}   -- A column on the grid
            row {int}   -- A row on the grid
        """
        move = None
        if unit:
            if self.grid.get_unit_type(col, row) == BLANK:
                # Set old tile to unit_type of blank
                self.grid.set_unit_type(unit.col(), unit.row(), BLANK)
                # Update grid with new unit position
                self.grid.set_unit_type(col, row, unit.type)
                unit.pos = [col, row]
                move = [unit.type, col, row]

        return move

    def attack(self, enemy_unit):
        """
        Attack an enemy unit.
        """
        self.selected_unit.attack(enemy_unit)
        if not enemy_unit.is_alive:
            self.kill_unit(enemy_unit)
        attack = [enemy_unit.type, self.selected_unit.attack_power]
        return attack

    def get_clicked_enemy(self, col, row):
        """
        Return the enemy if one exists at col, row.
        """
        clicked_enemy = None
        if self.grid.tile_in_attack_range(col, row):
            for enemy_unit in self.enemy_units:
                if enemy_unit.pos == [col, row]:
                    clicked_enemy = enemy_unit
                    break

        return clicked_enemy

    def determine_tile_from_mouse_position(self, mouse_position):
        """
        To get position relative to map, we must subtract the
        offset from the mouse position. Dividing by the tile
        size gives us the clicked tile.
        
        Arguments:
            mouse_position {(float, float)} -- Position (x, y) of mouse on game window in pixels

        Returns:
            tile_position {(int, int)} -- Column and row of tile on grid
        """
        mouse_x, mouse_y = mouse_position
        offset_x, offset_y = self.get_rect().topleft

        col = (mouse_x - offset_x) // (self.tile_w + self.margin)
        row = (mouse_y - offset_y) // (self.tile_h + self.margin)

        return (col, row)

    def highlight_tiles(self, unit, range_type):
        """
        Highlights movable or attackable tiles around given unit.
        """
        if range_type == "move":
            tile_type = MOVABLE
        elif range_type == "attack":
            tile_type = ATTACKABLE
        movable_list = unit.get_range(range_type, self.grid.cols, self.grid.rows)
        for position in movable_list:
            col = position[0]
            row = position[1]
            self.grid.set_tile_type(col, row, tile_type)

    def remove_highlight(self, range_type):
        """
        Changes highlighted tile types back to blank.
        """
        if range_type == "move":
            highlight_type = 3
        elif range_type == "attack":
            highlight_type = 4
        for row in range(self.grid.rows):
            for col in range(self.grid.cols):
                tile_type = self.grid.get_tile_type(col, row)
                if tile_type == highlight_type:
                    self.grid.set_tile_type(col, row, 0)

    def draw(self):
        """
        Draw map onto surface.
        """

        self.surface.fill(colors.white)

        # Loop through the grid data structure
        for row in range(self.grid.rows):
            for col in range(self.grid.cols):

                # Get current unit and tile
                unit_type = self.grid.get_unit_type(col, row)
                unit = None
                if unit_type != 0:
                    unit = self.get_unit_by_type(unit_type)
                tile_type = self.grid.get_tile_type(col, row)

                # Determine color of tiles
                tile_color = colors.darkgray
                if tile_type == HEALTH:
                    tile_color = colors.green
                elif tile_type == HARM:
                    tile_color = colors.purple
                elif tile_type == MOVABLE:
                    tile_color = colors.lightergrey
                elif tile_type == ATTACKABLE:
                    tile_color = colors.red

                # Display tiles
                tile_rect = pygame.draw.rect(self.surface,
                                        tile_color,
                                        [(self.margin + self.tile_w) * col + self.margin,
                                         (self.margin + self.tile_h) * row + self.margin,
                                         self.tile_w,
                                         self.tile_h])

                # Highlight hovered tile
                if self.hover_location:
                    if self.hover_location == (col, row):
                        pygame.draw.rect(self.surface,
                                     colors.get_hover_color(tile_color),
                                     tile_rect)


                # TODO: Draw units inside Unit class. Pass in tile_rect
                # Determine unit color and shape
                # using tile's rect as reference
                pointlist = None
                if unit:
                    if unit.is_triangle():
                        # Green triangle
                        pointlist = [
                            tile_rect.midtop,
                            tile_rect.bottomleft,
                            tile_rect.bottomright
                        ]
                    elif unit.is_diamond():
                        # Red diamond
                        pointlist = [
                            tile_rect.midtop,
                            tile_rect.midleft,
                            tile_rect.midbottom,
                            tile_rect.midright
                        ]
                    elif unit.is_circle():
                        # Blue circle
                        pos = tile_rect.center
                        radius = tile_rect.width / 2

                    # Draw unit
                    if pointlist is not None:
                        pygame.draw.polygon(
                            self.surface,
                            unit.color,
                            pointlist
                        )
                    else:
                        pygame.draw.circle(
                            self.surface,
                            unit.color,
                            pos,
                            int(radius)
                        )

    def flash_red(self):
        """
        Makes screen red for a moment.
        """
        self.screen.fill(colors.darkred)
        pygame.display.update()
        pygame.time.delay(18)

    def display_attack_result(self, result):
        """
        Result is either "hit", "block", or "kill"
        TODO: Integrate this into game in a clean way. Currently makes game hangup.
        """
        font = pygame.font.Font(GAME_FONT, 26)
        text = ""
        color = colors.darkgray
        # Determine font based on result
        if result == "hit":
            text = "Attack landed!"
        elif result == "block":
            text = "Blocked attack!"
            color = colors.blue
        elif result == "kill":
            text = self.get_random_kill_text()
            color = colors.darkred

        # Set up popup window
        text_surface = font.render(text, False, colors.lightergrey, color)
        text_rect = text_surface.get_rect()
        text_rect.center = WINDOW_CENTER

        # Display popup for 2 seconds
        self.screen.blit(text_surface, text_rect)
        pygame.display.update()
        time.sleep(2)

    def get_random_kill_text(self):
        kill_text = ""
        random_num = random.randint(1, 11)
        if random_num == 1:
            kill_text = "Fatal blow!"
        elif random_num == 2:
            kill_text = "Brutally slain!"
        elif random_num == 3:
            kill_text = "The gift of death!"
        elif random_num == 4:
            kill_text = "Man down!"
        elif random_num == 5:
            kill_text = "What a kill!"
        elif random_num == 6:
            kill_text = "Say goodbye!"
        elif random_num == 7:
            kill_text = "Adiós, muchacho!"
        elif random_num == 8:
            kill_text = "Unit killed!"
        elif random_num == 9:
            kill_text = "No shape is safe!"
        elif random_num == 10:
            kill_text = "Death!"

        return kill_text
        
    def get_rect(self):
        """
        Return rect with (x, y) relative to window.

        Returns:
            Rect -- The rectangle bounding map grid
        """

        x, y = self.surface.get_abs_offset()
        w, h = self.map_size
        return pygame.Rect(x, y, w, h)

    def get_unit_by_type(self, unit_type):
        target_unit = None

        if unit_type == 0:
            return None

        for unit in self.all_units:
            if unit.type == unit_type:
                target_unit = unit
                break
        else:
            print("[Error]: Could not get unit by type.")

        return target_unit

    def initialize_units(self):
        """
        Place all units on map in initial positions.
        """
        # Create Unit objects and add to list
        total_units = (2 * MAX_UNITS)
        for unit_type in range(1, total_units + 1):
            unit = Unit(unit_type)
            self.all_units.append(unit)

        # Determine this player's units
        for unit in self.all_units:
            if unit.is_players_unit(self.player_num):
                self.players_units.append(unit)
            else:
                self.enemy_units.append(unit)

        # Place units on grid
        left_column = 0
        right_column = self.grid.cols - 1
        top_row = 0
        middle_row = self.grid.rows // 2
        bottom_row = self.grid.rows - 1
        positions = {
            1 : (left_column, top_row),
            2 : (left_column, middle_row),
            3 : (left_column, bottom_row),
            4 : (right_column, top_row),
            5 : (right_column, middle_row),
            6 : (right_column, bottom_row)
        }
        for unit in self.all_units:
            col, row = positions[unit.type]
            unit.pos = [col, row]
            self.grid.set_unit_type(col, row, unit.type)

    def mouse_position_inside_map(self, mouse_position):
        """
        Returns true if mouse is positioned over map.
        """
        return self.get_rect().collidepoint(mouse_position)

    def enemy_in_attack_range(self):
        """
        Returns true if an enemy unit is in self.selected_unit's attack range.
        """
        is_in_range = False
        attack_range = self.selected_unit.get_range("attack", self.grid.cols, self.grid.rows)
        for enemy_unit in self.enemy_units:
            if enemy_unit.pos in attack_range:
                is_in_range = True

        return is_in_range

    def kill_unit(self, unit):
        """
        Removes given unit from unit lists.
        """
        column, row = unit.pos
        self.grid.set_unit_type(column, row, 0)
        if unit in self.all_units:
            self.all_units.remove(unit)
        if unit in self.players_units:
            self.players_units.remove(unit)
        if unit in self.enemy_units:
            self.enemy_units.remove(unit)

    def rps_loop(self, role):
        """
        Play rock paper scissors to see if attack lands.
        Parameter role can be "attacker" or "defender".
        """
        player_has_picked = False
        hand_sent = False
        winner = 0

        while winner == 0:
            # Loop until rps is over
            mouse_position = pygame.mouse.get_pos()
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    print("Exiting game...")
                    self.network.close()
                    pygame.quit()
                    sys.exit(0)

                # Only check for mouse clicks if player hasn't made a choice
                if not player_has_picked:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.rps.handle_click(mouse_position)
                        if self.rps.hand:
                            player_has_picked = True
            
            if (not hand_sent) and player_has_picked:
                self.network.send_hand(self.rps.hand)
                hand_sent = True
            elif player_has_picked:
                winner = self.network.get_rps_winner()

            # Draw RPS graphics
            self.screen.fill(colors.lightgray)
            if not player_has_picked:
                # Draw RPS graphics
                self.rps.draw(role)
            else:
                self.display_rps_waiting()
            pygame.display.update()

        # Make tie go to attacker
        if role == "attacker" and winner == 3:
            winner = self.player_num

        return winner

    def display_rps_waiting(self):
        """
        Draws waiting text for rock, paper, scissors.
        """
        font = pygame.font.Font(GAME_FONT, 24)
        textsurface = font.render("Waiting for other player's choice...", False, colors.white)
        text_rect = textsurface.get_rect(center=(WINDOW_CENTER))
        self.screen.blit(textsurface, text_rect)

    def reset(self):
        """
        Initialize the map.

        Removes special tile_types and
        resets unit health and positions.
        """
        for row in range(self.grid.rows):
            for col in range(self.grid.cols):
                self.grid.set_tile_type(col, row, 0)

        self.initialize_units()

        print("[Debug]: Map reset.")
