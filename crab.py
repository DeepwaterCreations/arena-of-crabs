import pygame
from pygame.locals import *
pygame.init()

from character import Character
from drawable import loadImage
from timerhandler import Timerlistener
from attackhandler import Attackable

class Crab(Character, Timerlistener, Attackable):
    
    def __init__(self):
        Character.__init__(self)
        Timerlistener.__init__(self)
        Attackable.__init__(self)
        
        self.x = 250
        self.y = 250
        self.facing = Character.Direction.UP
        
        spritesheet = loadImage("MonstersBeach.bmp");
        
        self.sprites[Character.Direction.UP] = pygame.Surface((64, 64))    
        self.sprites[Character.Direction.UP].blit(spritesheet, (0,0), (4, 4, 64, 64))   
        self.sprites[Character.Direction.UP].set_colorkey(self.sprites[Character.Direction.UP].get_at((0,0)), RLEACCEL)
        
        self.sprites[Character.Direction.RIGHT] = pygame.Surface((64, 64))    
        self.sprites[Character.Direction.RIGHT].blit(spritesheet, (0,0), (140, 4, 64, 64))   
        self.sprites[Character.Direction.RIGHT].set_colorkey(self.sprites[Character.Direction.RIGHT].get_at((0,0)), RLEACCEL)
        
        self.sprites[Character.Direction.DOWN] = pygame.Surface((64, 64))    
        self.sprites[Character.Direction.DOWN].blit(spritesheet, (0,0), (140, 72, 64, 64))   
        self.sprites[Character.Direction.DOWN].set_colorkey(self.sprites[Character.Direction.DOWN].get_at((0,0)), RLEACCEL)
        
        self.sprites[Character.Direction.LEFT] = pygame.Surface((64, 64))   
        self.sprites[Character.Direction.LEFT].blit(spritesheet, (0,0), (4, 72, 64, 64))   
        self.sprites[Character.Direction.LEFT].set_colorkey(self.sprites[Character.Direction.LEFT].get_at((0,0)), RLEACCEL)
        
    def handletimer(self, event):
        Timerlistener.handletimer(self, event)
        
        #Spin in a circle
        facingIndex = self.facing.value
        self.facing = Character.Direction((facingIndex % 4) + 1)
        
    def onWeaponHit(self, other):
        print "Ow!"
        #Get the direction from the location of other to the location of self
        #direction = {'x': other.x - self.x, 'y': other.y - self.y}
        #length = math.sqrt(math.pow(direction['x'], 2) + math.pow(direction['y']))
        #direction['x'] /= length
        #direction['y'] /= length
        
        #Move in that direction at a calculated speed (based on "traction" stat and attack power?)
        #Set a timer to stop the motion? Duration based on attack power?
    