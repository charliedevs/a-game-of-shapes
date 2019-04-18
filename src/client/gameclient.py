"""
File: network.py
Programmers: Fernando Rodriguez, Charles Davis, Paul Rogers


Contains the Network class which adds connectivity to a CLIENT.

"""

import socket
import json
import threading

from src.encryption import encrypt, decrypt

class GameClient:
    """
    Adds network functionality to a CLIENT or game.
    Allows to send and recieve strings and dictionaries.
    Incorporates encryption and decryption to sent information. 
    """

    # Initilization
    def __init__(self, server_host, server_port, client_port):
        self.server_message = []
        self.client_addr = ("0.0.0.0", client_port)

        self.lock = threading.Lock()
        self.server_listener = SocketThread(self.client_addr,
                                            self,
                                            self.lock)
        self.server_listener.start()

        self.server_addr = (server_host, server_port)

    def send_gamestate(self, dictionary):
        # Send dictionary
        data = json.dumps(dictionary)
        try:
            encrypted_data = encrypt(data.encode())
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.sendto(encrypted_data, self.SERVER)
        except socket.error as e:
            print(str(e))

    def receive_gamestate(self):
        # Receive dictionary from server
        data = self.server_message
        decrypted_data = decrypt(data)
        gamestate = json.loads(decrypted_data.decode())
        return gamestate

    def connect(self):
         # Connect to server
        self.CLIENT.connect(self.ADDR)
        reply = self.receive()
        print(reply)

    def close(self):
        # Close CLIENT socket
        self.CLIENT.close()

class SocketThread(threading.Thread):
    def __init__(self, addr, client, lock):
        """
        Client UDP connection
        
        Arguments:
            threading {[type]} -- [description]
            addr {[type]} -- [description]
            client {[type]} -- [description]
            lock {[type]} -- [description]
        """
        threading.Thread.__init__(self)
        self.client = client
        self.lock = lock
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(addr)

    def run(self):
        """
        Get responses from server
        """
        while True:
            data, addr = self.sock.recvfrom(1024)
            self.lock.acquire()
            try:
                self.client.server_message.append(data)
            finally:
                self.lock.release()

    def stop(self):
        """
        Kill thread
        """
        self.sock.close()