"""
File: rockpaperscissors.py
Programmers: Fernando Rodriguez, Charles Davis

"""
import pygame
import os

import src.colors as colors
from src.constants import *

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
        self.rock_image = self.scale(pygame.image.load("rock.png"))
        self.paper_image = self.scale(pygame.image.load("paper.png"))
        self.scissors_image = self.scale(pygame.image.load("scissors.png"))

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

    def draw(self, role):
        """
        Draws Rock, Paper, Scissors game.
        Role is "attacker" or "defender".
        """
        self.screen.blit(self.rock_image, self.rock_rect)
        self.screen.blit(self.paper_image, self.paper_rect)
        self.screen.blit(self.scissors_image, self.scissors_rect)

        # Change text based on role
        title_color = colors.white
        title_text = ""
        help_text = ""
        if role == "attacker":
            title_text = "DESTROY YOUR ENEMIES!"
            help_text = "HELP: Play rock, paper, scissors! Win or tie to damage your enemy."
        elif role == "defender":
            title_text = "YOU'VE BEEN ATTACKED!"
            help_text = "HELP: Play rock, paper, scissors! You must win to avoid damage."

        # Display title
        title_font = pygame.font.Font(GAME_FONT, 20)
        text_surface = title_font.render(title_text, False, title_color)
        location = [(WINDOW_WIDTH // 2) - (text_surface.get_width() // 2), 10] 
        self.screen.blit(text_surface, location)

        # Display help text
        location = [0, WINDOW_HEIGHT-25]
        font = pygame.font.Font(GAME_FONT, 12)
        text_surface = font.render(help_text, False, colors.white)
        self.screen.blit(text_surface, location)

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