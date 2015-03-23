import pdb

import sys, pygame
from pygame.locals import *
pygame.init()

from character import Character
from cricket import Cricket
from crab import Crab
import keyhandler
import timerhandler
from drawable import Drawable

screensize = width, height = 640, 576

display = pygame.display.set_mode(screensize)

blue = 0, 0, 255

cricket = Cricket()
cricket.loadSprites()

testcrab = Crab()

update_list = []
update_list.append(cricket)
update_list.append(testcrab)

clock = pygame.time.Clock()

display.fill(blue)
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
    for thing_that_needs_updating in update_list:
        thing_that_needs_updating.update(dt)

    display.fill(blue)
    dirty_rects = Drawable.drawAll(display)
    pygame.display.update(dirty_rects) 
		
