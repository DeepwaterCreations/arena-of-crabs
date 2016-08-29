import pdb

import pygame
from pygame.locals import *

from drawable import Drawable, loadImage 

class SpriteSheet:
    def __init__(self, filepath, spritewidth = 64, spriteheight = 64, border = 0, use_transparency = True):
       self.sheet = loadImage(filepath, use_transparency) 

       self.spritewidth = spritewidth
       self.spriteheight = spriteheight
       self.border = border

       self.sprites_x = (self.sheet.get_width() - self.border) / (self.spritewidth + self.border)
       self.sprites_y = (self.sheet.get_height() - self.border) / (self.spriteheight + self.border)

    def getSprite(self, x, y):
        '''Return a surface with image data from the sub-cell of the spritesheet at index x, y'''
        if x + 1 > self.sprites_x or y + 1 > self.sprites_y:
            print "ERROR: Sprite index out of bounds"
            pdb.set_trace()
            return

        surface = pygame.Surface((self.spritewidth, self.spriteheight))
        
        surface.blit(self.sheet, (0,0), 
                     (self.border + (x * (self.spritewidth + self.border)), 
                      self.border + (y * (self.spriteheight + self.border)), 
                      self.spritewidth, 
                      self.spriteheight))
        surface.set_colorkey(surface.get_at((0,0)), RLEACCEL)
        return surface
