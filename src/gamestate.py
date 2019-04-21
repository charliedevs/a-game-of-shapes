"""
File: gamestate.py
Programmers: Fernando Rodriguez, Charles Davis, Paul Rogers

"""
import enum

class GameState:

    def __init__(self):
        # Set to true if two clients are connected
        self.ready = False

        # Keeps track of player turn
        self.turn = {1 : True, 2 : False}

        # Holds unit locations
        # 1-3 are player 1's, 4-6 are player 2's
        self.locations = {
            1 : None,
            2 : None,
            3 : None,
            4 : None,
            5 : None,
            6 : None
        }

    def connected(self):
        return self.ready

    def is_players_turn(self, player_num):
        return self.turn[player_num]
    
    def change_turns(self):
        for player, is_turn in turn.items():
            if is_turn:
                turn[player] = False
            else:
                turn[player] = True

    def move(self, move):
        # move is {unit_type : [col, row]}
        unit_type, pos = move.popitem()
        self.locations[unit_type] = pos

    def winner(self):
        pass

    def reset(self):
        for player_moved in self.turn_completed:
            player_moved = False