import pdb

import pygame
from pygame.locals import *

from updatable import Updatable

class Animation(Updatable):
    
    def __init__(self, frames, style="looping"):
        """
        @param frames: A list of tuples, each containing an image and a duration
        in ms for that image to be displayed.   
        """
        Updatable.__init__(self)
        self.frames = frames
        self.position = 0
        self.length = 0
        for frame in frames:
            self.length += frame[1]
        self.style = style
            
    def update(self, dt):
        if self.style == "oneoff":
            self.position = min(self.position + dt, self.length -1)
        elif self.style == "looping":
            self.position = (self.position + dt) % self.length
        else:
            raise ValueError("Animation style '{}' isn't a thing: \n{}".format(self.style, self.frames))
        
    def getCurrentFrame(self):
        """Return the frame corresponding to the current position in the timeline."""
        check_elapsed = 0
        for i, frame in enumerate(self.frames):
            if i + 1 == len(self.frames) or check_elapsed <= self.position < check_elapsed + self.frames[i + 1][1]:
                return frame[0]
            check_elapsed += self.frames[i + 1][1]
    
    def reset(self):
        self.position = 0
