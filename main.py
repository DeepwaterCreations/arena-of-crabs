import sys, pygame
from pygame.locals import *
pygame.init()

import cricket
import keyhandler

screensize = width, height = 640, 576

display = pygame.display.set_mode(screensize)

blue = 0, 0, 255

cricket = cricket.Cricket()
cricket.loadSprite('Cricket1f.png')

clock = pygame.time.Clock()

while 1:
    clock.tick()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE): 
            sys.exit()
        if((event.type == KEYDOWN) or (event.type == KEYUP)):
            keyhandler.handle(event)
                
    cricket.update(clock.get_time())
				
    display.fill(blue)
    display.blit(cricket.sprite, (cricket.x, cricket.y))
    pygame.display.flip()
		
