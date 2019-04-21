"""
File: unit.py
Programmers: Fernando Rodriguez, Charles Davis, Paul Rogers
"""
#import pygame

class Unit:
    """
    A player's unit on the gameboard.

    Has attributes: health, speed, attack_power
    """

    def __init__(self, unit_type):
        """
        Sets up player unit.

        Arguments:
            unit_type -- an integer; 1, 2, or 3
        """
        self.unit_type = unit_type

        # Determine unit attributes
        health, attack_power, speed = 0, 0, 0
        if self.unit_type == 1 or self.unit_type == 4:
            # Low health, low attack, low speed
            health = 5
            attack_power = 1
            speed = 2
        elif self.unit_type == 2 or self.unit_type == 5:
            # Low health, low attack, low speed
            health = 8
            attack_power = 2
            speed = 3
        else:
            # High health, high attack, high speed
            health = 10
            attack_power = 4
            speed = 5

        self.health = health
        self.health_max = health + 1
        self.attack_power = attack_power
        self.speed = speed
        self.is_alive = True

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
