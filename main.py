import pdb

import sys, pygame
from pygame.locals import *
pygame.init()

import entity
from hud import Hud
import character
from character import Character
from cricket import Cricket
from crab import Crab
import keyhandler
import timerhandler
from drawable import Drawable
from updatable import Updatable
from crabspawner import CrabSpawner
from background import Background

screensize = width, height = 640, 576

display = pygame.display.set_mode(screensize)

blue = 0, 0, 255

top_wall = entity.Wall(0, 0, width, 64)
bottom_wall = entity.Wall(0, height - 128, width, 64)
left_wall = entity.Wall(0, 64, 64, height - 128)
right_wall = entity.Wall(width - 64, 64, 64, height - 128)
corner_ur = entity.Wall(width - 128, 64, 64, 64)
corner_lr = entity.Wall(width - 128, height - 192, 64, 64)
corner_ul = entity.Wall(64, 64, 64, 64)
corner_ll = entity.Wall(64, height - 192, 64, 64)
background = Background()

cricket = Cricket()
cricket.loadSprites()

hud_space = Rect(0, bottom_wall.rect.bottom, width, height - left_wall.rect.height)
hud = Hud(hud_space)
hud.registerListeners(cricket)

crabzone = Rect(left_wall.rect.right + 64, top_wall.rect.bottom + 64, right_wall.rect.left - left_wall.rect.width - 128, bottom_wall.rect.top - top_wall.rect.height - 128)
crabspawner = CrabSpawner(crabzone)

clock = pygame.time.Clock()

#display.fill(blue)
pygame.display.flip()

while 1:
    clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE): 
            sys.exit()
        if((event.type == KEYDOWN) or (event.type == KEYUP)):
            keyhandler.handle(event)
        
    
    dt = clock.get_time()
    timerhandler.updateTimers(dt)
    Updatable.updateAll(dt)
    #for (collider, wall) in pygame.sprite.groupcollide(character.wall_colliders, entity.walls, False, False):
    #    collider.onWallCollision(wall)
    for enemy in pygame.sprite.spritecollide(cricket, character.enemies, False):
        enemy.onPlayerCollision(cricket)
    

    display.fill(blue)
    dirty_rects = Drawable.drawAll(display)
    pygame.display.update(dirty_rects) 
