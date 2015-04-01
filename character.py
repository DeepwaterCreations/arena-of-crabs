import pdb

import math

from enum import Enum

import pygame
from pygame.locals import *

#from drawable import Drawable
from entity import Entity

enemies = pygame.sprite.Group()


class Character(Entity):
    
    Direction = Enum("Direction", "UP RIGHT DOWN LEFT");
    
    def __init__(self):
        Entity.__init__(self)
        
        self.max_speed = 100
        self.current_speed = 0
        self.movement = {'h':0.0, 'v':0.0} #Should range from -1 to 1. TODO: Do I want a unit vector?
        
        self.max_hitpoints = self.current_hitpoints = 10
        
        self.sprites = {
            Character.Direction.UP : 0, 
            Character.Direction.RIGHT : 0, 
            Character.Direction.DOWN : 0, 
            Character.Direction.LEFT : 0
                }
        self.facing = Character.Direction.DOWN

    #This should typically be called by a subclass's update function.
    def makeMove(self, dt):
        speed = self.current_speed * (dt/1000.0)
        self.x += int(math.floor(self.movement['h'] * speed))
        self.y += int(math.floor(self.movement['v'] * speed))
    
    #By default, charactes will move when updated.
    def update(self, dt):
        self.makeMove(dt)
    
    def updateImage(self):
        self.image = self.sprites[self.facing]
        
    def setHostile(self, is_hostile = True):
        """Add or remove this character from the group that can collide with the player for damage"""
        if is_hostile:
            enemies.add(self)
        else:
            enemies.remove(self)
        
    #TODO: Should be abstracted out into an interface?
    def onPlayerCollision(self, player):
        pass