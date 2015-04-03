import pdb

import pygame
from pygame.locals import *

import attackhandler
from drawable import loadImage
from entity import Entity
from character import Character
from timerhandler import Timer    

#TODO: Structure for multiple held objects (weapons)
class Knife(Entity):
    def __init__(self):
        Entity.__init__(self)
    
        self.slash_duration = 64
        self.damage_output = 1
    
        self.setVisible(False)
    
        self.hold_sprites = {}
        self.hold_sprites[Character.Direction.UP] = loadImage('knifeb.bmp')
        self.hold_sprites[Character.Direction.RIGHT] = loadImage('knifer.bmp')
        self.hold_sprites[Character.Direction.DOWN] = loadImage('knifef.bmp')
        self.hold_sprites[Character.Direction.LEFT] = loadImage('knifel.bmp')
    
        #TODO: For dual-handed whatevers, these shouldn't be keyed to character directions after all. (If I ever do that.) 
        self.swing_sprites = {}
        self.swing_sprites[Character.Direction.UP] = loadImage('knifeslashne.bmp')
        self.swing_sprites[Character.Direction.RIGHT] = loadImage('knifeslashse.bmp')
        self.swing_sprites[Character.Direction.DOWN] = loadImage('knifeslashsw.bmp')
        self.swing_sprites[Character.Direction.LEFT] = loadImage('knifeslashnw.bmp')
    
        self.sprites = self.hold_sprites #Change self.sprites to the appropriate set...?
    
        self.facing = Character.Direction.DOWN
        self.attacker = None        
        self.attacking = False
        self.is_slash = False
        
        self.atk_origin = [0, 0]
        self.slash_timer = Timer(self.slash_duration, self.finishSlash)
        self.slash_timer.pause()
        
    def updateImage(self):
        self.image = self.sprites[self.facing]
               
               
    def attack(self, attacker, direction):
        self.facing = direction
        self.attacker = attacker
        
        if not self.attacking:
            self.attacking = True
            self.is_slash = True
            self.sprites = self.swing_sprites   
        
            self.slash_timer.reset()
            self.slash_timer.unpause()
        
        if self.facing == Character.Direction.UP:
            if self.is_slash:
                self.atk_origin = self.bottomleft = self.attacker.topright
            else:
                self.atk_origin = self.midbottom = self.attacker.midtop
            
        elif self.facing == Character.Direction.RIGHT:
            if self.is_slash:
                self.atk_origin = self.topleft = self.attacker.bottomright
            else:
                self.atk_origin = self.midleft = self.attacker.midright
            
        elif self.facing == Character.Direction.DOWN:
            if self.is_slash:
                self.atk_origin = self.topright = self.attacker.bottomleft
            else:
                self.atk_origin = self.midtop = self.attacker.midbottom
                
        elif self.facing == Character.Direction.LEFT:
            if self.is_slash:
                self.atk_origin = self.bottomright = self.attacker.topleft
            else:
                self.atk_origin = self.midright = self.attacker.midleft
        
        self.setVisible(True)
        attackhandler.makeAttack(self)
                 
    def finishSlash(self, timer):
        self.is_slash = False
        self.sprites = self.hold_sprites
        
    def endAttack(self):
        '''Reset for a new attack.'''
        self.slash_timer.pause()
        self.setVisible(False)
        self.attacking = False
               
