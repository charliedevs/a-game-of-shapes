"""
File: gamestate.py
Programmers: Fernando Rodriguez, Charles Davis, Paul Rogers

"""

from src.constants import *

class GameState:

    def __init__(self):
        # Set to true if two clients are connected
        self.ready_state = {1 : False, 2 : False}

        # Keeps track of player turn
        self.turn = {1 : True, 2 : False}

        # Holds locations of all units
        # 1-3 are player 1's, 4-6 are player 2's
        self.unit_locations = self.initialize_locations()

        # Server keeps track of unit health
        self.unit_health = self.initialize_health()

        # Keep track of rock paper scissors moves
        self.hands = {
            1 : None,
            2 : None
        }

        # self.rps_finished = {
        #     1 : False,
        #     2 : False
        # }

        self.rps_winner = 0

        self.game_is_over = False
        self.winner = None
        self.playing_rps = False

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

    # def finish_rps(self, player_num):
    #     self.rps_finished[player_num] = True
    #     all_finished = True
    #     for finished in self.rps_finished.values():
    #         if not finished:
    #             all_finished = False

    #     if all_finished:
    #         self.hands[1] = None
    #         self.hands[2] = None

    def ready(self):
        return all(ready for ready in self.ready_state.values())

    def determine_if_game_over(self):
        #TODO: Make sure these dicts are correct. Maybe use for loops
        # Use dictionary comprehensions to separate player units
        player_1_health = {unit: self.unit_health[unit] for unit in self.unit_health.keys() & {1, 2, 3}}
        player_2_health = {unit: self.unit_health[unit] for unit in self.unit_health.keys() & {4, 5, 6}}

        # Game is over if either player has no health left
        game_is_over = False
        if all(health == 0 for health in player_1_health.values()):
            # Player 1 died, Player 2 wins
            self.winner = 2
            game_is_over = True
        if all(health == 0 for health in player_2_health.values()):
            # Player 2 died, Player 1 wins
            self.winner = 1
            game_is_over = True

        if game_is_over:
            self.game_is_over = True

    def set_hand(self, player_num, hand):
        self.hands[player_num] = hand

    def determine_rps_winner(self, winner_cache=[]):
        """
        See who won the game of rock paper scissors!

        If it returns 0, both haven't played yet.
        If it returns 3, it's a tie!
        """

        # If both haven't played, there's no winner yet
        both_have_played = True
        for hand in self.hands.values():
            if not hand:
                both_have_played = False

        winner = 0
        if both_have_played:
            # Check if winner has already been calculated
            if winner_cache:
                # Both have played, so remove their plays
                self.hands[1] = None
                self.hands[2] = None
                return winner_cache.pop()

            # Winning conditions
            if self.hands[1] == self.hands[2]:
                # Tie
                winner = 3
            elif self.hands[1] == ROCK:
                if self.hands[2] == PAPER:
                    winner = 2
                elif self.hands[2] == SCISSORS:
                    winner = 1
            elif self.hands[1] == PAPER:
                if self.hands[2] == SCISSORS:
                    winner = 2
                elif self.hands[2] == ROCK:
                    winner = 1
            elif self.hands[1] == SCISSORS:
                if self.hands[2] == ROCK:
                    winner = 2
                elif self.hands[2] == PAPER:
                    winner = 1 

            winner_cache.append(winner)

        return winner

    def rps_in_session(self):
        in_session = 0
        for hand in self.hands.values():
            if hand:
                in_session = 1

        return in_session

    def clear_rps_hands(self):
        self.hands[1] = None
        self.hands[2] = None

    def reset(self):
        self.unit_locations = self.initialize_locations()
        self.unit_health = self.initialize_health()

        # Set both players to not ready
        for player in self.ready_state.keys():
            self.ready_state[player] = False


    def initialize_locations(self):
        unit_locations = {
            1 : None,
            2 : None,
            3 : None,
            4 : None,
            5 : None,
            6 : None
        }

        return unit_locations

    def initialize_health(self):
        unit_health = {
            1 : TRIANGLE_HEALTH,
            2 : DIAMOND_HEALTH,
            3 : CIRCLE_HEALTH,
            4 : TRIANGLE_HEALTH,
            5 : DIAMOND_HEALTH,
            6 : CIRCLE_HEALTH
        }

        return unit_health