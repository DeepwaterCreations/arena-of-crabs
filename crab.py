import pygame
from pygame.locals import *
pygame.init()

import character
import drawable
import timerhandler

class Crab(character.Character, timerhandler.Timerlistener):
    
    def __init__(self):
        character.Character.__init__(self)
        timerhandler.Timerlistener.__init__(self)
        self.x = 250
        self.y = 250
        self.facing = character.Character.Direction.UP
        
        spritesheet = drawable.loadImage("MonstersBeach.bmp");
        
        self.sprites[character.Character.Direction.UP] = pygame.Surface((64, 64))    
        self.sprites[character.Character.Direction.UP].blit(spritesheet, (0,0), (4, 4, 64, 64))   
        self.sprites[character.Character.Direction.UP].set_colorkey(self.sprites[character.Character.Direction.UP].get_at((0,0)), RLEACCEL)
        
        self.sprites[character.Character.Direction.RIGHT] = pygame.Surface((64, 64))    
        self.sprites[character.Character.Direction.RIGHT].blit(spritesheet, (0,0), (140, 4, 64, 64))   
        self.sprites[character.Character.Direction.RIGHT].set_colorkey(self.sprites[character.Character.Direction.RIGHT].get_at((0,0)), RLEACCEL)
        
        self.sprites[character.Character.Direction.DOWN] = pygame.Surface((64, 64))    
        self.sprites[character.Character.Direction.DOWN].blit(spritesheet, (0,0), (140, 72, 64, 64))   
        self.sprites[character.Character.Direction.DOWN].set_colorkey(self.sprites[character.Character.Direction.DOWN].get_at((0,0)), RLEACCEL)
        
        self.sprites[character.Character.Direction.LEFT] = pygame.Surface((64, 64))   
        self.sprites[character.Character.Direction.LEFT].blit(spritesheet, (0,0), (4, 72, 64, 64))   
        self.sprites[character.Character.Direction.LEFT].set_colorkey(self.sprites[character.Character.Direction.LEFT].get_at((0,0)), RLEACCEL)
        
    def handletimer(self, event):
        timerhandler.Timerlistener.handletimer(self, event)
        
        #Spin in a circle
        facingIndex = self.facing.value
        self.facing = character.Character.Direction((facingIndex % 4) + 1)