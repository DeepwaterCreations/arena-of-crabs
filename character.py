from enum import Enum

import pygame
from pygame.locals import *
pygame.init()

class Character:
    
    Direction = Enum("Direction", "UP DOWN LEFT RIGHT");
    
    def __init__(self):
        self.x = 0
        self.y = 0
        self.sprite = ""
        self.speed = 100
        self.facing = Character.Direction.DOWN