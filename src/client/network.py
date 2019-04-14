# Client networking class

import socket
import sys
from src.encryption import encrypt, decrypt
import json


class Network(object):

    # Initilization
    def __init__(self, host, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.addr = (self.host, self.port)

    def send(self, data):
        # Send data to server
        try:
            encrypted_data = encrypt(data.encode())
            self.client.sendall(encrypted_data)
        except socket.error as e:
            print(str(e))

    def send_game_state(self, dictionary):
        # Send dictionary
        data = json.dumps(dictionary)
        try:
            encrypted_data = encrypt(data.encode())
            self.client.sendall(encrypted_data)
        except socket.error as e:
            print(str(e))

    def receive(self):
        # Receive data from server
        try:
            decrypted_reply = decrypt(self.client.recv(1024))
            reply = decrypted_reply.decode()
            return reply
        except socket.error as e:
            print(str(e))
            return e

    def receive_game_state(self):
        # Receive dictionary from server
        try:
            decrypted_data = decrypt(self.client.recv(1024))
            dictionary = json.loads(decrypted_data.decode())
            return dictionary
        except socket.error as e:
            print(str(e))

    def connect(self):
         # Connect to server
        self.client.connect(self.addr)
        reply = self.receive()
        print(reply)

    def close(self):
        # Close client socket
        self.client.close()
