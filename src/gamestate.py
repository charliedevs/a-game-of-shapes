"""
File: gamestate.py
Programmers: Fernando Rodriguez, Charles Davis, Paul Rogers

"""
import enum

class GameState:

    def __init__(self):
        # Set to true if two clients are connected
        self.ready_state = {1 : False, 2 : False}

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

    def is_players_turn(self, player_num):
        return self.turn[player_num]

    def get_turn(self):
        players_turn = 0
        for player, is_turn in self.turn.items():
            if is_turn:
                players_turn = player
        return players_turn
    
    def change_turns(self):
        self.turn[1] = not self.turn[1]
        self.turn[2] = not self.turn[2]

    def move_unit(self, move):
        # move is [unit_type, col, row]
        unit_type, col, row = move
        self.locations[unit_type] = [col, row]

    def attack_unit(self, attack):
        pass

    def set_ready(self, player_num):
        self.ready_state[player_num] = True

    def ready(self):
        return all(ready for ready in self.ready_state.values())

    def winner(self):
        pass

    def reset(self):
        for player_moved in self.turn_completed:
            player_moved = False