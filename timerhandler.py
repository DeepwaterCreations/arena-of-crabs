import pdb

import pygame
from pygame.locals import *

#Main currently catches events and sends them here, where the individual timers will sort out for themselves which event IDs they 
#care about.  
timers = []
def handle(event):
    for timer in timers:
        timer.handle(event)
      
#Generators, eh? Okay, I'll try it out.
#BIG ISSUE: Pygame only gives me 9 events between USEREVENT (24) and MAXEVENT (32)! That means I can have nine timers max at any moment.
#For non-timer events, I can use sub-attributes to maybe work things out. Timers, alas, don't appear to let me do this. (So StackExchange claims.)
#Obviously, this won't at all work with my current design. So um...? SDL?
def getEventID():
    eventID = pygame.USEREVENT 
    while(True):
        eventID += 1
        yield eventID
 
#Sets itself on creation. 
#listeners is a list of Timerlisteners.    
#milliseconds is the timer's duration.
class Timer:
    
    idGenerator = getEventID()
    
    def __init__(self, milliseconds, callback, shouldRepeat = False):
        self.callback = callback
        self.shouldRepeat = shouldRepeat
        timers.append(self)
        
        self.eventid = Timer.idGenerator.next()
        print "Registered ", self.eventid
        pygame.time.set_timer(self.eventid, milliseconds)
        
    def handle(self, event):
        if event.type != self.eventid:
            return False
                    
        self.callback(event)
        if(not self.shouldRepeat):
            pygame.time.set_timer(self.eventid, 0)
            
#When this timer finishes, it restarts itself immediately.            
#class RepeatingTimer(Timer):
    #def __init__(self, milliseconds, callback):
        #Timer.__init__(self, milliseconds, callback)
        #self.milliseconds = milliseconds
        
        
    #def handle(self, event):
        #if Timer.handle(self, event):
            #pygame.time.set_timer(self.eventid, self.milliseconds)