"""
File: gamestate.py
Programmers: Fernando Rodriguez, Charles Davis, Paul Rogers


"""
import enum

class GameState:

    def __init__(self):
        # Set to true if two clients are connected
        self.ready = False

        # Holds the current moves made by each player
        self.moves = {1 : None, 2 :  None}

        # Keeps track of if turns are completed for a round
        self.turn_completed = {1 : False, 2 : False}

    def connected(self):
        return self.ready

    def both_players_moved(self):
        return self.turn_completed[1] and self.turn_completed[2]

    def winner(self):
        pass