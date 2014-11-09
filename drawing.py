from pygame.locals import *
from thread import *
import numpy as np
import pygame
import time
import sys
import event
import skater

class Game( object ):

    skt = skater.Skater()

    
    board = []
    jumping = 0
    jumpvalue = 0
    WHITE = (255, 255, 255)
    FPS = 30
    fpsClock = pygame.time.Clock()

    def __init__(self, event_dispatcher):
        self.event_dispatcher = event_dispatcher
        print "Game dispatcher: {0}".format(self.event_dispatcher)

        # Listen for Frequency events
        self.event_dispatcher.add_event_listener(
            event.MusicEvent.FREQUENCY, self.on_event
        )

        jumping = 0

        self.DISPLAYSURF = pygame.display.set_mode((800, 400))
        pygame.display.set_caption('Test Screen')
        self.DISPLAYSURF.fill(self.WHITE)

        for x in range(1, 3):
            temp = pygame.image.load('blip.png')
            self.board.append(temp)

        temp = pygame.image.load('board.png')
        self.board.append(temp)

    def on_event(self, event ):
        """
        Event handler for MusicEvents events
        """
        # print "game recieved frequency value: " + str(event.data[1])
        if event.type == "frequencyEvent":
            self.jumpvalue = event.data[1] - 4
            jumping = 1
        # self.caty = self.jumpvalue
        # print caty * 10
        # self.DISPLAYSURF.fill(self.WHITE)
        # self.DISPLAYSURF.blit(self.catPic[1], (self.catx, self.caty))
        # pygame.display.update()
        # self.fpsClock.tick(self.FPS)

    def update( self ):
        self.skt.boardy = self.jumpvalue * 2
        # for event in self.event_dispatcher.getEvents():
        #     if event == "frequencyEvent":
        #         self.caty = self.jumpvalue

    def render( self ):
        print "in renderer"
        while (1==1):
            self.update()

            # this is super necessary
            print self.skt.boardy

            # clear screen
            self.DISPLAYSURF.fill(self.WHITE)

            # draw board
            self.DISPLAYSURF.blit(self.board[0], (self.skt.boardx - 20, 400 - 10 - self.skt.boardy))
            self.DISPLAYSURF.blit(self.board[1], (self.skt.boardx + 20, 400 - 10 - self.skt.boardy))
            self.DISPLAYSURF.blit(self.board[2], (self.skt.boardx - 30, 400 - 15 - self.skt.boardy))

            pygame.display.update()

        return
