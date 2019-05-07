"""
File: network.py
Programmers: Fernando Rodriguez, Charles Davis

Contains the Network class which adds connectivity to a client.

"""
import socket
import pickle

from src.encryption import encrypt, decrypt
from src.gamestate import GameState

class Network:
    """
    Adds network functionality to the game.
    Allows sending and receiving encrypted data.
    """

    def __init__(self, server_host, server_port):
        self.CLIENT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.HOST = server_host
        self.PORT = server_port
        self.ADDR = (self.HOST, self.PORT)
        self.player_num = None

        gamestate = GameState()

    def get_gamestate(self):
        """
        Retrieves the gamestate from server.
        """
        self.send_command("get")
        return self.receive_pickle()

    def send_turn(self, turn):
        """
        Sends move and attack to server.
        """
        reply = None
        while reply != "ok":
            self.send_command("turn")
            reply = self.receive()
        reply = None
        while reply != "ok":
            self.send_pickle(turn)
            reply = self.receive()

    def request_turn(self):
        """
        Retrieves whose turn it is from server.
        """
        self.send_command("request_turn")
        turn = self.receive_integer()
        return turn

    def send_hand(self, hand):
        """
        Sends rock paper scissors move to server.
        """
        reply = None
        while reply != "ok":
            self.send_command("hand")
            reply = self.receive()
        reply = None
        while reply != "ok":
            self.send_pickle(hand)
            reply = self.receive()

    def get_rps_winner(self):
        """
        Retrieves winner of rock paper scissors.
        """
        winner = None
        while not winner:
            self.send_command("rps_winner")
            winner = self.receive_integer()
        return winner

    def check_for_rps(self):
        """
        Asks server if rock paper scissors game has
        been initiated by other client.
        """
        self.send_command("check_rps")
        rps_in_session = self.receive_integer()
        if rps_in_session == 1:
            rps_in_session = True
        else:
            rps_in_session = False
        return rps_in_session

    def send_command(self, data):
        """
        Sends a command the server understands, such
        as requesting data or letting the server know
        that the client is about to send data.
        """
        try:
            encrypted_data = encrypt(data.encode())
            self.CLIENT.sendall(encrypted_data)
        except socket.error as e:
            print(str(e))
            
    def send_pickle(self, data):
        """
        Sends a serialized object to server.
        """
        data_pickle = pickle.dumps(data)
        try:
            encrypted_data = encrypt(data_pickle)
            self.CLIENT.sendall(encrypted_data)
        except socket.error as e:
            print(str(e))

    def receive_pickle(self):
        """
        Retrieves pickle from server.
        
        Returns:
            {object} -- An object loaded from pickle
        """
        try:
            decrypted_data = decrypt(self.CLIENT.recv(2048))
            return pickle.loads(decrypted_data)
        except socket.error as e:
            print(str(e))
            return None

    def receive(self):
        """
        Receives regular data from server.
        """
        try:
            decrypted_data = decrypt(self.CLIENT.recv(2048))
            data = decrypted_data.decode()
            return data
        except socket.error as e:
            print(str(e))
            return None

    def receive_integer(self):
        """
        Retrieves an integer.
        """
        try:
            integer = int(self.receive())
            return integer
        except ValueError as e:
            print(str(e))
            return None

    def connect(self):
        """
        Initiates a connection with server.
        """
        self.CLIENT.connect(self.ADDR)
        self.player_num = self.receive_integer()
        print("Connected to server:", self.HOST)

    def get_player_num(self):
        """
        Gets player's number stored in Network class.
        """
        return self.player_num

    def close(self):
        """
        Safely closes client socket.
        """
        self.send_command("quit")
        self.CLIENT.close()