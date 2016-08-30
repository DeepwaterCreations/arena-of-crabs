import pdb

import math

import pygame
from pygame.locals import *

from character import Character
from spritesheet import SpriteSheet
from timerhandler import Timer
from attackhandler import Attackable
from animation import Animation

class Crab(Character, Attackable):
    
    def __init__(self, crabspawner):
        Character.__init__(self)
        Attackable.__init__(self)
        
        self.rect.x = 250
        self.rect.y = 250
        self.facing = Character.Direction.UP
        self.turn_freq = 1024
        self.walk_freq = 3072
        self.walk_duration = 512
        self.walk_speed = 256 
        
        self.damage_output = 1
        self.current_hitpoints = self.max_hitpoints = 3
        
        self.being_knocked_back = False #TODO: I'll probably want to make this more robust.
        
        self.setHostile()
        
        spritesheet = SpriteSheet("MonstersBeach.bmp", border = 4);
        
        self.sprites[Character.Direction.UP] = Animation([
                                         (spritesheet.getSprite(0, 0), 128),
                                         (pygame.transform.flip(spritesheet.getSprite(1, 0), True, False), 128)
                                         ])
        self.sprites[Character.Direction.RIGHT] = Animation([
                                         (spritesheet.getSprite(2, 0), 128),
                                         (pygame.transform.flip(spritesheet.getSprite(2, 0), False, True), 128)
                                         ])
        self.sprites[Character.Direction.DOWN] = Animation([
                                         (spritesheet.getSprite(2, 1), 128),
                                         (pygame.transform.flip(spritesheet.getSprite(2, 1), True, False), 128)
                                         ])
        self.sprites[Character.Direction.LEFT] = Animation([
                                         (spritesheet.getSprite(0, 1), 128),
                                         (pygame.transform.flip(spritesheet.getSprite(0, 1), False, True), 128)
                                         ])
        
        #Set timer for turning
        self.turntimer = Timer(self.turn_freq, self.makeTurn, should_repeat = True)
        Timer(self.walk_freq, self.makeWalk)

        self.parent_spawn = crabspawner 
        
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
        self.addKnockbackVector(weapon.getAttackOrigin(), weapon.getForce())
        self.takeDamage(weapon.damage_output)
        
    def endWeaponHit(self, timer):
        #self.addMovementVector(-self.knockback_vector[0], -self.knockback_vector[1])
        self.being_knocked_back = False #TODO: Make this part of character?
        
    def onPlayerCollision(self, player):
        player.onHit(self, self.damage_output)

    def die(self):
        '''Play a death animation, alert the spawn, and remove this object from the game'''
        self.parent_spawn.crabKilledTrigger()
        self.kill()
