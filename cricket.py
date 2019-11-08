import pdb
import math

import pygame
from pygame.locals import *

#import attackhandler
import weapons
import decoration
from drawable import Drawable
from spritesheet import SpriteSheet
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
        self.rect.x = 320
        self.rect.y = 320
        #
        
        self.walk_speed = 256;
        
        self.key_inputs = {'up': False, 
                           'right': False,
                           'down': False, 
                           'left': False,  
                           'atk': False}
        
        self.knife = weapons.Knife()
        
        self.lock_face = False
        self.swinging = False
        self.holding = False
        self.invulnerable = False
    
        self.anim_timer = 0
        self.hit_invuln_duration = 1024
        self.invuln_flash_frequency = 32

        self.take_damage_listeners = []
        self.cricket_death_listeners = []
    
    #What I eventually want: Load a sprite sheet, have a whole structure for getting sprites and picking frames and animation
    #and all that jazz.
    #Uhh, sprites. So. I have 
    #1. Different sprites for different states, such as walking, standing still, or swinging a sword. 
    #2. Different sprites that form the frames of an animation.
    #Each frame, I'll return exactly 1 of these sprites. Which one, however, is a bit complicated.
    
    def loadSprites(self):
        
        spritesheet = SpriteSheet("Cricketbigsheet_reduced.bmp", border = 4)
        
        self.sprites["not_walking"] = {}
        self.sprites["not_walking"][Character.Direction.UP] = spritesheet.getSprite(0, 2)
        self.sprites["not_walking"][Character.Direction.RIGHT] = spritesheet.getSprite(0, 1)
        self.sprites["not_walking"][Character.Direction.DOWN] = spritesheet.getSprite(0, 0)
        self.sprites["not_walking"][Character.Direction.LEFT] = spritesheet.getSprite(0, 3)
                
        self.sprites["not_walking"]["holding"] = {}
        self.sprites["not_walking"]["holding"][Character.Direction.UP] = spritesheet.getSprite(3, 4)
        self.sprites["not_walking"]["holding"][Character.Direction.RIGHT] = spritesheet.getSprite(1, 4)
        self.sprites["not_walking"]["holding"][Character.Direction.DOWN] = spritesheet.getSprite(0, 4)
        self.sprites["not_walking"]["holding"][Character.Direction.LEFT] = spritesheet.getSprite(2, 4)
        
        self.sprites["not_walking"]["swinging"] = {}
        self.sprites["not_walking"]["swinging"][Character.Direction.UP] = spritesheet.getSprite(3, 5)
        self.sprites["not_walking"]["swinging"][Character.Direction.RIGHT] = spritesheet.getSprite(1, 5)
        self.sprites["not_walking"]["swinging"][Character.Direction.DOWN] = spritesheet.getSprite(0, 5)
        self.sprites["not_walking"]["swinging"][Character.Direction.LEFT] = spritesheet.getSprite(2, 5)
        
        self.sprites["walking"] = {}
        self.sprites["walking"][Character.Direction.UP] = Animation([
                                                  (spritesheet.getSprite(0, 2), 128), 
                                                  (spritesheet.getSprite(2, 2), 128), 
                                                  (spritesheet.getSprite(0, 2), 128),
                                                  (spritesheet.getSprite(1, 2), 128)])
        self.sprites["walking"][Character.Direction.RIGHT] = Animation([
                                                  (spritesheet.getSprite(0, 1), 128), 
                                                  (spritesheet.getSprite(2, 1), 128), 
                                                  (spritesheet.getSprite(0, 1), 128),
                                                  (spritesheet.getSprite(1, 1), 128)])
        self.sprites["walking"][Character.Direction.DOWN] = Animation([
                                                  (spritesheet.getSprite(0, 0), 128), 
                                                  (spritesheet.getSprite(2, 0), 128), 
                                                  (spritesheet.getSprite(0, 0), 128),
                                                  (spritesheet.getSprite(1, 0), 128)])
        self.sprites["walking"][Character.Direction.LEFT] = Animation([
                                                  (spritesheet.getSprite(0, 3), 128), 
                                                  (spritesheet.getSprite(2, 3), 128), 
                                                  (spritesheet.getSprite(0, 3), 128),
                                                  (spritesheet.getSprite(1, 3), 128)])
        
        self.sprites["walking"]["holding"] = {}
        self.sprites["walking"]["holding"][Character.Direction.UP] = Animation([(spritesheet.getSprite(4, 2), 128), 
                                                  (spritesheet.getSprite(6, 2), 128), 
                                                  (spritesheet.getSprite(4, 2), 128),
                                                  (spritesheet.getSprite(5, 2), 128)])
        self.sprites["walking"]["holding"][Character.Direction.RIGHT] = Animation([(spritesheet.getSprite(4, 1), 128), 
                                                  (spritesheet.getSprite(6, 1), 128), 
                                                  (spritesheet.getSprite(4, 1), 128),
                                                  (spritesheet.getSprite(5, 1), 128)])
        self.sprites["walking"]["holding"][Character.Direction.DOWN] = Animation([(spritesheet.getSprite(4, 0), 128), 
                                                  (spritesheet.getSprite(6, 0), 128), 
                                                  (spritesheet.getSprite(4, 0), 128),
                                                  (spritesheet.getSprite(5, 0), 128)])
        self.sprites["walking"]["holding"][Character.Direction.LEFT] = Animation([(spritesheet.getSprite(4, 3), 128), 
                                                  (spritesheet.getSprite(6, 3), 128), 
                                                  (spritesheet.getSprite(4, 3), 128),
                                                  (spritesheet.getSprite(5, 3), 128)])
        
    def update(self, dt):
        if dt == 0:
            return      
        if self.current_hitpoints <= 0:
            return
            
        #Set the walking state
        self.setWalking(Character.Direction.UP, self.key_inputs['up'])
        self.setWalking(Character.Direction.RIGHT, self.key_inputs['right'])
        self.setWalking(Character.Direction.DOWN, self.key_inputs['down'])
        self.setWalking(Character.Direction.LEFT, self.key_inputs['left'])
        
        #Set the facing direction
        if not self.lock_face:
            if (not self.key_inputs['down']) and self.key_inputs['up']:
                self.facing = Character.Direction.UP
            if (not self.key_inputs['up']) and self.key_inputs['down']:
                self.facing = Character.Direction.DOWN
            if (not self.key_inputs['left']) and self.key_inputs['right']:
                self.facing = Character.Direction.RIGHT
            if (not self.key_inputs['right']) and self.key_inputs['left']:
                self.facing = Character.Direction.LEFT

        if self.key_inputs['atk']:
            self.knife.attack(self, self.facing)
            self.lock_face = True
        else:
            if self.knife.attacking:
                self.knife.endAttack()
            self.lock_face = False
            
        #TODO: "holding" state determination code needs to be made better.
        self.holding = self.key_inputs['atk']
        
        self.swinging = self.knife.isSlashing() 
        
        Character.makeMove(self, dt)
        
    def updateImage(self):
        if self.isWalking():
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
        if not self.invulnerable and self.current_hitpoints > 0:
            self.takeDamage(damage)
            print "Ouch! ", self.current_hitpoints 
            if self.current_hitpoints > 0:
                self.invulnerable = True
                self.setVisible(False)
                Timer(self.hit_invuln_duration, self.endInvuln)
                Timer(self.invuln_flash_frequency, self.invulnFlashTimer)
                self.addKnockbackVector((enemy.rect.x, enemy.rect.y), 640) #TODO: Figure out better values
            
    def takeDamage(self, damage_amount):
        self.current_hitpoints -= damage_amount

        #Call listeners - I need to find something more elegant/flexible than observer pattern eventually,
        #but for this project, I'm favoring quick-and-dirty. So I'll stick with it for now.
        #Also, let's cut it out with the "handler" interfaces or whatever that was.
        for listener in self.take_damage_listeners:
            #TODO: Can my listeners be passed-in functions, instead of objects with this one weird method?
            listener.onCricketTakesDamage(self.current_hitpoints, self.max_hitpoints)

        if self.current_hitpoints <= 0:
            self.die()

    def die(self):
        #Play an animation
        #Go to the Game Over screen (GUI listener)
        #Maybe create a corpse object and immediately remove Cricket to avoid lingering effects?
        # corpse = Corpse(self.rect)
        deathsheet = SpriteSheet("Cricket_death_large.bmp", use_transparency=False)
        death_animation = Animation([
            (deathsheet.getSprite(0, 0), 128),
            (deathsheet.getSprite(1, 0), 128),
            (deathsheet.getSprite(2, 0), 128),
            (deathsheet.getSprite(3, 0), 128),
            ], style="oneoff")
        corpse = decoration.OneOff(layer="Character", animation=death_animation)
        corpse.rect.x = self.rect.x
        corpse.rect.y = self.rect.y

        for listener in self.cricket_death_listeners:
            listener.onCricketDeath()
        self.setVisible(False)
        #FIXME: Sometimes Cricket stays visible?
        self.kill() #This just removes it from all sprite groups
        

    def addTakeDamageListener(self, listener):
        self.take_damage_listeners.append(listener)

    def addCricketDeathListener(self, listener):
        self.cricket_death_listeners.append(listener)
            
    def endInvuln(self, timer):
        self.invulnerable = False
        
    def invulnFlashTimer(self, timer):
        if self.invulnerable:
            self.setVisible(not self.isVisible())
            Timer(self.invuln_flash_frequency, self.invulnFlashTimer)
        else:
            self.setVisible(True)
