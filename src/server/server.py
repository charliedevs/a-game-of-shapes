"""
File: SERVER.py
Programmers: Fernando Rodriguez, Charles Davis, Paul Rogers


Controls the connection between two clients.

"""

import socket  # For networkingn sockets
import sys		# For system exit
import threading
import json

from encryption import encrypt, decrypt

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

##################Client Loop##################


def client_thread(connection):
    # Fucntion for client connection

    verification_message = "Established connection with SERVER"
    encrypted_verification = encrypt(verification_message.encode())
    connection.sendall(encrypted_verification)
    threads_num = threading.active_count()
    print("Active threads:", threads_num)

    while True:
        # Receive one kB of data
        command = receive(connection)
        if command == "quit":
            send("quit", connection)
            break  # exit main client loop to close connection
        elif command == "looking":
            # Wait loop for two active threads
            while True:
                # 3 because SERVER is treated as a thread?
                if threading.active_count() == 3:
                    send("start", connection)
                    break  # exit waiting loop
        elif command == "game":
            # recieve game state
            gamestate = receive_gamestate(connection)
            print(gamestate)
            # Do stuff to game state here. Maybe make a method to change sutff?
            # Send game state back to client
            send_gamestate(gamestate, connection)
		# TODO: add more commands here

        #print("Recieved", data)
        #send("Message received", connection)

    # Close connection
    print("Closing connection")
    connection.close()

################################################


##################SERVER Start##################
# Check for correct number of arguments
if len(sys.argv) < 2:
    print("Usage: Python3 game_SERVER.py <port>")
    sys.exit()

# SERVER socket creation
SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Host ip and port
HOST = socket.gethostbyname(socket.gethostname())
PORT = int(sys.argv[1])

# Attemp bind to (host, port) pair
try:
    SERVER.bind((HOST, PORT))
except socket.error:
    print("Binding to " + HOST + ":" + str(PORT) + "failed")
    SERVER.close()
    sys.exit()

# Start listeing for connections, max of two
SERVER.listen(2)
print("SERVER listening on " + HOST + ":" + str(PORT))

# Main SERVER loop
try:
    while True:
        connection, address = SERVER.accept()
        #address = (ip, port)
        print("Established connection with " + address[0] + ":" + str(address[1]))
        # Establish new threaded client connection
        t = threading.Thread(target=client_thread, args=(connection,))
        t.start()
except KeyboardInterrupt:
    print("\nProgram Terminated")
    SERVER.close()
    sys.exit()

SERVER.close()
