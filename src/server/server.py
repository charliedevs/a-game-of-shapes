"""
File: SERVER.py
Programmers: Fernando Rodriguez, Charles Davis, Paul Rogers


Controls the connection between two clients.

"""

import socket
import sys
import threading
import json

from gamestate import GameState
from encryption import encrypt, decrypt

connected = set()

# Number of clients connected
client_count = 0

# Global gamestate object holding
# positions of player units and
# other game information.
gamestate = None

def start_server():
    """
    Sets up server and begins listening for
    client connections.
    """

    # Use the global variable gamestate
    global gamestate

    # Create a socket object
    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Use localhost and grab port from commandline arg
    HOST = socket.gethostbyname(socket.gethostname())
    PORT = int(sys.argv[1])

    # Attempt bind to (host, port) pair
    try:
        SERVER.bind((HOST, PORT))
    except socket.error:
        print("Binding to " + HOST + ":" + str(PORT) + "failed.")
        SERVER.close()
        sys.exit()

    # Start listeing for connections, max of two
    SERVER.listen(2)
    print("SERVER listening on " + HOST + ":" + str(PORT))

    # Main server loop
    while True:
        # Try block to allow keyboard interrupt
        try:
            if client_count < 2:
                # Accept incoming connection
                print("Waiting for client {}...".format(client_count + 1))
                connection, address = SERVER.accept()
                print("Established connection with " + address[0] + ":" + str(address[1]))

                # Increment global client counter
                client_count += 1

                # Keep track of whose turn it is
                player_num = 1

                if client_count == 0:
                    # Create new gamestate object
                    gamestate = GameState()
                else:
                    # One client already connected so
                    # this connection will be player 2
                    gamestate.ready = True
                    player_num = 2

                # Create thread to handle client
                t = threading.Thread(target=client_thread, args=(connection, player_num))
                t.start()
        except KeyboardInterrupt:
            # Exit server loop
            break

    print("\nServer closing...")
    SERVER.close()

def send(data, connection):
    try:
        encrypted_data = encrypt(str(data).encode())
        connection.sendall(encrypted_data)
    except socket.error as e:
        print("[Error]: Socket cannot be used to send data.")
        print(str(e))
    except TypeError:
        print("[Error]: Data cannot be converted to string to be sent.")


def send_gamestate(gamestate, connection):
    # Send gamestate as serialized json object
    gamestate_json = json.dumps(gamestate)
    try:
        encrypted_data = encrypt(gamestate_json.encode())
        connection.sendall(encrypted_data)
    except socket.error as e:
        print(str(e))


def receive(connection):
    # Receive data from client
    try:
        decrypted_reply = decrypt(connection.recv(1024))
        reply = decrypted_reply.decode()
        return reply
    except socket.error as e:
        print(str(e))
        return e


#TODO: maybe remove this
def get_gamestate_from_json(gamestate_json):
    # TODO: add try/except for json conversion
    gamestate = json.loads(gamestate_json)
    return gamestate


##############   Client Loop   #################

def client_thread(connection, player_num):
    """
    Handles connection to clients.

    Arguments:
        connection {socket} -- Used to access network
        player_num {[type]} -- Defines player order
    """

    # Access global variables
    global client_count
    global gamestate

    # Send player's number to client
    send(player_num, connection)
    encrypted_num = encrypt(str(player_num).encode())
    connection.sendall(encrypted_num)

    # Number of active threads
    thread_count = threading.active_count()
    print("[Debug]: Active threads:", thread_count)

    while True:
        # Receive one kB of data
        data = receive(connection)

        if data:
            # Single commands, no json
            if data == "reset":
                gamestate.reset()
            elif data == "quit":
                #TODO: fix this command
                send("quit", connection)
                break  # exit main client loop to close connection
            else:
                # Client sent a move
                # or an attack
        else:
            # Data wasn't received; exit loop
            break

    # Close connection
    print("Closing connection with player", player_num)
    client_count -= 1
    if client_count == 0:
        # Delete gamestate object
        gamestate = None
        print("All clients disconnected.")
    connection.close()

################################################


if __name__ == "__main__":
    # Check for correct number of arguments
    if len(sys.argv) < 2:
        print("Usage: python server.py <port>")
        sys.exit()
    # Enter server loop
    start_server()
