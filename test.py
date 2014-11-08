import sys, pygame, time, random, pyaudio
from pygame.locals import *

pygame.init()

FPS = 30
fpsClock = pygame.time.Clock()
WHITE = (255, 255, 255)
DISPLAYSURF = pygame.display.set_mode((400, 300))
pygame.display.set_caption('Test Screen')
DISPLAYSURF.fill(WHITE)

catPic = pygame.image.load('cat.png')
catx = 10
caty = 10


while True:

	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()

		elif event.type == KEYDOWN:

			if event.key == K_UP:
				catx += 10
				DISPLAYSURF.blit(catPic, (catx, caty))

			elif event.key == K_DOWN:
				catx -= 10
				DISPLAYSURF.blit(catPic, (catx, caty))

			elif event.key == K_RIGHT:
				caty += 10
				DISPLAYSURF.blit(catPic, (catx, caty))

			elif event.key == K_LEFT:
				caty -= 10
				DISPLAYSURF.blit(catPic, (catx, caty))

	pygame.display.update()
	fpsClock.tick(FPS)

