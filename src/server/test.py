from game_client import Network
import sys

if len(sys.argv) < 3:
	print("Usage: python3 test.py <host> <port>")
	sys.exit()

host = sys.argv[1]
port = int(sys.argv[2])

client_one = Network(host, port)

while True: 
	message = input("Enter a message to send to server: ")
	client_one.send(message)
