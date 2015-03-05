import pygame
from pygame.locals import *
pygame.init()

from drawable import Drawable

class Entity(Drawable, pygame.Rect):
    
    #TODO: Rect constructors
    def __init__(self):
        Drawable.__init__(self)
        
        self.x = 0
        self.y = 0
        self.width = 64
        self.height = 64
        
        self.sprites = {}
        
        
    def draw(self, surface):
        if self.visible:         
            surface.blit(self.sprites[0], (self.rect.x, self.rect.y))