import pdb
import math

import pygame
from pygame.locals import *

import attackhandler
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
    
        self.atk_origin = [0, 0]
    
        self.facing = Character.Direction.DOWN
        
    def draw(self, surface):
        if self.visible:         
            surface.blit(self.sprites[self.facing], (self.x, self.y))
                
    def attack(self, attacker, direction):
        #Set the position and facing
        self.facing = direction
        
        if direction == Character.Direction.UP:
            #self.x = attacker.x
            #self.y = attacker.y - self.height
            self.atk_origin = self.midbottom = attacker.midtop
            
        elif direction == Character.Direction.DOWN:
            #self.x = attacker.x
            #self.y = attacker.y + attacker.height
            self.atk_origin = self.midtop = attacker.midbottom
        
        elif direction == Character.Direction.LEFT:
            #self.x = attacker.x - self.width
            #self.y = attacker.y 
            self.atk_origin = self.midright = attacker.midleft
        
        elif direction == Character.Direction.RIGHT:
            #self.x = attacker.x + attacker.width
            #self.y = attacker.y
            self.atk_origin = self.midleft = attacker.midright
        
        self.visible = True
        attackhandler.makeAttack(self)

        

class Cricket(Character, Keylistener):
    
    def __init__(self):
        Character.__init__(self)
        Keylistener.__init__(self)
        
        self.max_speed = 200;
        
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
        
        # I want the currently held horizontal/vertical key to override a second key, so if I hold down two keys at once, I keep moving in the first direction.
        #When the first key is released, if the second is still being held down, immediately move in the other direction.
        #Therefore, check for the opposite key before setting the movement variables for a given key.
        if not self.key_inputs['down']:
            if self.key_inputs['up']:
                self.movement['v'] = -1 
                self.facing = Character.Direction.UP
            else:        
                self.movement['v'] = 0
                
        if not self.key_inputs['up']:
            if self.key_inputs['down']:
                self.movement['v'] = 1
                self.facing = Character.Direction.DOWN
            else:
                self.movement['v'] = 0
        
        if not self.key_inputs['right']:
            if self.key_inputs['left']: 
                self.movement['h'] = -1
                self.facing = Character.Direction.LEFT
            else:
                self.movement['h'] = 0
                
        if not self.key_inputs['left']:
            if self.key_inputs['right']:
                self.movement['h'] = 1
                self.facing = Character.Direction.RIGHT
            else:
                self.movement['h'] = 0
            
        if self.key_inputs['up'] or self.key_inputs['down'] or self.key_inputs['left'] or self.key_inputs['right']:
            self.current_speed = self.max_speed
        else:
            self.current_speed = 0
            
        if self.key_inputs['atk']:
            self.knife.attack(self, self.facing)        
        else:
            self.knife.visible = False
        
        Character.make_move(self, dt)
    
        
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
        