import pygame
from pygame.locals import *

attackableGroup = pygame.sprite.Group()

def makeAttack(weapon):
    targets = pygame.sprite.spritecollide(weapon, attackableGroup, False)
    for target in targets:
        target.onWeaponHit(weapon)
        
class Attackable:
    
    def __init__(self):
        attackableGroup.add(self)
        
    def onWeaponHit(self, weapon):
        print self, "Ow!"