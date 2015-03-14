import pdb

import pygame
from pygame.locals import *

from drawable import Drawable

class Entity(Drawable, pygame.sprite.Sprite, pygame.Rect):
    
    #TODO: Rect constructors
    def __init__(self):
        Drawable.__init__(self)
        pygame.sprite.Sprite.__init__(self)
        
        #Assuming this even works, it's for my convenience with the sprite stuff.
        self.rect = self
        
        self.x = 0
        self.y = 0
        self.width = 64
        self.height = 64
        
        self.sprites = {} #TODO Rename this. >.-.< 
        
        
    def draw(self, surface):
        if self.visible:         
            surface.blit(self.sprites[0], (self.rect.x, self.rect.y))