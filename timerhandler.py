import pygame
from pygame.locals import *

#Main currently catches events and sends them here, where the individual timers will sort out for themselves which event IDs they 
#care about.  
timers = []
def handle(event):
    for timer in timers:
        timer.handle(event)

#Generators, eh? Okay, I'll try it out.
def getEventID():
    eventID = pygame.USEREVENT
    while(True):
        eventID += 1
        yield eventID
 
#Sets itself on creation. 
#listeners is a list of Timerlisteners.    
#milliseconds is the timer's duration.
class Timer:
    def __init__(self, milliseconds, callback):
        #self.listeners = listeners
        self.callback = callback        
        timers.append(self)
        
        self.eventid = getEventID().next()
        pygame.time.set_timer(self.eventid, milliseconds)
        
    def handle(self, event):
        if event.type != self.eventid:
            return False
                    
        self.callback(event)
            
#When this timer finishes, it restarts itself immediately.            
class RepeatingTimer(Timer):
    def __init__(self, milliseconds, callback):
        Timer.__init__(self, milliseconds, callback)
        self.milliseconds = milliseconds
        
        
    def handle(self, event):
        if Timer.handle(self, event):
            pygame.time.set_timer(self.eventid, self.milliseconds)