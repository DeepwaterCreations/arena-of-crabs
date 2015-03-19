import pdb

import sys, pygame
from pygame.locals import *
pygame.init()

from character import Character
from cricket import Cricket
from crab import Crab
import keyhandler
import timerhandler

screensize = width, height = 640, 576

display = pygame.display.set_mode(screensize)

blue = 0, 0, 255

cricket = Cricket()
cricket.loadSprites()

testcrab = Crab()

clock = pygame.time.Clock()

while 1:
    clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE): 
            sys.exit()
        if((event.type == KEYDOWN) or (event.type == KEYUP)):
            keyhandler.handle(event)
        
    
    dt = clock.get_time()
    timerhandler.updateTimers(dt)
    #TODO: List of things to update            
    cricket.update(dt)
    testcrab.update(dt)
				
    display.fill(blue)
    #TODO: List of things to draw
    cricket.draw(display)
    testcrab.draw(display)
    pygame.display.flip()
		
