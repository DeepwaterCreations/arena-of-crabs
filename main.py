import sys, pygame
from pygame.locals import *
pygame.init()

screensize = width, height = 640, 576

display = pygame.display.set_mode(screensize)

blue = 0, 0, 255

cricket = pygame.image.load('Cricket1f.bmp').convert()
cricket_location = x, y = width/2, height/2
cricket_speed = 10

while 1:
    for event in pygame.event.get():
		if event.type == pygame.QUIT: sys.exit()
		if event.type == (KEYDOWN):
			if event.key == K_UP:
				y -= cricket_speed
			elif event.key == K_DOWN:
				y += cricket_speed
			elif event.key == K_LEFT:
				x -= cricket_speed
			elif event.key == K_RIGHT:
				x += cricket_speed
			elif event.key == K_ESCAPE:
				sys.exit()
							
		display.fill(blue)
		display.blit(cricket, (x, y))
		pygame.display.flip()
		
