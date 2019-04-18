"""
File: SERVER.py
Programmers: Fernando Rodriguez, Charles Davis, Paul Rogers


Controls the connection between two clients.

"""

import socket 
import sys
import select
import json

from src.encryption import encrypt, decrypt

def send_gamestate(dictionary, connection):
    # Send dictionary
    data = json.dumps(dictionary)
    try:
        encrypted_data = encrypt(data.encode())
        connection.sendall(encrypted_data)
    except socket.error as e:
        print(str(e))


def recieve_gamestate(connection):
    pass

def decode_data(incoming_data):
    try:
        decrypted_data = decrypt(incoming_data)
        gamestate = json.loads(decrypted_data.decode())
        return gamestate
    except socket.error as e:
        print(str(e))
        return None


##################SERVER Start##################

if len(sys.argv) < 2:
    print("Usage: python3 gameserver.py <port_num>")
    sys.exit()

# Set up connection
SERVER = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
HOST = socket.gethostbyname(socket.gethostname())
PORT = int(sys.argv[1])
try:
    SERVER.bind((HOST, PORT))
except socket.error:
    print("Binding to " + HOST + ":" + str(PORT) + "failed")
    SERVER.close()
    sys.exit()

# Create lists to hold messages between client/server
read_list = [SERVER]
write_list = []

# Dictionaries representing gamestate and connected players
gamestate = {}
players = {1 : None, 2 : None}

# Start listening for connections, max of two
SERVER.listen(2)
print("SERVER listening on " + HOST + ":" + str(PORT))

# Main SERVER loop
try: 
    while True:
        # Set up waitable objects.
        # select() allows blocking until the
        # sockets are ready to be written to.
        # Returns empty lists upon timeout.
        # see: https://docs.python.org/2/library/select.html
        readable, writable, exceptional = (
            select.select(read_list, write_list, [])
        )

        for f in readable:
            if f is SERVER:

                ######################################################
                # METHODIZE THIS TOO
                # Receive data from client
                try:
                    data, recv_addr = SERVER.recvfrom(1024)
                    print("[Debug]: Received data from",  recv_addr)
                except socket.timeout:
                    continue

                if len(data) > 0:
                    #convert data to dict
                    new_gamestate = decode_data(data)

                    ########################################
                    ## PULL THIS INTO METHOD

                    # If gamestate has changed, update
                    # and send back to both clients.
                    if new_gamestate != gamestate:
                        gamestate = new_gamestate
                        
                        # Retrieve client_addr from gamestate
                        sending_client = None
                        try:
                            sending_client = gamestate['client_addr']
                        except KeyError:
                            pass

                        # Assign player number by address
                        for player, addr in players:
                            # if address doesn't exist, add
                            if addr is None:
                                players[player] = sending_client
                                break

                        #send gamestate to other player
                        for player, addr in players:
                            if addr != sending_client:
                                SERVER.sendto(gamestate, addr)

                    ########################################

except KeyboardInterrupt:
    print("\nServer terminated.")
    SERVER.close()
    sys.exit()
