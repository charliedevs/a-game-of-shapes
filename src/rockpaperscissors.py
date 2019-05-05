import pygame
from src.constants import *
import os

class RPS:
    """
    Handles drawing rock, paper, scissors minigame.
    """

    def __init__(self, screen):
        self.screen = screen
        self.rps_rect = self.get_rps_rect()

        # Determine size of each image
        self.block_width = self.rps_rect.w // 3
        self.rock_rect = self.get_rock_rect()
        self.paper_rect = self.get_paper_rect()
        self.scissors_rect = self.get_scissors_rect()

        # Scaled images of Rock, Paper, Scissors #TODO: Place images in separate folder
        self.rock_image = self.scale(pygame.image.load("rock.jpg"))
        self.paper_image = self.scale(pygame.image.load("paper.jpg"))
        self.scissors_image = self.scale(pygame.image.load("scissors.jpg"))

        # The choice picked by client
        self.hand = None


    def handle_click(self, mouse_position):
        """
        Check if player clicked rock, paper, or scissors.
        """
        if not self.mouse_position_inside_rps(mouse_position):
            return
        
        hand = None
        if self.rock_rect.collidepoint(mouse_position):
            hand = ROCK
        if self.paper_rect.collidepoint(mouse_position):
            hand = PAPER
        if self.scissors_rect.collidepoint(mouse_position):
            hand = SCISSORS

        self.hand = hand
        

    def mouse_position_inside_rps(self, mouse_position):
        """
        Returns true if mouse is positioned over rps rect.
        """
        return self.rps_rect.collidepoint(mouse_position)

    def draw(self):
        self.screen.blit(self.rock_image, self.rock_rect)
        self.screen.blit(self.paper_image, self.paper_rect)
        self.screen.blit(self.scissors_image, self.scissors_rect)

    def scale(self, image):
        """
        Returns a properly scaled version of image.
        """
        return pygame.transform.scale(image, (self.block_width, self.rps_rect.h))

    def get_rps_rect(self):
        """
        Returns the size of the rps surface.
        """
        return self.screen.get_rect()

    def get_rock_rect(self):
        """
        Returns the size of the rock surface.
        """

        x = self.rps_rect.x
        y = self.rps_rect.y
        w = self.block_width
        h = self.rps_rect.h

        rock_rect = pygame.Rect(x, y, w, h)
        
        return rock_rect

    def get_paper_rect(self):
        """
        Returns the size of the paper surface.
        """

        x = self.rps_rect.x + self.block_width
        y = self.rps_rect.y
        w = self.block_width
        h = self.rps_rect.h

        paper_rect = pygame.Rect(x, y, w, h)
    
        return paper_rect

    def get_scissors_rect(self):
        """
        Returns the size of the scissors surface.
        """

        x = self.rps_rect.x + (2 * self.block_width)
        y = self.rps_rect.y
        w = self.block_width
        h = self.rps_rect.h

        scissors_rect = pygame.Rect(x, y, w, h)
        
        return scissors_rect