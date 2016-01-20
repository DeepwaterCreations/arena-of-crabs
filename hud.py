import pdb

import pygame
from pygame.locals import *

from drawable import Drawable, loadImage
from updatable import Updatable
from cricket import Cricket 
from spritesheet import SpriteSheet

class Hud(Drawable, Updatable):

    hud_elements = []

    def __init__(self, hud_space):
        Drawable.__init__(self, "Hud_BG")
        Updatable.__init__(self)

        self.rect = hud_space
        
        #Make a black box for the background
        self.background = pygame.Surface( (self.rect.width, self.rect.height) )
        self.background.fill( (0,0,0) )

        #Make a simple health bar
        health_bar_box = pygame.Rect(self.rect.width/2 + 64, 16, self.rect.width/2 - 128, 32)
        health_bar_box.x += self.rect.x
        health_bar_box.y += self.rect.y
        self.health_bar = HealthBar(health_bar_box) 

        #Make a kill counter
        kill_counter_box = pygame.Rect(16, 0, (32 * 6), 64)
        kill_counter_box.x += self.rect.x
        kill_counter_box.y += self.rect.y
        self.kill_counter = KillCounter(kill_counter_box)
    
    def updateImage(self):
        self.image = self.background

    #TODO: Make this suck less. Totally rough draft code.
    def registerListeners(self, cricket, crabspawner):
        cricket.addTakeDamageListener(self.health_bar)
        crabspawner.addCrabKilledListener(self.kill_counter)


class HudElement(Drawable, Updatable):

    def __init__(self):
        Drawable.__init__(self, "Hud_Elem")
        Updatable.__init__(self)

        Hud.hud_elements.append(self)

class HealthBar(HudElement):

    def __init__(self, rect):
        HudElement.__init__(self)

        self.rect = rect
        self.image = pygame.Surface((self.rect.width, self.rect.height))

        self.filled = 1.0 #Using decimal instead of percentage values.

    def updateImage(self):
        self.image.fill((255,0,0))
        green_bar = pygame.Rect(0, 0, self.rect.width * self.filled, self.rect.height)
        self.image.fill((0,255,0), green_bar) 

    def onCricketTakesDamage(self, current_hitpoints, max_hitpoints):
        #Poor man's typecast. I hear this is better than actually casting, because it 
        #behaves better for certain types that max_hitpoints might be (but let's face
        #it, won't ever actually.) Anyway, I have to do something, or it's integer
        #division and herp de derp.
        self.filled = current_hitpoints / (max_hitpoints * 1.0)

class KillCounter(HudElement):

    def __init__(self, rect):
        HudElement.__init__(self)

        self.count = 0
        self.rect = rect
        self.image = pygame.Surface((32 + 32 + (32 * 4), 64)) #Crab symbol, "x", four digits.

        self.number_sprites = []
        self.loadSprites()

    def loadSprites(self):
        spritesheet = SpriteSheet("letters_large.bmp", spritewidth = 32) 

        #Get a set of number sprites #TODO: Move this to a separate class?
        for i in range(0, 10):
            self.number_sprites.append(spritesheet.getSprite(i, 3))

        #Draw the part of the image that won't ever change
        crab_sprite = spritesheet.getSprite(0, 2)
        x_sprite = spritesheet.getSprite(23, 1)
        label_sprite = pygame.Surface((32 + 32, 64)) 
        label_sprite.blit(crab_sprite, (0,0))
        label_sprite.blit(x_sprite, (crab_sprite.get_width()+1, 0))
        self.image.blit(label_sprite, (0,0))

    def updateImage(self):
        self.image.fill((0,0,0), pygame.Rect((2*32+1), 0, (4*32), 64))
        self.image.blit(self.number_sprites[(self.count/1000)%10], (0+(2*32), 0))
        self.image.blit(self.number_sprites[(self.count/100)%10], ((1*32)+(2*32), 0))
        self.image.blit(self.number_sprites[(self.count/10)%10], ((2*32)+(2*32), 0))
        self.image.blit(self.number_sprites[self.count%10], ((3*32)+(2*32), 0))

    def onCrabKilled(self):
        self.count += 1
