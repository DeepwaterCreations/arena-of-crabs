import pygame
from pygame.locals import *
pygame.init()

import drawable
import character
import keyhandler

class Cricket(character.Character, keyhandler.Keylistener):
    
    def __init__(self):
        character.Character.__init__(self)
        keyhandler.Keylistener.__init__(self)
        
        self.speed = 200;
        
        self.key_inputs = {'up': 0, 'down': 0, 'left': 0, 'right': 0} #Really, Python? No boolean values? 
    
    
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
        self.sprites[character.Character.Direction.UP] = drawable.loadImage('Cricket1b.bmp')
        self.sprites[character.Character.Direction.DOWN] = drawable.loadImage('Cricket1f.bmp')
        self.sprites[character.Character.Direction.LEFT] = drawable.loadImage('Cricket1l.bmp')
        self.sprites[character.Character.Direction.RIGHT] = drawable.loadImage('Cricket1r.bmp')
        
        
    def update(self, dt):
        if dt == 0:
            return
        
        #TODO: I want the currently held horizontal/vertical key to override a second key, so if I hold down two keys at once, I keep moving in the first direction.
        #When the first key is released, if the second is still being held down, immediately move in the other direction.
        if self.key_inputs['up']:
            self.y -= self.speed * (dt/1000.0)
            self.facing = character.Character.Direction.UP
        if self.key_inputs['down']:
            self.y += self.speed * (dt/1000.0) 
            self.facing = character.Character.Direction.DOWN
            
        if self.key_inputs['left']:
            self.x -= self.speed * (dt/1000.0)
            self.facing = character.Character.Direction.LEFT
        elif self.key_inputs['right']:
            self.x += self.speed * (dt/1000.0)
            self.facing = character.Character.Direction.RIGHT
            
        
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
        