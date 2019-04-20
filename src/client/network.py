"""
File: network.py
Programmers: Fernando Rodriguez, Charles Davis, Paul Rogers


Contains the Network class which adds connectivity to a client.

"""

import socket
import json

from src.encryption import encrypt, decrypt

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

    def send(self, data):
        # Send data to server
        try:
            encrypted_data = encrypt(data.encode())
            self.CLIENT.sendall(encrypted_data)
        except socket.error as e:
            print(str(e))

    def send_gamestate(self, dictionary):
        # Send dictionary
        data = json.dumps(dictionary)
        try:
            encrypted_data = encrypt(data.encode())
            self.CLIENT.sendall(encrypted_data)
        except socket.error as e:
            print(str(e))

    def receive(self):
        # Receive data from server
        try:
            decrypted_reply = decrypt(self.CLIENT.recv(1024))
            reply = decrypted_reply.decode()
            return reply
        except socket.error as e:
            print(str(e))
            return e

    def receive_gamestate(self):
        # Receive dictionary from server
        try:
            decrypted_data = decrypt(self.CLIENT.recv(1024))
            dictionary = json.loads(decrypted_data.decode())
            return dictionary
        except socket.error as e:
            print(str(e))

    def connect(self):
         # Connect to server
        self.CLIENT.connect(self.ADDR)
        self.player_num = self.receive()
        print("Connected to server:", self.HOST)

    def get_player_num(self):
        return self.player_num

    def close(self):
        # Close CLIENT socket
        self.CLIENT.close()