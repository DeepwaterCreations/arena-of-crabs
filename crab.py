import pdb

import math

import pygame
from pygame.locals import *

from character import Character
from drawable import loadImage
from timerhandler import Timer#, RepeatingTimer
from attackhandler import Attackable

class Crab(Character, Attackable):
    
    def __init__(self):
        Character.__init__(self)
        Attackable.__init__(self)
        
        self.x = 250
        self.y = 250
        self.facing = Character.Direction.UP
        self.turnFreq = 1000
        
        self.being_knocked_back = False #TODO: I'll probably want to make this more robust.
        
        spritesheet = loadImage("MonstersBeach.bmp");
        
        self.sprites[Character.Direction.UP] = pygame.Surface((64, 64))    
        self.sprites[Character.Direction.UP].blit(spritesheet, (0,0), (4, 4, 64, 64))   
        self.sprites[Character.Direction.UP].set_colorkey(self.sprites[Character.Direction.UP].get_at((0,0)), RLEACCEL)
        
        self.sprites[Character.Direction.RIGHT] = pygame.Surface((64, 64))    
        self.sprites[Character.Direction.RIGHT].blit(spritesheet, (0,0), (140, 4, 64, 64))   
        self.sprites[Character.Direction.RIGHT].set_colorkey(self.sprites[Character.Direction.RIGHT].get_at((0,0)), RLEACCEL)
        
        self.sprites[Character.Direction.DOWN] = pygame.Surface((64, 64))    
        self.sprites[Character.Direction.DOWN].blit(spritesheet, (0,0), (140, 72, 64, 64))   
        self.sprites[Character.Direction.DOWN].set_colorkey(self.sprites[Character.Direction.DOWN].get_at((0,0)), RLEACCEL)
        
        self.sprites[Character.Direction.LEFT] = pygame.Surface((64, 64))   
        self.sprites[Character.Direction.LEFT].blit(spritesheet, (0,0), (4, 72, 64, 64))   
        self.sprites[Character.Direction.LEFT].set_colorkey(self.sprites[Character.Direction.LEFT].get_at((0,0)), RLEACCEL)
        
        #Set timer for turning
        self.turntimer = Timer(self.turnFreq, self.handletimer, should_repeat = True)
        
    def handletimer(self, timer):
        #Spin in a circle
        if timer == self.turntimer:
            if not self.being_knocked_back:
                facingIndex = self.facing.value
                self.facing = Character.Direction((facingIndex % 4) + 1)
        
    def onWeaponHit(self, weapon):
        #TODO: Allow multiple hits in a row?
        if self.being_knocked_back:
            return 
        self.being_knocked_back = True
        
        #Get the direction from the location of the weapon's attack origin to the location of self.
        self.hit_direction = {'x': self.centerx - weapon.atk_origin[0], 'y':  self.centery - weapon.atk_origin[1]}
        length = math.sqrt(math.pow(self.hit_direction['x'], 2) + math.pow(self.hit_direction['y'], 2))
        self.hit_direction['x'] /= length
        self.hit_direction['y'] /= length
        self.movement['h'] += self.hit_direction['x']
        self.movement['v'] += self.hit_direction['y']
        
        #Move in that direction at a calculated speed (based on "traction" stat and attack power?)
        self.current_speed = 640 #TODO: Calculated number instead of magic, if you please.
        
        #Set a timer to stop the motion? Duration based on attack power?
        hittimer = Timer(200, self.endWeaponHit) #TODO: Another place where I don't want a magic number.
   
        
    def endWeaponHit(self, timer):
        #BUG: This will cause bad things to happen if onWeaponHit is called twice before we get here. 
        self.movement['h'] -= self.hit_direction['x']
        self.movement['v'] -= self.hit_direction['y']
        self.current_speed = 0 #TODO: This is also wrong.
        self.being_knocked_back = False
        