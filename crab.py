import pdb

import math

import pygame
from pygame.locals import *

from character import Character
from drawable import loadImage
from timerhandler import Timer
from attackhandler import Attackable

class Crab(Character, Attackable):
    
    def __init__(self):
        Character.__init__(self)
        Attackable.__init__(self)
        
        self.x = 250
        self.y = 250
        self.facing = Character.Direction.UP
        self.turn_freq = 1024
        self.walk_freq = 3072
        self.walk_duration = 512
        self.walk_speed = 256 
        
        self.damage_output = 1
        self.current_hitpoints = self.max_hitpoints = 3
        
        self.being_knocked_back = False #TODO: I'll probably want to make this more robust.
        
        self.setHostile()
        
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
        self.turntimer = Timer(self.turn_freq, self.makeTurn, should_repeat = True)
        Timer(self.walk_freq, self.makeWalk)
        
    def makeTurn(self, timer):
        """Spin in a circle"""
        if not self.being_knocked_back:
            facingIndex = self.facing.value
            self.facing = Character.Direction((facingIndex % 4) + 1)
        
    def makeWalk(self, timer):
        """Make the crab walk in the direction it's currently facing"""
        #if not self.being_knocked_back:
        self.turntimer.pause()
        self.setWalking(self.facing)
        Timer(self.walk_duration, self.endWalk)
        
    def endWalk(self, timer):
        """Stop the crab from walking forward"""
        self.haltWalking()
        Timer(self.walk_freq, self.makeWalk)
        self.turntimer.unpause()
        
    def onWeaponHit(self, weapon):
        #TODO: Allow multiple hits in a row?
        if self.being_knocked_back:
            return 
        self.being_knocked_back = True
        
        #Get the direction from the location of the weapon's attack origin to the location of self.
        hit_direction = {'x': self.centerx - weapon.atk_origin[0], 'y':  self.centery - weapon.atk_origin[1]}
        #Normalize
        length = math.sqrt(math.pow(hit_direction['x'], 2) + math.pow(hit_direction['y'], 2))
        if length == 0:
            length = 1
        hit_direction['x'] /= length
        hit_direction['y'] /= length
        #Combine the hit direction with the weapon force to get a knockback movement vector 
        #TODO: Could amend the attack force after getting it from the weapon. Weapon resistance, for instance. 
        self.knockback_vector = (hit_direction['x'] * weapon.getForce(), hit_direction['y'] * weapon.getForce()) 
        self.addMovementVector(self.knockback_vector[0], self.knockback_vector[1])
                
        #Set a timer to stop the motion? Duration based on attack power?
        hittimer = Timer(200, self.endWeaponHit) #TODO: Another place where I don't want a magic number.
        
        self.takeDamage(weapon.damage_output)
        
    def endWeaponHit(self, timer):
        self.addMovementVector(-self.knockback_vector[0], -self.knockback_vector[1])
        self.being_knocked_back = False
        
    def onPlayerCollision(self, player):
        player.onHit(self, self.damage_output)