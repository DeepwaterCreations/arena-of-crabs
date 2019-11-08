import pdb

import pygame
from pygame.locals import *

import string

from drawable import loadImage
from spritesheet import SpriteSheet

spritewidth = 32
spriteheight = 64
filename = "letters_large.bmp"
misc_chars = ["crabsymbol"]

letter_surfaces = {}

def loadTextSprites():
    spritesheet = SpriteSheet(filename, spritewidth, spriteheight)
    for idx, c in enumerate(string.ascii_uppercase):
        letter_surfaces[c] = spritesheet.getSprite(idx, 0)
    for idx, c in enumerate(string.ascii_lowercase):
        letter_surfaces[c] = spritesheet.getSprite(idx, 1)
    for idx, label in enumerate(misc_chars):
        letter_surfaces[label] = spritesheet.getSprite(idx, 2)
    for idx, d in enumerate(string.digits):
        letter_surfaces[d] = spritesheet.getSprite(idx, 3)

def getCharSurface(char):
    if letter_surfaces == {}:
        raise Exception("Text sprites haven't been loaded yet")
    else:
        return letter_surfaces[char]

def getStringSurface(string):
    if letter_surfaces == {}:
        raise Exception("Text sprites haven't been loaded yet")
    else:
        string_surface = pygame.Surface((len(string) * spritewidth, spriteheight))
        for idx, c in enumerate(string):
            char_surface = getCharSurface(c)
            x_pos = idx * spritewidth
            string_surface.blit(char_surface, (x_pos,0))
        return string_surface
