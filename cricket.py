import pdb
import math

import pygame
from pygame.locals import *

import attackhandler
from drawable import Drawable, loadImage
from character import Character
from keyhandler import Keylistener
from entity import Entity
from animation import Animation


#This should not be the final structure of this!
#TODO: Structure for multiple held objects (weapons)
class Knife(Entity):
    def __init__(self):
        Entity.__init__(self)
        
        self.setVisible(False)
    
        self.sprites[Character.Direction.UP] = loadImage('knifeb.bmp')
        self.sprites[Character.Direction.DOWN] = loadImage('knifef.bmp')
        self.sprites[Character.Direction.LEFT] = loadImage('knifel.bmp')
        self.sprites[Character.Direction.RIGHT] = loadImage('knifer.bmp')
    
        self.atk_origin = [0, 0]
    
        self.facing = Character.Direction.DOWN
        
    def updateImage(self):
        self.image = self.sprites[self.facing]
                
    def attack(self, attacker, direction):
        #Set the position and facing
        self.facing = direction
        
        if direction == Character.Direction.UP:
            self.atk_origin = self.midbottom = attacker.midtop
            
        elif direction == Character.Direction.DOWN:
            self.atk_origin = self.midtop = attacker.midbottom
        
        elif direction == Character.Direction.LEFT:
            self.atk_origin = self.midright = attacker.midleft
        
        elif direction == Character.Direction.RIGHT:
            self.atk_origin = self.midleft = attacker.midright
        
        self.setVisible(True)
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
        
        self.lock_face = False
        self.walking = False
    
        self.anim_timer = 0
    
    #What I eventually want: Load a sprite sheet, have a whole structure for getting sprites and picking frames and animation
    #and all that jazz.
    #Uhh, sprites. So. I have 
    #1. Different sprites for different states, such as walking, standing still, or swinging a sword. 
    #2. Different sprites that form the frames of an animation.
    #Each frame, I'll return exactly 1 of these sprites. Which one, however, is a bit complicated.
    
    def loadSprites(self):
        self.sprites[Character.Direction.UP] = loadImage('Cricket1b.bmp')
        self.sprites[Character.Direction.DOWN] = loadImage('Cricket1f.bmp')
        self.sprites[Character.Direction.LEFT] = loadImage('Cricket1l.bmp')
        self.sprites[Character.Direction.RIGHT] = loadImage('Cricket1r.bmp')
        
        self.walk_anim = {}
        self.walk_anim[Character.Direction.UP] = Animation([(loadImage('Cricket1b.bmp'), 128), 
                                                  (loadImage('Cricket1bwalkl.bmp'), 128), 
                                                  (loadImage('Cricket1b.bmp'), 128),
                                                  (loadImage('Cricket1bwalkr.bmp'), 128)])
        self.walk_anim[Character.Direction.DOWN] = [loadImage('Cricket1f.bmp')]
        self.walk_anim[Character.Direction.LEFT] = [loadImage('Cricket1l.bmp')]
        self.walk_anim[Character.Direction.RIGHT] = [loadImage('Cricket1r.bmp')]
        
    def update(self, dt):
        if dt == 0:
            return
        
        # I want the currently held horizontal/vertical key to override a second key, so if I hold down two keys at once, I keep moving in the first direction.
        #When the first key is released, if the second is still being held down, immediately move in the other direction.
        #Therefore, check for the opposite key before setting the movement variables for a given key.
        #TODO: Set these relative instead of absolute, so as not to override movement inflicted from a different source
        if not self.key_inputs['down']:
            if self.key_inputs['up']:
                self.movement['v'] = -1 
                if not self.lock_face: self.facing = Character.Direction.UP
            else:        
                self.movement['v'] = 0
                
        if not self.key_inputs['up']:
            if self.key_inputs['down']:
                self.movement['v'] = 1
                if not self.lock_face: self.facing = Character.Direction.DOWN
            else:
                self.movement['v'] = 0
        
        if not self.key_inputs['right']:
            if self.key_inputs['left']: 
                self.movement['h'] = -1
                if not self.lock_face: self.facing = Character.Direction.LEFT
            else:
                self.movement['h'] = 0
                
        if not self.key_inputs['left']:
            if self.key_inputs['right']:
                self.movement['h'] = 1
                if not self.lock_face: self.facing = Character.Direction.RIGHT
            else:
                self.movement['h'] = 0
            
        if self.key_inputs['up'] or self.key_inputs['down'] or self.key_inputs['left'] or self.key_inputs['right']:
            self.current_speed = self.max_speed
            self.walking = True
        else:
            self.current_speed = 0
            self.walking = False
            
        if self.key_inputs['atk']:
            self.knife.attack(self, self.facing)
            self.lock_face = True
        else:
            self.knife.setVisible(False) #TODO: Instead, call knife.endAttack()
            self.lock_face = False
        
        Character.make_move(self, dt)
        
        #TODO: Maybe self.current_anim.update()? Or maybe it's high time I made Updatable a thing.
        self.walk_anim[Character.Direction.UP].update(dt)
        
    def updateImage(self):
        Character.updateImage(self)
        if self.walking and self.facing == Character.Direction.UP:
            self.image = self.walk_anim[Character.Direction.UP].getCurrentFrame() 
        self.knife.updateImage()
        
        
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
        