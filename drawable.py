import os

import pygame
from pygame.locals import *

def loadImage(filename):
    filepath = os.path.join('images', filename)
    try:
        image = pygame.image.load(filepath)
    except pygame.error, message:
        print "ERROR: Couldn't load image at ", filepath
        raise SystemExit, message
    
    image = image.convert()
    colorkey = image.get_at((0,0))
    image.set_colorkey(colorkey, RLEACCEL)
    
    return image

def getSpritesheetSprite(x, y, spritesheet):
    '''Return a surface with image data from the sub-cell of the spritesheet at index x, y'''
    sprite_width = 64
    sprite_height = 64
    border_width = 4 #I'll leave these numbers hard-coded since I think all my sprite sheets are going to follow this same convention. 
    surface = pygame.Surface((sprite_width, sprite_height))
    
    surface.blit(spritesheet, (0,0), 
                 (border_width + (x * (sprite_width + border_width)), 
                  border_width + (y * (sprite_height + border_width)), 
                  sprite_width, 
                  sprite_height))
    surface.set_colorkey(surface.get_at((0,0)), RLEACCEL)
    return surface

class Drawable(pygame.sprite.Sprite):
    drawable_group = pygame.sprite.RenderUpdates()
    
    @staticmethod
    def drawAll(surface):
        for whatever in Drawable.drawable_group:
            if whatever.visible:
                whatever.updateImage()
        return Drawable.drawable_group.draw(surface)
        
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.visible = True;
        self.image = loadImage('no_image.bmp')
        Drawable.drawable_group.add(self)
        
    def updateImage(self):
        """Set the value of self.image to something appropriate."""
        pass
    
    def setVisible(self, visible):
        """Add or remove the sprite from the draw group"""
        if self.visible != visible:
            self.visible = visible
            if self.visible:
                Drawable.drawable_group.add(self)
            else:
                Drawable.drawable_group.remove(self)