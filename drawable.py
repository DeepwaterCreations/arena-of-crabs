import pygame
from pygame.locals import *
pygame.init()

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
        

class Drawable:
    def __init__(self):
        pass
        
    def draw(self, surface):
        pass