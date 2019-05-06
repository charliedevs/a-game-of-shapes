"""
File: colors.py
Programmers: Fernando Rodriguez, Charles Davis

Defines custom colors used for GUI.

"""

white = (213, 213, 213)
black = (59, 59, 59)

lightergrey = (169, 169, 169)
lightgray = (100, 100, 100)
lightgrey = (100, 100, 100)
darkgray = (73, 73, 73)
darkgrey = (73, 73, 73)

red = (247, 141, 140)
orange = (252, 163, 105)
yellow = (255, 212, 121)
green = (168, 211, 169)
blue = (120, 170, 214)
purple = (214, 172, 214)
aqua = (118, 212, 214)

darkred = (218, 75, 75)
darkblue = (55, 122, 183)
darkgreen = (118, 186, 120)
darkpurple = (190, 124, 190)
darkorange = (251, 105, 9)

def get_hover_color(color):
    """
    Used for highlighting hovered tiles.
    
    Arguments:
        color {(int, int, int)} -- The RGB value of the tile
    
    Returns:
        (int, int, int) -- The new RGB value
    """
    new_color = None

    if color == darkgray:
        # Regular tiles get lighter
        new_color = lightgray
    else:
        # Other tile colors get darkened
        R, G, B = color
        R -= 20
        G -= 20
        B -= 20
        new_color = (R, G, B)

    return new_color