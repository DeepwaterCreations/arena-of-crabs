import pygame
from pygame.locals import *
pygame.init()

class Character:
    
    def __init__(self):
        self.x = 0
        self.y = 0
        self.sprite = ""
        self.speed = 100