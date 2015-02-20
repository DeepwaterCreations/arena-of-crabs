import pygame
from pygame.locals import *
pygame.init()

class Character:
    
    def __init__(self):
        self.x = 0
        self.y = 0
        self.speed = 100        
        
        self.sprite = ""
        
        self.key_inputs = {'up': 0, 'down': 0, 'left': 0, 'right': 0} #Really, Python? No boolean values? 
        
    #What I eventually want: Load a sprite sheet, have a whole structure for getting sprites and picking frames and animation
    #and all that jazz.
    def loadSprite(self, filepath):
        self.sprite = pygame.image.load(filepath).convert()
        
    def update(self, dt):
        if dt == 0:
            return
        
        if self.key_inputs['up']:
            self.y -= self.speed * (dt/1000.0)
            
        if self.key_inputs['down']:
            self.y += self.speed * (dt/1000.0) 
            
        if self.key_inputs['left']:
            self.x -= self.speed * (dt/1000.0)
            
        if self.key_inputs['right']:
            self.x += self.speed * (dt/1000.0)