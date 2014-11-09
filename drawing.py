from pygame.locals import *
from thread import *
import numpy as np
import pygame
import time
import sys
import event

class Game( object ):

    def __init__(self, event_dispatcher):
        self.event_dispatcher = event_dispatcher
        print "Game dispatcher: {0}".format(self.event_dispatcher)

        # Listen for Frequency events
        self.event_dispatcher.add_event_listener(
            event.MusicEvent.FREQUENCY, self.on_frequency_event
        )

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

    def on_frequency_event(self, event ):
        """
        Event handler for MusicEvents.FREQUENCY events
        """
        print "game recieved frequency value: " + str(event.data)


    def render( self ):
        pygame.display.update()
        return
