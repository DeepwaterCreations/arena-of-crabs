import pygame
from pygame.locals import *
pygame.init()

keylisteners = []

def handle(event):
    for listener in keylisteners:
        if(listener.keyListening):
            listener.handleKey(event)

class Keylistener:
    
    def __init__(self):
        self.keyListening = 1;
        keylisteners.append(self)
    
    def handleKey(self, event):
        pass