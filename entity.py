import pdb

import pygame
from pygame.locals import *

from drawable import Drawable, loadImage
from updatable import Updatable

walls = pygame.sprite.Group()

class Entity(Drawable, Updatable, pygame.Rect):
    
    #TODO: Rect constructors
    def __init__(self, layer="Character"):
        Drawable.__init__(self, layer)
        Updatable.__init__(self) 
        
        #Assuming this even works, it's for my convenience with the sprite stuff.
        self.rect = self
        
        self.x = 0
        self.y = 0
        self.width = 64
        self.height = 64
        
        self.sprites = {0: loadImage("no_image.bmp")} #TODO Rename this. >.-.< 
        
    def setWall(self, is_wall = True):
        """Add or remove this entity from the group that will block most characters"""
        if is_wall:
            walls.add(self)
        else:
            walls.remove(self)
        
    def draw(self):        
        self.image = self.sprites[0]
        
class Wall(Entity):
    def __init__(self, x, y, w, h):
        Entity.__init__(self, layer="Floor")
        pygame.Rect.__init__(self, x, y, w, h)
        
        self.setWall()
        
        self.image = pygame.Surface((self.w, self.h))
        self.image.fill((255, 0, 255))