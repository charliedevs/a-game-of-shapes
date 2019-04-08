import socket
import sys

class Network(object):
	
	def __init__(self, host, port):
		self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.host = host
		self.port = port
		self.addr = (self.host, self.port)
		self.id = self.connect()

	def connect(self):
		self.client.connect(self.addr)
		print(self.client.recv(1024).decode())

	def send(self, data):
		try:
			self.client.send(data.encode())
			reply = self.client.recv(1024).decode()
			print(reply)
		except socket.error as e:
			return str(e)
