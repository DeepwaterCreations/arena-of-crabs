import pdb

import pygame
from pygame.locals import *

from drawable import Drawable, loadImage

class Entity(Drawable, pygame.Rect):
    
    #TODO: Rect constructors
    def __init__(self):
        Drawable.__init__(self)
        
        #Assuming this even works, it's for my convenience with the sprite stuff.
        self.rect = self
        
        self.x = 0
        self.y = 0
        self.width = 64
        self.height = 64
        
        self.sprites = {0: loadImage("no_image.bmp")} #TODO Rename this. >.-.< 
        
        
    def draw(self):        
        self.image = self.sprites[0]