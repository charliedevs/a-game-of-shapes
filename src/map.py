"""
File: map.py
Programmers: Fernando Rodriguez, Charles Davis, Paul Rogers
"""
import pygame

import src.colors as colors
from src.unit import Unit
from src.grid import Grid
from src.unit import Unit

#########################################################################
# CONSTANTS

# Tile size
TILE_WIDTH = 23
TILE_HEIGHT = 23
TILE_MARGIN = 2

# Units per player
MAX_UNITS = 3

# Move phases
NOT_TURN = 0
SHOW_MOVE_RANGE = 1
MOVING = 2
ATTACKING = 3
END_TURN = 4

#########################################################################

class Map:
    """
    The surface on which gameplay occurs.
    
    Comprised of a grid of tiles, where each tile
    has a tile_type and a unit_type. Units move
    across tiles and are affected by tile_type.

    """

    def __init__(self, screen, player_num):
        """
        Set up tile grid and units.

        
        Arguments:
            screen {pygame.Surface} -- The main display window
            player_num {int} -- The player identifier; 1 or 2
        """

        self.screen = screen
        self.player_num = player_num

        # The grid is a 2D array with columns and rows
        self.grid = Grid()
        cols = self.grid.cols
        rows = self.grid.rows

        # TODO: create function to return a tile, and one to get tile based on mouse_position

        # The dimensions of each tile
        self.tile_w = TILE_WIDTH
        self.tile_h = TILE_HEIGHT
        self.margin = TILE_MARGIN

        # Keep track of unit that was last clicked on
        self.selected_unit = None

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

        # Set up player units
        self.all_units = []
        self.players_units = []
        self.initialize_units()



    def handle_hover(self, mouse_position):
        # highlights tile hovered over
        pass

    def highlight_tiles(self, unit, range_type):
        if range_type == "move":
            tile_type = 3
        elif range_type == "attack":
            tile_type = 4
        movable_list = unit.get_range(range_type, self.grid.cols, self.grid.rows)
        print(movable_list)
        for position in movable_list:
            col = position[0]
            row = position[1]
            self.grid.set_tile_type(col, row, tile_type)


    def remove_highlight(self, highlight_type):
        for row in range(self.grid.rows):
            for col in range(self.grid.cols):
                tile_type = self.grid.get_tile_type(col, row)
                if tile_type == highlight_type:
                    self.grid.set_tile_type(col, row, 0)


    def handle_click(self, mouse_position, turn):
        """
        Process user clicks on game tiles.

        Arguments:
            mouse_position {(float, float)} -- The (x, y) position of mouse on window
            turn {dict} -- Contains keys move and attack. Both are lists: [unit_type, col, row]
        """

        if not self.mouse_position_inside_map(mouse_position):
            return turn

        column, row = self.determine_tile_from_mouse_position(mouse_position)
        print("[Debug]: Click", mouse_position, "Grid coords:", column, row)

        clicked_unit = None
        for unit in self.players_units:
            if unit.pos == [column, row]:
                clicked_unit = unit

        # If player hasn't moved yet
        if turn["phase"] == SHOW_MOVE_RANGE:
            if clicked_unit:
                self.highlight_tiles(clicked_unit, "move")
                self.selected_unit = clicked_unit
                turn["phase"] = MOVING

        # Player has clicked unit to move
        elif turn["phase"] == MOVING:
            if self.grid.get_tile_type(column, row) == 3:# 3 == movable
                movable_unit = self.selected_unit
                if movable_unit.pos == [column, row]:
                    # Clicked on self
                    turn["phase"] = SHOW_MOVE_RANGE
                else:
                    move = self.move(movable_unit, column, row)
                    if move:
                        turn["move"] = move
                        turn["phase"] = ATTACKING
                        # highlight attackable tiles
                        self.highlight_tiles(movable_unit, "attack")
                    else:
                        # move is invalid
                        turn["phase"] = SHOW_MOVE_RANGE

                self.remove_highlight(3) # remove movable tile
                self.selected_unit = None

        elif turn["phase"] == ATTACKING:
            # show attackable range
            # if enemy in attackable range, process click in range as attack on enemy
            self.remove_highlight(4)    # remove attack highlight
            turn["phase"] = END_TURN

        return turn

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


    def draw(self):
        """
        Draw map onto surface.
        """

        self.surface.fill(colors.white)

        # Loop through the grid data structure
        for row in range(self.grid.rows):
            for col in range(self.grid.cols):

                unit_type = self.grid.get_unit_type(col, row)
                unit = None
                if unit_type != 0:
                    unit = self.get_unit_by_type(unit_type)
                tile_type = self.grid.get_tile_type(col, row)

                # Determine color of tiles
                tile_color = colors.darkgray
                if tile_type == 1:
                    tile_color = colors.green
                elif tile_type == 2:
                    tile_color = colors.red
                elif tile_type == 3:
                    tile_color = colors.yellow
                elif tile_type == 4:
                    tile_color = colors.purple

                # Display tiles
                rect = pygame.draw.rect(self.surface,
                                        tile_color,
                                        [(self.margin + self.tile_w) * col + self.margin,
                                         (self.margin + self.tile_h) * row + self.margin,
                                         self.tile_w,
                                         self.tile_h])

                # Determine unit color and shape
                # using tile's rect as reference
                unit_color = colors.white
                pointlist = None
                if unit:
                    if unit.is_triangle():
                        # Green triangle
                        unit_color = colors.darkgreen
                        pointlist = [
                            rect.midtop,
                            rect.bottomleft,
                            rect.bottomright
                        ]
                    elif unit.is_diamond():
                        # Red diamond
                        unit_color = colors.darkred
                        pointlist = [
                            rect.midtop,
                            rect.midleft,
                            rect.midbottom,
                            rect.midright
                        ]
                    elif unit.is_circle():
                        # Blue circle
                        unit_color = colors.darkblue
                        pos = rect.center
                        radius = rect.width / 2

                    # Draw unit
                    if unit_color == colors.white:
                        continue # No unit in this tile
                    if pointlist is not None:
                        pygame.draw.polygon(
                            self.surface,
                            unit_color,
                            pointlist
                        )
                    else:
                        pygame.draw.circle(
                            self.surface,
                            unit_color,
                            pos,
                            int(radius)
                        )

    def get_rect(self):
        """
        Return rect with (x, y) relative to window.

        Returns:
            Rect -- The rectangle bounding map grid
        """

        x, y = self.surface.get_abs_offset()
        w, h = self.map_size
        return pygame.Rect(x, y, w, h)

    def move(self, unit, col, row):
        """
        Move unit to given location if possible.

        Arguments:
            unit {Unit} -- The unit to move
            col {int}   -- A column on the grid
            row {int}   -- A row on the grid
        """
        move = None
        if self.grid.get_unit_type(col, row) == 0:
            # Set old tile to tile_type of blank
            self.grid.set_unit_type(unit.pos[0], unit.pos[1], 0) #TODO: abstract this into GameState class
            # Update grid with new unit position
            self.grid.set_unit_type(col, row, unit.type)
            unit.pos = [col, row]
            move = [unit.type, col, row]

        return move

    def attack(self, col, row, unit):
        pass


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

        # Place units on grid
        left_column = 0
        right_column = self.grid.cols -1
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

    def clear(self):
        # Resets the map.
        #
        # Removes special tile_types and
        # TODO: resets unit positions.

        for row in range(self.grid.rows):
            for col in range(self.grid.cols):
                self.grid.set_tile_type(col, row, 0)

        self.initialize_units()

        print("[Debug]: Map reset.")
