import pdb

import pygame
from pygame.locals import *

class Animation:
    
    def __init__(self, frames):
        """
        @param frames: A list of tuples, each containing an image and a duration in ms for that image to be displayed.   
        """
        self.frames = frames
        self.position = 0
        self.length = 0
        for frame in frames:
            self.length += frame[1]
            
    def update(self, dt):
        self.position = (self.position + dt) % self.length
        
    def getCurrentFrame(self):
        """Return the frame corresponding to the current position in the timeline."""
        check_elapsed = 0
        for i, frame in enumerate(self.frames):
            if i + 1 == len(self.frames) or check_elapsed <= self.position < check_elapsed + self.frames[i + 1][1]:
                return frame[0]
            check_elapsed += self.frames[i + 1][1]
    
    def reset(self):
        self.position = 0