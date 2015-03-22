import pygame
from pygame.locals import *

def loadImage(filepath):
    try:
        image = pygame.image.load(filepath)
    except pygame.error, message:
        print "ERROR: Couldn't load image at ", filepath
        raise SystemExit, message
    
    image = image.convert()
    colorkey = image.get_at((0,0))
    image.set_colorkey(colorkey, RLEACCEL)
    
    return image
        

class Drawable():
    drawable_list = []
    
    @staticmethod
    def drawAll(surface):
        for whatever in Drawable.drawable_list:
            if whatever.visible:
                whatever.draw(surface)

    def __init__(self):
        self.visible = True;
        Drawable.drawable_list.append(self)
        
    def draw(self, surface):
        pass