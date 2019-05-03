"""
File: gamestate.py
Programmers: Fernando Rodriguez, Charles Davis, Paul Rogers

"""

# Max. health values
TRIANGLE_HEALTH = 4
DIAMOND_HEALTH = 5
CIRCLE_HEALTH = 3

class GameState:

    def __init__(self):
        # Set to true if two clients are connected
        self.ready_state = {1 : False, 2 : False}

        # Keeps track of player turn
        self.turn = {1 : True, 2 : False}

        # Holds locations of all units
        # 1-3 are player 1's, 4-6 are player 2's
        self.unit_locations = {
            1 : None,
            2 : None,
            3 : None,
            4 : None,
            5 : None,
            6 : None
        }

        self.unit_health = {
            1 : TRIANGLE_HEALTH,
            2 : DIAMOND_HEALTH,
            3 : CIRCLE_HEALTH,
            4 : TRIANGLE_HEALTH,
            5 : DIAMOND_HEALTH,
            6 : CIRCLE_HEALTH
        }

    def is_players_turn(self, player_num):
        return self.turn[player_num]

    def get_turn(self):
        players_turn = 0
        for player, is_turn in self.turn.items():
            if is_turn:
                players_turn = player
        return players_turn

    def get_unit_location_by_type(self, unit_type):
        return self.unit_locations[unit_type]
    
    def change_turns(self):
        self.turn[1] = not self.turn[1]
        self.turn[2] = not self.turn[2]

    def move_unit(self, move):
        # move is [unit_type, col, row]
        unit_type, col, row = move
        self.unit_locations[unit_type] = [col, row]

    def attack_unit(self, attack):
        # attack is [unit_type, attack_power] where unit_type is the unit being attacked
        unit_type, attack_power = attack
        self.unit_health[unit_type] -= attack_power
        if self.unit_health[unit_type] <= 0:
            self.unit_health[unit_type] = 0
            self.unit_locations[unit_type] = None

    def set_ready(self, player_num):
        self.ready_state[player_num] = True

    def ready(self):
        return all(ready for ready in self.ready_state.values())

    def winner(self):
        pass

    def reset(self):
        for player_moved in self.turn_completed:
            player_moved = False