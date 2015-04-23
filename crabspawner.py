import random

import pygame
from pygame.locals import *

from crab import Crab
from timerhandler import Timer

class CrabSpawner:
    '''Currently: Keeps track of the number of crabs. If the number is below a maximum, new crabs will spawn at regular intervals'''
    
    def __init__(self, spawn_rect):
        self.spawn_rect = spawn_rect
        
        self.crab_group = pygame.sprite.Group()
        self.max_crabs = 3
        #self.current_crabs = 0
        
        self.spawn_freq = 5000
    
        self.spawnTimer = Timer(self.spawn_freq, self.onSpawnTimer, should_repeat = True)
    
    def spawnCrab(self):
        '''Create a new crab within the spawn_rect'''
        x = random.randint(self.spawn_rect.left, self.spawn_rect.right)
        y = random.randint(self.spawn_rect.top, self.spawn_rect.bottom)
        new_crab = Crab()
        new_crab.setLocation(x, y)
        new_crab.clamp_ip(self.spawn_rect)
        self.crab_group.add(new_crab)
        #self.current_crabs += 1 
        
    def onSpawnTimer(self, timer):
        if len(self.crab_group.sprites()) < self.max_crabs:
            self.spawnCrab()   
        