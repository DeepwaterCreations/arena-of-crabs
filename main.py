import sys, pygame
from pygame.locals import *
pygame.init()

import character
import cricket
import crab
import keyhandler
import timerhandler

screensize = width, height = 640, 576

display = pygame.display.set_mode(screensize)

blue = 0, 0, 255

cricket = cricket.Cricket()
cricket.loadSprites()

testcrab = crab.Crab()

clock = pygame.time.Clock()

timerhandler.startTimer(timerhandler.TIMEREVENT, 1000)

while 1:
    clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE): 
            sys.exit()
        if((event.type == KEYDOWN) or (event.type == KEYUP)):
            keyhandler.handle(event)
        if event.type == timerhandler.TIMEREVENT:
            timerhandler.handle(event)
                
    cricket.update(clock.get_time())
				
    display.fill(blue)
    cricket.draw(display)
    testcrab.draw(display)
    pygame.display.flip()
		
