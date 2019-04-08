#Client networking class

import socket
import sys
from src.encryption import encrypt, decrypt

class Network(object):
	
	#Initilization
	def __init__(self, host, port):
		self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.host = host
		self.port = port
		self.addr = (self.host, self.port)
		self.connect()

	#Connect to server
	def connect(self):
		self.client.connect(self.addr)
		decyrpted_verification = decrypt(self.client.recv(1024))
		verification = decyrpted_verification.decode()
		print(verification)

	#Send data to server
	def send(self, data):
		try:
			encrypted_data = encrypt(data.encode())
			self.client.sendall(encrypted_data)
			decrypted_reply = decrypt(self.client.recv(1024))
			reply = decrypted_reply.decode()
			print(reply)
		except socket.error as e:
			return str(e)