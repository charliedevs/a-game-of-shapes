"""
File: unit.py
Programmers: Fernando Rodriguez, Charles Davis, Paul Rogers
"""
#import pygame
import src.colors as colors


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
        health, attack_power, speed, attack_range = 0, 0, 0, 0

        if self.is_triangle():
            max_health = 8
            attack_power = 1
            attack_range = 3
            speed = 5
            color = colors.green
            archetype = "triangle"
        elif self.is_diamond():
            max_health = 10
            attack_power = 3
            attack_range = 1
            speed = 2
            color = colors.red
            archetype = "diamond"
        elif self.is_circle():
            max_health = 6
            attack_power = 4
            attack_range = 1
            speed = 3
            color = colors.blue
            archetype = "circle"

        self.max_health = max_health
        self.health = max_health
        self.attack_power = attack_power
        self.attack_range = attack_range
        self.speed = speed
        self.is_moving = False
        self.is_alive = True
        # pos = [col, row]
        self.pos = [None, None]
        self.color = color
        self.archetype = archetype

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

    def attack(self, enemy_unit):
        """
        Effects health of given unit.
        
        Arguments:
            enemy_unit {Unit} -- The unit to attack
        """
        enemy_unit.reduce_health(self.attack_power)


    def get_range(self, range_type, max_col, max_row):
        """
        Returns a list of tiles the unit can move to.

        Arguments:
            range_type {string} -- Range type to calculate (attack, move)
            max_col {int}       -- Number of columns
            max_row {int}       -- Number of rows

        """
        #Determine range type based on input
        if range_type == "attack":
            unit_range = self.attack_range
        elif range_type == "move":
            unit_range = self.speed
        else:
            return []

        # Create list of tiles
        # Unit pos is [col, row]
        range_list = []
        # Add current pos of unit to list
        range_list.append(self.pos)

        # Loop for range of points within speed
        for s in range(1, unit_range + 1):
            # Add speed to col i.e. right
            possible_pos = [self.pos[0] + s, self.pos[1]]
            if not possible_pos[0] >= max_col:
                range_list.append(possible_pos)

            # Subtract speed from col i.e. left
            possible_pos = [self.pos[0] - s, self.pos[1]]
            if not possible_pos[0] < 0:
                range_list.append(possible_pos)

            # Add speed to row i.e. down
            possible_pos = [self.pos[0], self.pos[1] + s]
            if not possible_pos[1] >= max_row:
                range_list.append(possible_pos)

            # Subtract speed from row i.e. up
            possible_pos = [self.pos[0], self.pos[1] - s]
            if not possible_pos[1] < 0:
                range_list.append(possible_pos)

            # Loop for corners and inbetweens
            for i in range(1, unit_range + 1):
                # Add speed to col and row i.e. bottom right
                possible_pos = [self.pos[0] + s, self.pos[1] + i]
                if not (possible_pos[0] >= max_col or possible_pos[1] >= max_row):
                    range_list.append(possible_pos)

                # Subtract speed to col and row i.e. top left
                possible_pos = [self.pos[0] - s, self.pos[1] - i]
                if not (possible_pos[0] < 0 or possible_pos[1] < 0):
                    range_list.append(possible_pos)
                
                # i.e. top right
                possible_pos = [self.pos[0] + s, self.pos[1] - i]
                if not (possible_pos[0] >= max_col or possible_pos[1] < 0):
                    range_list.append(possible_pos)
                
                # i.e. bottom left
                possible_pos = [self.pos[0] - s, self.pos[1] + i]
                if not (possible_pos[0] < 0 or possible_pos[1] >= max_row):
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
