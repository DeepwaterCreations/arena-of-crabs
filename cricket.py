import math

import pygame
from pygame.locals import *
pygame.init()

from drawable import Drawable, loadImage
from character import Character
from keyhandler import Keylistener
from entity import Entity

#This should not be the final structure of this!
#TODO: Structure for multiple held objects (weapons)
class Knife(Entity):
    def __init__(self):
        Entity.__init__(self)
        
        self.visible = False
    
        self.sprites[Character.Direction.UP] = loadImage('knifeb.bmp')
        self.sprites[Character.Direction.DOWN] = loadImage('knifef.bmp')
        self.sprites[Character.Direction.LEFT] = loadImage('knifel.bmp')
        self.sprites[Character.Direction.RIGHT] = loadImage('knifer.bmp')
    
        self.facing = Character.Direction.DOWN
        
    def draw(self, surface):
        if self.visible:         
            surface.blit(self.sprites[self.facing], (self.x, self.y))

class Cricket(Character, Keylistener):
    
    def __init__(self):
        Character.__init__(self)
        Keylistener.__init__(self)
        
        self.speed = 200;
        
        self.key_inputs = {'up': False, 
                           'down': False, 
                           'left': False, 
                           'right': False, 
                           'atk': False}
        
        self.knife = Knife()
    
    
        #What I eventually want: Load a sprite sheet, have a whole structure for getting sprites and picking frames and animation
    #and all that jazz.
    #Uhh, sprites. So. I have 
    #1. Different sprites for different states, such as walking, standing still, or swinging a sword. 
    #2. Different sprites that form the frames of an animation.
    #Each frame, I'll return exactly 1 of these sprites. Which one, however, is a bit complicated.
    #I have no idea if pygame's sprite stuff is useful here. What, for instance, constitutes a group? Are all the frames of an animation a group? All the animations for a single character?
    #My read of it is that an appropriate group is something more like "enemies". 
    #The collision detection and all would be nice to have. But, it isn't clear how to use the pygame sprites for animations.
    #I guess it's not like I can't extend the class.
    #Let's first make this work the quick and dirty way, with just four sprites for each direction, and then go from there. 
    #In fact, I don't need animations yet. I should add a single crab next, and then a dumb sword thing after that, and get to animations later.  
    
    def loadSprites(self):
        self.sprites[Character.Direction.UP] = loadImage('Cricket1b.bmp')
        self.sprites[Character.Direction.DOWN] = loadImage('Cricket1f.bmp')
        self.sprites[Character.Direction.LEFT] = loadImage('Cricket1l.bmp')
        self.sprites[Character.Direction.RIGHT] = loadImage('Cricket1r.bmp')
        
        
    def update(self, dt):
        if dt == 0:
            return
        
        #TODO: I want the currently held horizontal/vertical key to override a second key, so if I hold down two keys at once, I keep moving in the first direction.
        #When the first key is released, if the second is still being held down, immediately move in the other direction.
        if self.key_inputs['up']:
            self.y -= math.floor(self.speed * (dt/1000.0))
            self.facing = Character.Direction.UP
        elif self.key_inputs['down']:
            self.y += math.floor(self.speed * (dt/1000.0))
            self.facing = Character.Direction.DOWN
            
        if self.key_inputs['left']:
            self.x -= math.floor(self.speed * (dt/1000.0))
            self.facing = Character.Direction.LEFT
        elif self.key_inputs['right']:
            self.x += math.floor(self.speed * (dt/1000.0))            
            self.facing = Character.Direction.RIGHT
            
        if self.key_inputs['atk']:
            if self.facing == Character.Direction.UP:
                self.knife.facing = Character.Direction.UP
                self.knife.x = self.x
                self.knife.y = self.y - self.knife.height
                self.knife.visible = True
                
            elif self.facing == Character.Direction.DOWN:
                self.knife.facing = Character.Direction.DOWN
                self.knife.x = self.x
                self.knife.y = self.y + self.height
                self.knife.visible = True            
            
            elif self.facing == Character.Direction.LEFT:
                self.knife.facing = Character.Direction.LEFT
                self.knife.x = self.x - self.knife.width
                self.knife.y = self.y 
                self.knife.visible = True
            
            elif self.facing == Character.Direction.RIGHT:
                self.knife.facing = Character.Direction.RIGHT
                self.knife.x = self.x + self.width
                self.knife.y = self.y 
                self.knife.visible = True
        else:
            self.knife.visible = False
        
    def draw(self, surface):
        Character.draw(self, surface)
        self.knife.draw(surface)
        
        
    def handleKey(self, event):
        Keylistener.handleKey(self, event)
        
        if event.type == (KEYDOWN):
            if event.key == K_UP:
                self.key_inputs['up'] = True
            elif event.key == K_DOWN:
                self.key_inputs['down'] = True
            elif event.key == K_LEFT:
                self.key_inputs['left'] = True
            elif event.key == K_RIGHT:
                self.key_inputs['right'] = True
            elif event.key == K_LSHIFT:
                self.key_inputs['atk'] = True
        if event.type == (KEYUP):
            if event.key == K_UP:
                self.key_inputs['up'] = False
            elif event.key == K_DOWN:
                self.key_inputs['down'] = False
            elif event.key == K_LEFT:
                self.key_inputs['left'] = False
            elif event.key == K_RIGHT:
                self.key_inputs['right'] = False
            elif event.key == K_LSHIFT:
                self.key_inputs['atk'] = False
        