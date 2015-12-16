import pdb

import pygame
from pygame.locals import *

from drawable import Drawable, loadImage 

class Background(Drawable):
    """Cheap, dirty tiles. 
        I'm going for a vertical slice thing, here. Shh.
        """

    def __init__(self):
       Drawable.__init__(self, "Floor") 
       self.image = loadImage("test_bgd_large.bmp", use_transparency = False)
       self.rect = self.image.get_rect()
       #Position the image:
       #self.x = 0
       #self.y = 0

