import pygame
from pygame.locals import *
pygame.init()

import keyhandler

class Character(keyhandler.Keylistener):
    
    def __init__(self):
        keyhandler.Keylistener.__init__(self)
        
        self.x = 0
        self.y = 0
        self.speed = 100        
        
        self.sprite = ""
        
        self.key_inputs = {'up': 0, 'down': 0, 'left': 0, 'right': 0} #Really, Python? No boolean values? 
        
        
    #What I eventually want: Load a sprite sheet, have a whole structure for getting sprites and picking frames and animation
    #and all that jazz.
    def loadSprite(self, filepath):
        self.sprite = pygame.image.load(filepath).convert_alpha()
        
        
    def update(self, dt):
        if dt == 0:
            return
        
        #TODO: I want the currently held horizontal/vertical key to override a second key, so if I hold down two keys at once, I keep moving in the first direction.
        #When the first key is released, if the second is still being held down, immediately move in the other direction.
        if self.key_inputs['up']:
            self.y -= self.speed * (dt/1000.0)           
        if self.key_inputs['down']:
            self.y += self.speed * (dt/1000.0) 
            
        if self.key_inputs['left']:
            self.x -= self.speed * (dt/1000.0)
        elif self.key_inputs['right']:
            self.x += self.speed * (dt/1000.0) 
            
        
    #This will have to be moved into the Cricket-specific subclass later.
    def handleKey(self, event):
        keyhandler.Keylistener.handleKey(self, event)
        
        if event.type == (KEYDOWN):
            if event.key == K_UP:
                self.key_inputs['up'] = 1
            elif event.key == K_DOWN:
                self.key_inputs['down'] = 1
            elif event.key == K_LEFT:
                self.key_inputs['left'] = 1
            elif event.key == K_RIGHT:
                self.key_inputs['right'] = 1
        if event.type == (KEYUP):
            if event.key == K_UP:
                self.key_inputs['up'] = 0
            elif event.key == K_DOWN:
                self.key_inputs['down'] = 0
            elif event.key == K_LEFT:
                self.key_inputs['left'] = 0
            elif event.key == K_RIGHT:
                self.key_inputs['right'] = 0
        