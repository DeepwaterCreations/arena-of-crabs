import pdb

import pygame
from pygame.locals import *

from drawable import Drawable, loadImage
from updatable import Updatable

walls = pygame.sprite.Group()

class Entity(Drawable, Updatable):
    
    #TODO: Rect constructors
    def __init__(self, layer="Character"):
        Drawable.__init__(self, layer)
        Updatable.__init__(self) 
        
        self.rect = pygame.Rect(0, 0, 64, 64)
        
        self.sprites = {0: loadImage("no_image.bmp")} #TODO Rename this. >.-.< 
        
    def setWall(self, is_wall = True):
        """Add or remove this entity from the group that will block most characters"""
        if is_wall:
            walls.add(self)
        else:
            walls.remove(self)
        
    def draw(self):        
        self.image = self.sprites[0]
        
    def setLocation(self, x = None, y = None):
        if x is None:
            x = self.rect.x
        if y is None:
            y = self.rect.y
        self.rect.x = x
        self.rect.y = y
        
class Wall(Entity):
    def __init__(self, x, y, w, h):
        Entity.__init__(self, layer="Floor")
        #pygame.Rect.__init__(self, x, y, w, h)

        self.rect = pygame.Rect(x, y, w, h)
        
        self.setWall()
        
        self.image = pygame.Surface((self.rect.w, self.rect.h))
        self.image.fill((255, 0, 255))
        self.visible = False
