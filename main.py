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
from decoration import WallTorch 

screensize = width, height = 640, 576

display = pygame.display.set_mode(screensize)

blue = 0, 0, 255

#TODO: Load map elements from Tiled file (which can be json! Sweet, yeah?)
top_wall = entity.Wall(0, 0, width, 64)
bottom_wall = entity.Wall(0, height - 128, width, 64)
left_wall = entity.Wall(0, 64, 64, height - 128)
right_wall = entity.Wall(width - 64, 64, 64, height - 128)
corner_ur = entity.Wall(width - 128, 64, 64, 64)
corner_lr = entity.Wall(width - 128, height - 192, 64, 64)
corner_ul = entity.Wall(64, 64, 64, 64)
corner_ll = entity.Wall(64, height - 192, 64, 64)
background = Background()

walltorch_topleft = WallTorch(Character.Direction.UP)
walltorch_topleft.rect.x = 64 * 3
walltorch_topleft.rect.y = 0
walltorch_topright = WallTorch(Character.Direction.UP)
walltorch_topright.rect.x = 64 * 6
walltorch_topright.rect.y = 0
walltorch_righttop = WallTorch(Character.Direction.RIGHT)
walltorch_righttop.rect.x = 64 * 9
walltorch_righttop.rect.y = 64 * 2
walltorch_rightbottom = WallTorch(Character.Direction.RIGHT)
walltorch_rightbottom.rect.x = 64 * 9
walltorch_rightbottom.rect.y = 64 * 5
walltorch_bottomleft = WallTorch(Character.Direction.DOWN)
walltorch_bottomleft.rect.x = 64 * 3
walltorch_bottomleft.rect.y = 64 * 7
walltorch_bottomright = WallTorch(Character.Direction.DOWN)
walltorch_bottomright.rect.x = 64 * 6
walltorch_bottomright.rect.y = 64 * 7
walltorch_lefttop = WallTorch(Character.Direction.LEFT)
walltorch_lefttop.rect.x = 0
walltorch_lefttop.rect.y = 64 * 2
walltorch_leftbottom = WallTorch(Character.Direction.LEFT)
walltorch_leftbottom.rect.x = 0
walltorch_leftbottom.rect.y = 64 * 5

cricket = Cricket()
cricket.loadSprites()

crabzone = Rect(left_wall.rect.right + 64, top_wall.rect.bottom + 64, right_wall.rect.left - left_wall.rect.width - 128, bottom_wall.rect.top - top_wall.rect.height - 128)
crabspawner = CrabSpawner(crabzone)

hud_space = Rect(0, bottom_wall.rect.bottom, width, height - left_wall.rect.height)
hud = Hud(hud_space)
hud.registerListeners(cricket, crabspawner)

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
