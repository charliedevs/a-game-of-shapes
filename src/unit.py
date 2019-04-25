"""
File: unit.py
Programmers: Fernando Rodriguez, Charles Davis, Paul Rogers
"""
#import pygame



#########################################################################
# CONSTANTS

NO_UNIT = 0

P1_TRIANGLE = 1
P1_DIAMOND = 2
P1_CIRCLE = 3

P2_TRIANGLE = 4
P2_DIAMOND = 5
P2_CIRCLE = 6

#########################################################################

class Unit:
    """
    A player's unit on the gameboard.

    Has attributes: health, speed, attack_power
    """

    def __init__(self, unit_type):
        """
        Sets up player unit.

        Arguments:
            unit_type -- Determines player number and unit attributes
        """
        self.type = unit_type

        # Determine unit attributes
        health, attack_power, speed = 0, 0, 0

        if self.is_triangle():
            health = 8
            attack_power = 1
            speed = 5
        elif self.is_diamond():
            health = 10
            attack_power = 3
            speed = 2
        elif self.is_circle():
            health = 6
            attack_power = 4
            speed = 3

        self.health = health
        self.health_max = health + 1
        self.attack_power = attack_power
        self.speed = speed
        self.is_alive = True
        self.pos = [None, None]

    def reduce_health(self, amount):
        """
        Subtracts the given amount from health.

        Arguments:
            amount {int} -- The health to remove
        """
        self.health = self.health - amount

        if self.health <= 0:
            self.is_alive = False

    def add_health(self, amount):
        """
        Heals the unit by given amount.

        Arguments:
            amount {int} -- The health to add
        """
        self.health = self.health + amount

        if self.health > self.health_max:
            self.health = self.health_max

    def get_move_range(self, max_col, max_row):
        # TODO: Add for loops to grab everything within range
        #       Currently grabs tiles equidistant from the origin based on speed
        """
        Returns a list of tiles the unit can move to.

        Arguments:
            max_col {int} -- Number of columns
            max_row {int} -- Number of rows

        """
        # Create list of tiles
        # Unit pos is [col, row]
        range_list = []

        # Add speed to col i.e. right
        possible_pos = [self.pos[0] + self.speed, self.pos[1]]
        if not possible_pos[0] >= max_col:
            range_list.append(possible_pos)

        # Subtract speed from col i.e. left
        possible_pos = [self.pos[0] - self.speed, self.pos[1]]
        if not possible_pos[0] < 0:
            range_list.append(possible_pos)

        # Add speed to row i.e. down
        possible_pos = [self.pos[0], self.pos[1] + self.speed]
        if not possible_pos[1] >= max_row:
            range_list.append(possible_pos)

        # Subtract speed from row i.e. up
        possible_pos = [self.pos[0], self.pos[1] - self.speed]
        if not possible_pos[1] < 0:
            range_list.append(possible_pos)

        # Add speed to col and row i.e. bottom right
        possible_pos = [self.pos[0] + self.speed, self.pos[1] + self.speed]
        if not (possible_pos[0] >= max_col or possible_pos[1] >= max_row):
            range_list.append(possible_pos)

        # Subtract speed to col and row i.e. top left
        possible_pos = [self.pos[0] - self.speed, self.pos[1] - self.speed]
        if not (possible_pos[0] < 0 or possible_pos[1] < 0):
            range_list.append(possible_pos)
        
        # i.e. top right
        possible_pos = [self.pos[0] + self.speed, self.pos[1] - self.speed]
        if not (possible_pos[0] >= max_col or possible_pos[1] < 0):
            range_list.append(possible_pos)
        
         # i.e. bottom left
        possible_pos = [self.pos[0] - self.speed, self.pos[1] + self.speed]
        if not (possible_pos[0] < 0 or possible_pos[1] <= max_row):
            range_list.append(possible_pos)

        return range_list

    def is_triangle(self):
        return self.type == P1_TRIANGLE or self.type == P2_TRIANGLE

    def is_diamond(self):
        return self.type == P1_DIAMOND or self.type == P2_DIAMOND

    def is_circle(self):
        return self.type == P1_CIRCLE or self.type == P2_CIRCLE

    def is_players_unit(self, player_num):
        if self.type in range(1, 4) and player_num == 1:
            return True
        if self.type in range(4, 7) and player_num == 2:
            return True

        return False