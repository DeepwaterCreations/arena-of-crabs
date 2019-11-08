import pdb

import pygame
from pygame.locals import *

import text
from drawable import Drawable, loadImage
from updatable import Updatable
from cricket import Cricket 
from spritesheet import SpriteSheet

class DeathMessage(Drawable, Updatable):

    def __init__(self, screen_space):
        Drawable.__init__(self, "Hud_Elem")
        Updatable.__init__(self)
        
        message = "Game Over"

        self.image = text.getStringSurface(message)
        self.rect = self.image.get_rect()
        self.rect.x = (screen_space.width/2 - self.rect.width/2)
        self.rect.y = (screen_space.height/2)
        self.setVisible(False)

    def onCricketDeath(self):
        self.setVisible(True)
