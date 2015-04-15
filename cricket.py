import pdb
import math

import pygame
from pygame.locals import *

#import attackhandler
import weapons
from drawable import Drawable, loadImage, getSpritesheetSprite
from character import Character
from keyhandler import Keylistener
from entity import Entity
from animation import Animation
from timerhandler import Timer      

class Cricket(Character, Keylistener):
    
    def __init__(self):
        Character.__init__(self)
        Keylistener.__init__(self)
        
        #TODO: These values are just for testing. 
        self.x = 74
        self.y = 74
        
        self.max_speed = 256;
        
        self.key_inputs = {'up': False, 
                           'right': False,
                           'down': False, 
                           'left': False,  
                           'atk': False}
        
        self.knife = weapons.Knife()
        
        self.lock_face = False
        self.walking = False
        self.swinging = False
        self.holding = False
        self.invulnerable = False
    
        self.anim_timer = 0
        self.hit_invuln_duration = 256
    
    #What I eventually want: Load a sprite sheet, have a whole structure for getting sprites and picking frames and animation
    #and all that jazz.
    #Uhh, sprites. So. I have 
    #1. Different sprites for different states, such as walking, standing still, or swinging a sword. 
    #2. Different sprites that form the frames of an animation.
    #Each frame, I'll return exactly 1 of these sprites. Which one, however, is a bit complicated.
    
    def loadSprites(self):
        
        spritesheet = loadImage("Cricketbigsheet_reduced.bmp")
        
        self.sprites["not_walking"] = {}
        self.sprites["not_walking"][Character.Direction.UP] = getSpritesheetSprite(0, 2, spritesheet)
        self.sprites["not_walking"][Character.Direction.RIGHT] = getSpritesheetSprite(0, 1, spritesheet)
        self.sprites["not_walking"][Character.Direction.DOWN] = getSpritesheetSprite(0, 0, spritesheet)
        self.sprites["not_walking"][Character.Direction.LEFT] = getSpritesheetSprite(0, 3, spritesheet)
        
        #self.sprites["not_walking"][Character.Direction.UP] = pygame.Surface((64, 64))
        #self.sprites["not_walking"][Character.Direction.UP].blit(spritesheet, (0,0), (4, 140, 64, 64))   
        #self.sprites["not_walking"][Character.Direction.UP].set_colorkey(self.sprites["not_walking"][Character.Direction.UP].get_at((0,0)), RLEACCEL)
        
        #self.sprites["not_walking"][Character.Direction.RIGHT] = pygame.Surface((64, 64))
        #self.sprites["not_walking"][Character.Direction.RIGHT].blit(spritesheet, (0,0), (4, 72, 64, 64))   
        #self.sprites["not_walking"][Character.Direction.RIGHT].set_colorkey(self.sprites["not_walking"][Character.Direction.RIGHT].get_at((0,0)), RLEACCEL)
        
        #self.sprites["not_walking"][Character.Direction.DOWN] = pygame.Surface((64, 64))
        #self.sprites["not_walking"][Character.Direction.DOWN].blit(spritesheet, (0,0), (4, 4, 64, 64))   
        #self.sprites["not_walking"][Character.Direction.DOWN].set_colorkey(self.sprites["not_walking"][Character.Direction.DOWN].get_at((0,0)), RLEACCEL)
        
        #self.sprites["not_walking"][Character.Direction.LEFT] = pygame.Surface((64, 64))
        #self.sprites["not_walking"][Character.Direction.LEFT].blit(spritesheet, (0,0), (4, 208, 64, 64))   
        #self.sprites["not_walking"][Character.Direction.LEFT].set_colorkey(self.sprites["not_walking"][Character.Direction.LEFT].get_at((0,0)), RLEACCEL)
        
        #TODO: Move these over from the sprite sheet
        self.sprites["not_walking"]["holding"] = {}
        self.sprites["not_walking"]["holding"][Character.Direction.UP] = loadImage('Cricket1bswing2.bmp')
        self.sprites["not_walking"]["holding"][Character.Direction.RIGHT] = loadImage('Cricket1rswing2.bmp')
        self.sprites["not_walking"]["holding"][Character.Direction.DOWN] = loadImage('Cricket1fswing2.bmp')
        self.sprites["not_walking"]["holding"][Character.Direction.LEFT] = loadImage('Cricket1lswing2.bmp')
        
        self.sprites["not_walking"]["swinging"] = {}
        self.sprites["not_walking"]["swinging"][Character.Direction.UP] = loadImage('Cricket1bswing1.bmp')
        self.sprites["not_walking"]["swinging"][Character.Direction.RIGHT] = loadImage('Cricket1rswing1.bmp')
        self.sprites["not_walking"]["swinging"][Character.Direction.DOWN] = loadImage('Cricket1fswing1.bmp')
        self.sprites["not_walking"]["swinging"][Character.Direction.LEFT] = loadImage('Cricket1lswing1.bmp')
        
        self.sprites["walking"] = {}
        self.sprites["walking"][Character.Direction.UP] = Animation([(loadImage('Cricket1b.bmp'), 128), 
                                                  (loadImage('Cricket1bwalkl.bmp'), 128), 
                                                  (loadImage('Cricket1b.bmp'), 128),
                                                  (loadImage('Cricket1bwalkr.bmp'), 128)])
        self.sprites["walking"][Character.Direction.RIGHT] = Animation([(loadImage('Cricket1r.bmp'), 128), 
                                                  (loadImage('Cricket1rwalkl.bmp'), 128), 
                                                  (loadImage('Cricket1r.bmp'), 128),
                                                  (loadImage('Cricket1rwalkr.bmp'), 128)])
        self.sprites["walking"][Character.Direction.DOWN] = Animation([(loadImage('Cricket1f.bmp'), 128), 
                                                  (loadImage('Cricket1fwalkl.bmp'), 128), 
                                                  (loadImage('Cricket1f.bmp'), 128),
                                                  (loadImage('Cricket1fwalkr.bmp'), 128)])
        self.sprites["walking"][Character.Direction.LEFT] = Animation([(loadImage('Cricket1l.bmp'), 128), 
                                                  (loadImage('Cricket1lwalkl.bmp'), 128), 
                                                  (loadImage('Cricket1l.bmp'), 128),
                                                  (loadImage('Cricket1lwalkr.bmp'), 128)])
        
        self.sprites["walking"]["holding"] = {}
        self.sprites["walking"]["holding"][Character.Direction.UP] = Animation([(getSpritesheetSprite(4, 2, spritesheet), 128), 
                                                  (getSpritesheetSprite(6, 2, spritesheet), 128), 
                                                  (getSpritesheetSprite(4, 2, spritesheet), 128),
                                                  (getSpritesheetSprite(5, 2, spritesheet), 128)])
        self.sprites["walking"]["holding"][Character.Direction.RIGHT] = Animation([(getSpritesheetSprite(4, 1, spritesheet), 128), 
                                                  (getSpritesheetSprite(6, 1, spritesheet), 128), 
                                                  (getSpritesheetSprite(4, 1, spritesheet), 128),
                                                  (getSpritesheetSprite(5, 1, spritesheet), 128)])
        self.sprites["walking"]["holding"][Character.Direction.DOWN] = Animation([(getSpritesheetSprite(4, 0, spritesheet), 128), 
                                                  (getSpritesheetSprite(6, 0, spritesheet), 128), 
                                                  (getSpritesheetSprite(4, 0, spritesheet), 128),
                                                  (getSpritesheetSprite(5, 0, spritesheet), 128)])
        self.sprites["walking"]["holding"][Character.Direction.LEFT] = Animation([(getSpritesheetSprite(4, 3, spritesheet), 128), 
                                                  (getSpritesheetSprite(6, 3, spritesheet), 128), 
                                                  (getSpritesheetSprite(4, 3, spritesheet), 128),
                                                  (getSpritesheetSprite(5, 3, spritesheet), 128)])
        
        
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
                
        if not self.key_inputs['left']:
            if self.key_inputs['right']:
                self.movement['h'] = 1
                if not self.lock_face: self.facing = Character.Direction.RIGHT
            else:
                self.movement['h'] = 0
                
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

            
        if self.key_inputs['up'] or self.key_inputs['right'] or self.key_inputs['down'] or self.key_inputs['left']:
            self.current_speed = self.max_speed
            self.walking = True
        else:
            self.current_speed = 0
            self.walking = False
            
        if self.key_inputs['atk']:
            self.knife.attack(self, self.facing)
            self.lock_face = True
        else:
            self.knife.endAttack()
            self.lock_face = False
            
        #TODO: "holding" state determination code needs to be made better.
        self.holding = self.key_inputs['atk']
        
        self.swinging = self.knife.isSlashing() 
        
        Character.makeMove(self, dt)
        
        
    def updateImage(self):
        if self.walking:
            if self.holding:
                self.image = self.sprites["walking"]["holding"][self.facing].getCurrentFrame()
            else:
                self.image = self.sprites["walking"][self.facing].getCurrentFrame() 
        else:
            if self.swinging:
                self.image = self.sprites["not_walking"]["swinging"][self.facing]
            elif self.holding:
                self.image = self.sprites["not_walking"]["holding"][self.facing]
            else:
                self.image = self.sprites["not_walking"][self.facing]
        self.knife.updateImage()
        
    def handleKey(self, event):
        Keylistener.handleKey(self, event)
        
        if event.type == (KEYDOWN):
            if event.key == K_UP:
                self.key_inputs['up'] = True
            elif event.key == K_RIGHT:
                self.key_inputs['right'] = True
            elif event.key == K_DOWN:
                self.key_inputs['down'] = True
            elif event.key == K_LEFT:
                self.key_inputs['left'] = True
            elif event.key == K_LSHIFT:
                self.key_inputs['atk'] = True
        if event.type == (KEYUP):
            if event.key == K_UP:
                self.key_inputs['up'] = False
            elif event.key == K_RIGHT:
                self.key_inputs['right'] = False
            elif event.key == K_DOWN:
                self.key_inputs['down'] = False
            elif event.key == K_LEFT:
                self.key_inputs['left'] = False
            elif event.key == K_LSHIFT:
                self.key_inputs['atk'] = False
        
    def onHit(self, enemy, damage):
        if not self.invulnerable:
            #TODO: I want a separate function to handle depleting hp, so I can check for death and so forth.
            self.current_hitpoints -= damage
            print "Ouch! ", self.current_hitpoints 
            #TODO: Set up invulnerability flashes or whatever.
            self.invulnerable = True
            Timer(self.hit_invuln_duration, self.endInvuln)
            #TODO: Hit knockback
            
    def endInvuln(self, timer):
        self.invulnerable = False