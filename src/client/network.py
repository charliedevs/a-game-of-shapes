#Client networking class

import socket
import sys
from encryption import encrypt, decrypt
import json

class Network(object):
	
	#Initilization
	def __init__(self, host, port):
		self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.host = host
		self.port = port
		self.addr = (self.host, self.port)

	#Send data to server
	def send(self, data):
		try:
			encrypted_data = encrypt(data.encode())
			self.client.sendall(encrypted_data)
		except socket.error as e:
			print(str(e))

	#Send dictionary
	def send_dictionary(self, dictionary):
		data = json.dumps(dictionary)
		try:
			encrypted_data = encrypt(data.encode())
			self.client.sendall(encrypted_data)
		except socket.error as e:
			print(str(e))

	#Receive data from server
	def receive(self):
		try:
			decrypted_reply = decrypt(self.client.recv(1024))
			reply = decrypted_reply.decode()
			return reply
		except socket.error as e:
			print(str(e))
			return e

	def receive_dictionary(self):
		decrypted_data = decrypt(self.client.recv(1024))
		dictionary = json.loads(decrypted_data.decode())
		#TODO: return dictionary 

	#Connect to server
	def connect(self):
		self.client.connect(self.addr)
		reply = self.receive()
		print(reply)

	def close(self):
		self.client.close()