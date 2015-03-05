from enum import Enum

import pygame
from pygame.locals import *
pygame.init()

import drawable
import entity

class Character(entity.Entity):
    
    Direction = Enum("Direction", "UP RIGHT DOWN LEFT");
    
    def __init__(self):
        entity.Entity.__init__(self)
        
        self.speed = 100
        
        self.sprites = {
            Character.Direction.UP : 0, 
            Character.Direction.RIGHT : 0, 
            Character.Direction.DOWN : 0, 
            Character.Direction.LEFT : 0
                }
        self.facing = Character.Direction.DOWN
        
    
    def draw(self, surface):
        if self.visible:         
            surface.blit(self.sprites[self.facing], (self.x, self.y))