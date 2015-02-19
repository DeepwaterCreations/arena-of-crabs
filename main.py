import sys, pygame
from pygame.locals import *
pygame.init()

import character

screensize = width, height = 640, 576

display = pygame.display.set_mode(screensize)

blue = 0, 0, 255

cricket = character.Character()
cricket.loadSprite('Cricket1f.bmp')

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == (KEYDOWN):
			if event.key == K_UP:
				cricket.key_inputs['up'] = 1
			elif event.key == K_DOWN:
				cricket.key_inputs['down'] = 1
			elif event.key == K_LEFT:
				cricket.key_inputs['left'] = 1
			elif event.key == K_RIGHT:
				cricket.key_inputs['right'] = 1
			elif event.key == K_ESCAPE:
				sys.exit()
        if event.type == (KEYUP):
            if event.key == K_UP:
                cricket.key_inputs['up'] = 0
            elif event.key == K_DOWN:
                cricket.key_inputs['down'] = 0
            elif event.key == K_LEFT:
                cricket.key_inputs['left'] = 0
            elif event.key == K_RIGHT:
                cricket.key_inputs['right'] = 0
                
    cricket.update()
				
    display.fill(blue)
    display.blit(cricket.sprite, (cricket.x, cricket.y))
    pygame.display.flip()
		
