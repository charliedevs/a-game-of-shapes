"""
File: button.py
Programmers: Fernando Rodriguez, Charles Davis, Paul Rogers
"""
import pygame

import src.colors as colors


class Button:
    """ A clickable button that calls a function.

    screen  -- pygame display surface.

    rect    -- a pygame rect or tuple (x, y, w, h)
               where (x, y) is the topleft corner.

    text    -- text displayed on button.

    action  -- function run on button click.
    """

    def __init__(self, screen, rect=(0, 0, 20, 8), text="Button", action=None):
        self.screen = screen
        self.rect = pygame.Rect(rect)
        self.color = colors.lightgray
        self.action = action

    def handle_click(self):
        if self.action is not None:
            self.action()

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)

    def set_position(self, (x, y)):
        # Pass in point for topleft of button.
        pass # replace this line with logic

    def change_size(self, (w, h)):
        # Pass in new width and height.
        pass # replace this line with logic
