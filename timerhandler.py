import pdb

import pygame
from pygame.locals import *

#Main calls this every frame.
timers = []
def updateTimers(dt):
    for timer in timers:
        timer.update(dt)
 
#Timers get an Update method. It will add dt to an elapsed time counter, then check that against the timer length.
#If the one is greater than the other, they'll fire. 
#Waits for 'duration' milliseconds after creation, then calls 'callback' with itself as an argument. If 'should_repeat' is true, it will
#immediately reset itself upon firing.
class Timer:
    
    #Duration is in milliseconds
    def __init__(self, duration, callback, should_repeat = False):
        self.callback = callback
        self.should_repeat = should_repeat
        self.elapsed_time = 0
        self.duration = duration
        
        timers.append(self)
        
        self.dead = False
        self.paused = False
        
    def reset(self, new_duration = None):
        if not new_duration is None:
            self.duration = new_duration
        self.elapsed_time = 0
        self.dead = False
        if not self in timers:
            timers.append(self)
        
    def getRemainingTime(self):
        return self.duration - self.elapsed_time
        
    def trigger(self):
        self.callback(self)
        if(self.should_repeat):
            self.elapsed_time = 0
        else:
            self.dead = True
            timers.remove(self) #TODO: Do I want this for sure? It would probably be better to make timers reusable. 
            
    def update(self, dt):
        if self.dead:
            print "ERROR: Dead timer still running. ID ", self.timer_id
            return
        if self.paused:
            return
        
        self.elapsed_time += dt
        if self.elapsed_time >= self.duration:
            self.trigger()
        
    def pause(self):
        '''Pause the timer until unpause is called.'''
        self.paused = True
            
    def unpause(self):
        '''Resume timer operation from a paused state.'''
        self.paused = False
            
#When this timer finishes, it restarts itself immediately.            
#class RepeatingTimer(Timer):
    #def __init__(self, duration, callback):
        #Timer.__init__(self, duration, callback)        
        
    #def trigger(self):
        #Timer.trigger(self)
        #self.elapsed_time = 0
        #pygame.time.set_timer(self.eventid, self.milliseconds)