import pdb

import pygame
from pygame.locals import *

from character import Character
from entity import Entity
from spritesheet import SpriteSheet


class Decoration(Entity):
    '''A non-interactable, non-blocking object that might have an animation.'''

    def __init__(self, layer="Floor", spritepath=None):
        Entity.__init__(self, layer)
        if spritepath != None:
            self.sprites = {0: loadImage(spritepath)}

import random

class WallTorch(Decoration):
    '''A flickering wall torch'''

    def __init__(self, direction):
        Decoration.__init__(self)
        self.facing = direction
        self.anim_frame = 0
        self.anim_speed = 100 #ms between flickers
        self.flicker_timer = 0
        self.flickering = False
        self.stability = 6 #Odds of switching between flickering and not flickering on a given flicker are 1/this.  

        self.sprites = {}
        self.loadSprites()
        
    def loadSprites(self):
        #TODO: Am I exporting this image with transparency already in? Why does "False" have no back-fill.
        #and True have no back-fill but also no shadow?
        spritesheet = SpriteSheet("torch_sheet_1_Large.bmp", use_transparency = False)

        self.sprites[0] = spritesheet.getSprite(0, self.facing.value - 1)
        self.sprites[1] = spritesheet.getSprite(1, self.facing.value - 1)
        self.sprites[2] = spritesheet.getSprite(2, self.facing.value - 1)

        self.image = self.sprites[self.anim_frame]

    def update(self, dt):
        if dt == 0:
            return      

        self.flicker_timer += dt

        if self.flicker_timer > self.anim_speed:
            #First, check if we're changing between flicker and not-flicker.
            if random.randint(0, self.stability) == 0:
                self.flickering = not self.flickering            

            #Then, if we're flickering, pick a random frame to switch to.
            if self.flickering:
                self.anim_frame = random.randint(0, 2)

            #Finally, set the image and reset the timer.
            self.image = self.sprites[self.anim_frame]
            self.flicker_timer = 0


class OneOff(Decoration):

    def __init__(self, layer, animation):
        Decoration.__init__(self, layer)
        self.animation = animation

    def loadSprites(self):
        pass

    def update(self, dt):
        if dt == 0:
            return

        self.animation.update(dt)
        self.image = self.animation.getCurrentFrame()
       



        

        
