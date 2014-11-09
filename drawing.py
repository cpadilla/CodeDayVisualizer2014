from pygame.locals import *
from thread import *
import numpy as np
import pygame
import time
import sys

FPS = 30
fpsClock = pygame.time.Clock()
WHITE = (255, 255, 255)
DISPLAYSURF = pygame.display.set_mode((400, 300))
pygame.display.set_caption('Test Screen')
DISPLAYSURF.fill(WHITE)

catPic = []
for x in range(1, 21):
    temp = pygame.image.load('blip.png')
    catPic.append(temp)

catx = 10
caty = 10

def render():
    pygame.display.update()
    return
