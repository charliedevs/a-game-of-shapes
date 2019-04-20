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
        encrypted_data = encrypt(data.encode())
        connection.sendall(encrypted_data)
    except socket.error as e:
        print(str(e))


def send_gamestate(dictionary, connection):
    # Send dictionary
    data = json.dumps(dictionary)
    try:
        encrypted_data = encrypt(data.encode())
        connection.sendall(encrypted_data)
    except socket.error as e:
        print(str(e))


def receive(connection):
    # Receive data from SERVER

    try:
        decrypted_reply = decrypt(connection.recv(1024))
        reply = decrypted_reply.decode()
        return reply
    except socket.error as e:
        print(str(e))
        return e


def receive_gamestate(connection):
    try:
        decrypted_data = decrypt(connection.recv(1024))
        dictionary = json.loads(decrypted_data.decode())
        return dictionary
    except socket.error as e:
        print(str(e))


##############   Client Loop   #################

def client_thread(connection, player_num):
    # Procedure for client connection

    # Access global variables
    global client_count
    global gamestate

    verification_message = "1"
    encrypted_verification = encrypt(verification_message.encode())
    connection.sendall(encrypted_verification)
    thread_num = threading.active_count()
    print("Active threads:", thread_num)

    while True:
        # Receive one kB of data
        command = receive(connection)

        if 
        if command == "quit":
            send("quit", connection)
            break  # exit main client loop to close connection
        elif command == "looking":
            # Wait loop for two active threads
            while True:
                # 3 because SERVER is treated as a thread?
                if thread_num == 3:
                    player_turn = threading.get_ident() 
                    send(player_turn, connection)
                    break  # exit waiting loop
        elif command == "game":
            # recieve game state
            temp_gamestate = receive_gamestate(connection)
            print(temp_gamestate)

            # Do stuff to game state here. Maybe make a method to change sutff?
            # Send game state back to client
            send_gamestate(gamestate, connection)
		# TODO: add more commands here

        #print("Recieved", data)
        #send("Message received", connection)

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
