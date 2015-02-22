from enum import Enum

import pygame
from pygame.locals import *
pygame.init()

import drawable

class Character(drawable.Drawable):
    
    Direction = Enum("Direction", "UP DOWN LEFT RIGHT");
    
    def __init__(self):
        drawable.Drawable.__init__(self)
        
        self.x = 0
        self.y = 0
        
        self.speed = 100
        
        self.sprites = {
            Character.Direction.UP : 0, 
            Character.Direction.DOWN : 0, 
            Character.Direction.LEFT : 0, 
            Character.Direction.RIGHT : 0
                }
        self.facing = Character.Direction.DOWN
        
    
    def draw(self, surface):        
        surface.blit(self.sprites[self.facing], (self.x, self.y))