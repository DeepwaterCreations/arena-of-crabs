import pdb

import math

from enum import Enum

import pygame
from pygame.locals import *

import entity
from entity import Entity
from timerhandler import KnockbackTimer 

enemies = pygame.sprite.Group()
#wall_colliders = pygame.sprite.Group()

class Character(Entity):
    
    Direction = Enum("Direction", "UP RIGHT DOWN LEFT");
    
    def __init__(self):
        Entity.__init__(self)
        
        self.collide_walls = True
        
        self.walk_speed = 100
        self._movement_vectors = []
        self._walking = {
            Character.Direction.UP : False, 
            Character.Direction.RIGHT : False, 
            Character.Direction.DOWN : False, 
            Character.Direction.LEFT : False
                }        
        
        self.max_hitpoints = self.current_hitpoints = 10
        self.hitbar_health_color = 0, 255, 0
        self.hitbar_damage_color = 255, 0, 0
        
        self.sprites = {
            Character.Direction.UP : 0, 
            Character.Direction.RIGHT : 0, 
            Character.Direction.DOWN : 0, 
            Character.Direction.LEFT : 0
                }
        self.facing = Character.Direction.DOWN

    #This should typically be called by a subclass's update function.
    def makeMove(self, dt):
        """Combines movement and walking vectors into a single vector, checks collisions,
        moves the character, and calls the wall collision handler if relevant.

        Yuck. This should be, what, four different methods? I should change that soon.
        """
        #Remove empty vectors. These are vectors that have timed out/become irrelevant.
        for vector in self._movement_vectors:
            if len(vector) == 0:
                self._movement_vectors.remove(vector)
                
        walking_vector = self.getWalkingVector()
        move_x = sum(vector[0] for vector in self._movement_vectors) + walking_vector[0]
        move_y = sum(vector[1] for vector in self._movement_vectors) + walking_vector[1]
        movement = (move_x, move_y)
        
        x_change = movement[0] * (dt/1000.0)
        y_change = movement[1] * (dt/1000.0)
       
        #Check for wall collisions
        def moveCollide(source, wall):
            source_move = source.rect.copy()
            #First, expand the source rect's width based on the movement distance.
            #This will move the right side of the rect out while keeping the left stationary.
            source_move.width += abs(x_change)
            #Then, if the movement is to the left, move the rect left.
            #The result will be a rect that covers both the original bounding box, and all the 
            #space that the rect will pass over or touch when it moves
            source_move.x = min(source.rect.x, source.rect.x + x_change)
            #Do the same for vertical movement, of course.
            #NOTE: We'll get slop here, won't we? Diagonal movement
            #makes a box that covers more than just the movement. Could that be the source of my bug?
            #Or am I only getting a list of possible collision candidates? 
            source_move.height += abs(y_change)
            source_move.y = min(source.rect.y, source.rect.y + y_change)
            #Finally, check if the movement box intersects with the wall and return the result.  
            return source_move.colliderect(wall) #pygame.sprite.collide_rect(source_move, wall)
        walls = pygame.sprite.spritecollide(self, entity.walls, False, moveCollide)
        
        collision = None
        #Compare the difference between the character and the wall with the distance they're going to move.
        #If the latter is greater than the former, set the latter to the former and get the wall that's being collided with.
        #Note that "walls" is only walls which the previous function call caught as potential collisions.
        for wall in walls: 
            if wall.rect.top <= self.rect.top < wall.rect.bottom or wall.rect.top < self.rect.bottom <= wall.rect.bottom:
                if x_change > 0 and wall.rect.left - self.rect.right <= x_change:
                    collision = wall
                    x_change = wall.rect.left - self.rect.right
                elif x_change < 0 and wall.rect.right - self.rect.left >= x_change:
                    collision = wall
                    x_change = wall.rect.right - self.rect.left 
            
            if wall.rect.left <= self.rect.left < wall.rect.right or wall.rect.left < self.rect.right <= wall.rect.right:
                if y_change > 0 and wall.rect.top - self.rect.bottom <= y_change:
                    collision = wall
                    y_change = wall.rect.top - self.rect.bottom
                elif y_change < 0 and wall.rect.bottom - self.rect.top >= y_change:
                    collision = wall
                    y_change = wall.rect.bottom - self.rect.top
        
        self.rect.x += x_change 
        self.rect.y += y_change
        if collision:
            self.onWallCollision(collision)
    
    def addMovementVector(self, x, y):
        """Add a vector to the character's movement that will impact the direction/speed he moves when makeMove() is called""" 
        self._movement_vectors.append([x, y])
        
     
    def setWalking(self, direction, is_walking = True):
        """Set the character's walking state for the given direction.
        
            Every direction the character is walking will add a vector to movement in the given direction, at the character's max speed.
        """
        self._walking[direction] = is_walking
        
    def haltWalking(self):
        """Stop the character from walking"""
        self._walking = self._walking.fromkeys(self._walking, False)
        
    def getWalkingVector(self):
        """Return a vector to represent the character's current attempt to move itself"""
        x = 0
        y = 0
        if self._walking[Character.Direction.UP]:
            y -= self.walk_speed
        if self._walking[Character.Direction.RIGHT]:
            x += self.walk_speed
        if self._walking[Character.Direction.DOWN]:
            y += self.walk_speed
        if self._walking[Character.Direction.LEFT]:
            x -= self.walk_speed
        return (x, y)
            
    def isWalking(self):
        return self._walking[Character.Direction.UP] or self._walking[Character.Direction.RIGHT] or self._walking[Character.Direction.DOWN] or self._walking[Character.Direction.LEFT] 
            
    def addKnockbackVector(self, source_position, force):
        """Add a movement vector away from source_position, then set a timer to remove it."""
        #Get the direction from source_position to the location of self.
        hit_direction = {'x': self.rect.centerx - source_position[0], 'y':  self.rect.centery - source_position[1]}
        #Normalize
        length = math.sqrt(math.pow(hit_direction['x'], 2) + math.pow(hit_direction['y'], 2))
        if length == 0:
            length = 1
        hit_direction['x'] /= length
        hit_direction['y'] /= length
        #Combine the hit direction with the force to get a knockback movement vector 
        self.knockback_vector = [hit_direction['x'] * force, hit_direction['y'] * force] 
        #self.addMovementVector(self.knockback_vector[0], self.knockback_vector[1])
        self._movement_vectors.append(self.knockback_vector)
        #Set a timer
        hittimer = KnockbackTimer(200, self.knockback_vector, self.endWeaponHit)

    def endWeaponHit(self, timer):
        pass
        
    #By default, charactes will move when updated.
    def update(self, dt):
        self.makeMove(dt)
    
    def updateImage(self):
        '''Set the sprite's image property based on its current state.
            This is what will be drawn to the screen for the current frame.
        ''' 
        self.image = self.sprites[self.facing]
        #Draw the hitpoint bar:
        bar_height = self.image.get_height()
        pygame.draw.rect(self.image, self.hitbar_health_color, Rect(0,0,3,bar_height))
        #Only draw damage if there is damage. (A bar with 0 height still shows as one pixel.)
        if self.current_hitpoints < self.max_hitpoints:
            damage_bar_height = (bar_height/self.max_hitpoints)*(self.max_hitpoints - self.current_hitpoints)
            pygame.draw.rect(self.image, self.hitbar_damage_color, Rect(0,0,3,damage_bar_height))
        
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
