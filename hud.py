import pdb

import pygame
from pygame.locals import *

from drawable import Drawable
from updatable import Updatable

class Hud(Drawable, Updatable):

    hud_elements = []

    def __init__(self, hud_space, layer="Hud"):
        Drawable.__init__(self, layer)
        Updatable.__init__(self)

        self.rect = hud_space

    
    def draw(self):
        pass
