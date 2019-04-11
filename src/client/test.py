#file for testing
#!/usr/bin/env python

'''
import pygame
import src.pygame_textinput

pygame.init()

BLACK = (0,0,0)
WHITE = (255, 255, 255)
WIDTH = 600
HEIGHT = 600

#text input
textinput = pygame_textinput.TextInput()

gameDisplay = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.SysFont(None, 25)
clock = pygame.time.Clock()

def message_to_screen(message, color):
	largeText = pygame.font.Font("Hello", 115)
	TextSurf, TextRect = text_objects(message, largeText)
	Text.Rect.center = ((WIDTH/2), (HEIGHT/2))
	gameDisplay.blit(TextRect, TextRect)
	pygame.display.update()

def game_intro():
	pygame.display.set_caption("Main Menu")
	intro = True
	while intro:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				intro = False
			print(event)
		gameDisplay.fill(WHITE)
		textinput.update(events)
		#pygame.display.flip()
		gameDisplay.blit(textinput.get_surface(), (10,10))
		pygame.display.update()
		clock.tick(60)

game_intro()
#message_to_screen("Hello", (255,255,0))
pygame.quit()
quit()

'''
import sys
from network import Network

if len(sys.argv) < 3:
	print("Usage: python3 test.py <host> <port>")
	sys.exit()

host = sys.argv[1]
port = int(sys.argv[2])

client = Network(host, port)
client.connect()

reply = ""
while True: 
	if reply == "quit":
		break
	message = input("Enter a message to send to server: ")
	client.send(message)
	reply = client.receive()
	print(reply)

client.close()