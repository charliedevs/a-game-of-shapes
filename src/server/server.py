#Game server

import socket								#For networkingn sockets
import sys									#For system exit
from _thread import start_new_thread		#For threading a client connection
from src.encryption import encrypt, decrypt

#Fucntion for client connection
def client_thread(connection):
	verification_message = "Established connection with server"
	encrypted_verification = encrypt(verification_message.encode())
	connection.sendall(encrypted_verification)

	while True:
		#Receive one kB of data
		decrypted_data = decrypt(connection.recv(1024))
		data = decrypted_data.decode()
		if not data:
			break
		################################################
		print(data)
		reply = "Recieved data"
		encrypted_reply = encrypt(reply.encode())
		connection.sendall(encrypted_reply)
		################################################
	
	#Close connection
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
	start_new_thread(client_thread, (connection,))
	
server.close()