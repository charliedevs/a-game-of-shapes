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

    def __init__(self, screen, rect=(0, 0, 20, 8), text="Button", font=None, action=None):
        self.screen = screen
        self.rect = pygame.Rect(rect)
        self.color = colors.black
        self.action = action
        self.text = text

        if font is None:
            self.font = pygame.font.SysFont("Courier", 12)
        else:
            self.font = font

        self.surface = self.screen.subsurface(self.rect)
        
    def handle_click(self):
        if self.action is not None:
            self.action()
            return True
        else:
            return False

    def draw(self):
        self.surface.fill(colors.darkgray)
        pygame.draw.rect(self.surface, self.color, self.rect)
        #font_surface = self.font.render(self.text, True, colors.white)
        #font_centerx = font_surface.get_rect().centerx
        #font_offset = font_surface.get_offset()[0]
        #print("[Debug]: ")
        #self.screen.blit(font_surface, dest=self.position_text(font_surface))

    def set_position(self, x, y):
        # Pass in point for topleft of button.
        pass # replace this line with logic

    def change_size(self, w, h):
        # Pass in new width and height.
        pass # replace this line with logic
        
    def get_rect(self):
        return self.rect

    def position_text(self, font_surface):
        font_centerx = font_surface.get_rect().centerx
        font_offset = font_surface.get_offset()[0]
        return self.rect.centerx - (font_centerx + font_offset)
