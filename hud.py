import pdb

import pygame
from pygame.locals import *

from drawable import Drawable
from updatable import Updatable

class Hud(Drawable, Updatable):

    hud_elements = []

    def __init__(self, hud_space, layer="Hud"):
        Drawable.__init__(self, layer)
        Updatable.__init__(self)

        self.rect = hud_space
        
        #Make a black box for the background
        self.background = pygame.Surface( (self.rect.width, self.rect.height) )
        #self.background = pygame.Surface( (64, 64) )
        self.background.fill( (0,0,0) )
    
    def updateImage(self):
        self.image = self.background
