""" 
Strategy Game

Created by: Fernando Rodriguez, Charles Davis, Paul Rogers

"""

import sys
import pygame

# Window Size
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600

# Colors
BLACK = (0, 0, 0)

class Game:

    def __init__(self):
        pygame.init()

        pygame.display.set_caption('Strategy')

        self.clock = pygame.time.Clock()
        self.last_tick = pygame.time.get_ticks()
        self.screen_res = (WINDOW_WIDTH, WINDOW_HEIGHT)

        self.font = pygame.font.SysFont("Courier", 55)
        self.screen = pygame.display.set_mode(self.screen_res)

        #self.entities = pygame.sprite.Group()

        self.clock.tick(30)

        self.game_loop()

    def game_loop(self):
        gameover = False
        while not gameover:
            self.event_loop()
            self.tick()
            self.draw()
            pygame.display.update()

    def event_loop(self):
        for event in pygame.event.get():
            # Client closes window
            if event.type == pygame.QUIT:
                # add code for terminating network connection
                pygame.quit()
                sys.exit(0)
    
    def tick(self):
        self.ttime = self.clock.tick()
        self.mousepos = pygame.mouse.get_pos()
        self.keys_pressed = pygame.key.get_pressed()

    def draw(self):
        self.screen.fill(BLACK)

        #update map layers?

        #self.player.update(self.ttime / 1000.)

        #for e in self.entities:
            #self.screen.blit(e.image, self.camera.apply(e))

    def reset(self):
        #self.entities.empty()
        print("reset")