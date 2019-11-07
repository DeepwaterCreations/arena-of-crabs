import pdb

import pygame
from pygame.locals import *

from drawable import Drawable, loadImage
from updatable import Updatable
from cricket import Cricket 
from spritesheet import SpriteSheet

class DeathMessage(Drawable, Updatable):

    def __init__(self, screen_space):
        Drawable.__init__(self, "Hud_Elem")
        Updatable.__init__(self)

        textheight = 16
        self.rect = pygame.Rect(screen_space.width/3, 
                                screen_space.height/2 + (textheight/2),
                                screen_space.width/3,
                                textheight)
        self.image = pygame.Surface((self.rect.width, self.rect.height))
        self.setVisible(False)

    def updateImage(self):
        #Just make a dumb blue box until I get stuff figured
        self.image.fill((0,0,225))

    def onCricketDeath(self):
        self.setVisible(True)
