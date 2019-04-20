"""
File: gamestate.py
Programmers: Fernando Rodriguez, Charles Davis, Paul Rogers

Represents the game board and state of
each tile. The GameState object is
sent to the server and passed to the
other client. 

    t -- tile_type
        0 is blank
        1 is health
        2 is harm
        3 is slowdown
    u -- unit_type
        0 is blank
        1 is player1, unit1
        2 is player1, unit2
        3 is player1, unit3
        4 is player2, unit1
        5 is player2, unit2
        6 is player2, unit3

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