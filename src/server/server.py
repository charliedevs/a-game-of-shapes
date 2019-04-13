#Game server
#!/usr/bin/env python

import socket								#For networkingn sockets
import sys									#For system exit
from encryption import encrypt, decrypt
import threading

def send(data, connection):
		try:
			encrypted_data = encrypt(data.encode())
			connection.sendall(encrypted_data)
		except socket.error as e:
			print(str(e))

#Receive data from server
def receive(connection):
	try:
		decrypted_reply = decrypt(connection.recv(1024))
		reply = decrypted_reply.decode()
		return reply
	except socket.error as e:
		print(str(e))
		return e

#Fucntion for client connection
def client_thread(connection):
	verification_message = "Established connection with server"
	encrypted_verification = encrypt(verification_message.encode())
	connection.sendall(encrypted_verification)
	threads_num = threading.active_count()
	print("Active threads:", threads_num)

	while True:
		#Receive one kB of data
		data = receive(connection)
		if data == "quit":
			send("quit", connection)
			break
		elif data == "looking":
			#Wait loop for two active threads
			while True:
				if threading.active_count() == 3:
					send("start", connection)
					break
				#TODO: implement dictionary(game state) elif

		print("Recieved", data)
		send("Message received", connection)
	#Close connection
	print("Closing connection")
	connection.close()

#Check for correct number of arguments
if len(sys.argv) < 2:
	print("Usage: Python3 game_server.py <port>")
	sys.exit()

#Server socket creation
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Host ip and port
host = socket.gethostbyname(socket.gethostname())
port = int(sys.argv[1])

#Attemp bind to (host, port) pair
try:
	server.bind((host, port))
except socket.error:
	print("Binding to " + host + ":" + str(port) + "failed")
	server.close()
	sys.exit()

#Start listeing for connections, max of two
server.listen(2)
print("Server listening on " + host + ":" + str(port))

#Main server loop
while True:
	try:
		connection, address = server.accept()
	except KeyboardInterrupt:
		print("\nProgram Terminated")
		server.close()
		sys.exit()
	#address = (ip, port)
	print("Established connection with " + address[0] + ":" + str(address[1]))
	#Establish new threaded client connection
	t = threading.Thread(target= client_thread, args= (connection,))
	t.start()
	
server.close()