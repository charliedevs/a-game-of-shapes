"""
File: network.py
Programmers: Fernando Rodriguez, Charles Davis, Paul Rogers


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

    # Initilization
    def __init__(self, server_host, server_port):
        self.CLIENT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.HOST = server_host
        self.PORT = server_port
        self.ADDR = (self.HOST, self.PORT)
        self.player_num = None

        gamestate = GameState()

    def get_gamestate(self):
        self.send("get")
        return self.receive()

    def send(self, data):
        # Send data to server
        try:
            encrypted_data = encrypt(data.encode())
            self.CLIENT.sendall(encrypted_data)
        except socket.error as e:
            print(str(e))

    def receive(self):
        """
        Retrieve gamestate from server.
        
        Returns:
            {GameState} -- Represents state of game
        """
        try:
            decrypted_data = decrypt(self.CLIENT.recv(1024))
            return pickle.loads(decrypted_data)
        except socket.error as e:
            print(str(e))
            return None

    def receive_player_num(self):
        try:
            decrypted_data = decrypt(self.CLIENT.recv(2014))
            player_num = int(decrypted_data.decode())
            return player_num
        except socket.error as e:
            print(str(e))
            return None

    def connect(self):
         # Connect to server
        self.CLIENT.connect(self.ADDR)
        self.player_num = self.receive_player_num()
        print("Connected to server:", self.HOST)

    def get_player_num(self):
        return self.player_num

    def close(self):
        # Close CLIENT socket
        self.CLIENT.close()