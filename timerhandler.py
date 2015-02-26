import pygame
from pygame.locals import *
pygame.init()

#TODO: It may be that I want separate timer instances with separate listener lists.
timerlisteners = []

def handle(event):
    for listener in timerlisteners:
        if(listener.timerListening):
            listener.handletimer(event)

#TODO: Set this up so I can do more than a single timer.
TIMEREVENT = pygame.USEREVENT + 1;

def startTimer(eventid, milliseconds):
    pygame.time.set_timer(eventid, milliseconds)

class Timerlistener:
    
    def __init__(self):
        self.timerListening = True; #TODO: It should specify a set of timer event ids that it cares about?
        timerlisteners.append(self)
    
    def handletimer(self, event):
        pass