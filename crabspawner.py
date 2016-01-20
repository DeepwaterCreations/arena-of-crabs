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
        
        self.spawn_freq = 5000
    
        self.spawnTimer = Timer(self.spawn_freq, self.onSpawnTimer, should_repeat = True)

        self.crab_killed_listeners = []
    
    def spawnCrab(self):
        '''Create a new crab within the spawn_rect'''
        new_crab = Crab(self)
        x = random.randint(self.spawn_rect.left, (self.spawn_rect.right - new_crab.rect.width))
        y = random.randint(self.spawn_rect.top, (self.spawn_rect.bottom - new_crab.rect.height))
        new_crab.setLocation(x, y)
        self.crab_group.add(new_crab)
        
    def onSpawnTimer(self, timer):
        if len(self.crab_group.sprites()) < self.max_crabs:
            self.spawnCrab()   
        
    def crabKilledTrigger(self):
        '''Called by crabs when they die'''
        for listener in self.crab_killed_listeners:
            listener.onCrabKilled()

    def addCrabKilledListener(self, listener):
        self.crab_killed_listeners.append(listener)

