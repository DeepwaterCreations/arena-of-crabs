import pdb

import pygame
from pygame.locals import *

from drawable import Drawable
from updatable import Updatable
from cricket import Cricket 

class Hud(Drawable, Updatable):

    hud_elements = []

    def __init__(self, hud_space):
        Drawable.__init__(self, "Hud_BG")
        Updatable.__init__(self)

        self.rect = hud_space
        
        #Make a black box for the background
        self.background = pygame.Surface( (self.rect.width, self.rect.height) )
        self.background.fill( (0,0,0) )

        #Make a simple health bar
        health_bar_box = pygame.Rect(self.rect.width/2 + 64, 16, self.rect.width/2 - 128, 32)
        health_bar_box.x += self.rect.x
        health_bar_box.y += self.rect.y
        self.health_bar = HealthBar(health_bar_box) 
    
    def updateImage(self):
        self.image = self.background

    #TODO: Make this suck less. Totally rough draft code.
    def registerListeners(self, cricket):
        cricket.addTakeDamageListener(self.health_bar)


class HudElement(Drawable, Updatable):

    def __init__(self):
        Drawable.__init__(self, "Hud_Elem")
        Updatable.__init__(self)

        Hud.hud_elements.append(self)

class HealthBar(HudElement):

    def __init__(self, rect):
        HudElement.__init__(self)

        self.rect = rect
        self.image = pygame.Surface((self.rect.width, self.rect.height))

        self.filled = 1.0 #Using decimal instead of percentage values.

    def updateImage(self):
        self.image.fill((255,0,0))
        green_bar = pygame.Rect(0, 0, self.rect.width * self.filled, self.rect.height)
        self.image.fill((0,255,0), green_bar) 

    def onCricketTakesDamage(self, current_hitpoints, max_hitpoints):
        #Poor man's typecast. I hear this is better than actually casting, because it 
        #behaves better for certain types that max_hitpoints might be (but let's face
        #it, won't ever actually.) Anyway, I have to do something, or it's integer
        #division and herp de derp.
        self.filled = current_hitpoints / (max_hitpoints * 1.0)
