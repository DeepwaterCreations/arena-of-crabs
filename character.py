import pdb

import math

from enum import Enum

import pygame
from pygame.locals import *

import entity
from entity import Entity

enemies = pygame.sprite.Group()
#wall_colliders = pygame.sprite.Group()

class Character(Entity):
    
    Direction = Enum("Direction", "UP RIGHT DOWN LEFT");
    
    def __init__(self):
        Entity.__init__(self)
        
        self.collide_walls = True
        
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
        x_change = int(math.floor(self.movement['h'] * speed))
        y_change = int(math.floor(self.movement['v'] * speed))
       
        #Check for wall collisions
        def moveCollide(source, wall):
            source_move = source.copy()
            source_move.width += abs(x_change)
            source_move.x = min(source.x, source.x + x_change)
            source_move.height += abs(y_change)
            source_move.y = min(source.y, source.y + y_change)
            return source_move.colliderect(wall) #pygame.sprite.collide_rect(source_move, wall)
        walls = pygame.sprite.spritecollide(self, entity.walls, False, moveCollide)
        
        collision = None
        #Compare the difference between the character and the wall with the distance they're going to move.
        #If the latter is greater than the former, set the latter to the former and get the wall that's being collided with.
        for wall in walls:
            if wall.top < self.top < wall.bottom or wall.top < self.bottom < wall.bottom:
                if x_change > 0 and wall.left - self.right <= x_change:
                    collision = wall
                    x_change = wall.left - self.right
                elif x_change < 0 and wall.right - self.left >= x_change:
                    collision = wall
                    x_change = wall.right - self.left 
            
            if wall.left < self.left < wall.right or wall.left < self.right < wall.right:
                if y_change > 0 and wall.top - self.bottom <= y_change:
                    collision = wall
                    y_change = wall.top - self.bottom
                elif y_change < 0 and wall.bottom - self.top >= y_change:
                    collision = wall
                    y_change = wall.bottom - self.top
        
        self.x += x_change 
        self.y += y_change
        if collision:
            self.onWallCollision(collision)
    
    
    #By default, charactes will move when updated.
    def update(self, dt):
        self.makeMove(dt)
    
    def updateImage(self):
        '''Set the sprite's image property based on its current state.
            This is what will be drawn to the screen for the current frame.
        ''' 
        self.image = self.sprites[self.facing]
        
    def setHostile(self, is_hostile = True):
        """Add or remove this character from the group that can collide with the player for damage"""
        if is_hostile:
            enemies.add(self)
        else:
            enemies.remove(self)
    
    #def setWallCollider(self, collides_walls = True):
        #"""Add or remove this character from the group that can collide with the player for damage"""
        #if collides_walls:
            #wall_colliders.add(self)
        #else:
            #wall_colliders.remove(self)
    
    #TODO: Should be abstracted out into an interface?
    def onPlayerCollision(self, player):
        pass
    
    def onWallCollision(self, wall):
        pass
    
    def takeDamage(self, damage_amount):
        self.current_hitpoints -= damage_amount
        if self.current_hitpoints <= 0:
            self.die()
    
    def die(self):
        '''Play a death animation and remove this object from the game'''
        self.kill()