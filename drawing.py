from pygame.locals import *
from thread import *
import numpy as np
import pygame
import time
import sys
import event
import skater
import scene

class Game( object ):

    skt = skater.Skater()
    scene = scene.Scene()

    board = []
    jumping = 0
    jumpvalue = 0
    treeshake = 0
    trunkshake = 0
    WHITE = (255, 255, 255)
    FPS = 30
    fpsClock = pygame.time.Clock()

    def __init__(self, event_dispatcher):
        self.event_dispatcher = event_dispatcher
        print "Game dispatcher: {0}".format(self.event_dispatcher)

        # Listen for Frequency events
        # BEAT = "beatEvent"
        # BASS = "bassEvent"
        # MIDS = "midsEvent"
        # HIGHS = "highsEvent"
        # HIGHDROP = "highDropEvent"
        # MIDSDROP = "midsDropEvent"
        # BASSDROP = "bassDropEvent"
        self.event_dispatcher.add_event_listener(
            event.MusicEvent.BEAT, self.on_event
        )
        self.event_dispatcher.add_event_listener(
            event.MusicEvent.BASS, self.on_event
        )
        self.event_dispatcher.add_event_listener(
            event.MusicEvent.MIDS, self.on_event
        )
        self.event_dispatcher.add_event_listener(
            event.MusicEvent.HIGHS, self.on_event
        )
        self.event_dispatcher.add_event_listener(
            event.MusicEvent.HIGHDROP, self.on_event
        )
        self.event_dispatcher.add_event_listener(
            event.MusicEvent.MIDSDROP, self.on_event
        )
        self.event_dispatcher.add_event_listener(
            event.MusicEvent.BASSDROP, self.on_event
        )

        jumping = 0

        self.DISPLAYSURF = pygame.display.set_mode((800, 400))
        pygame.display.set_caption('Test Screen')
        self.DISPLAYSURF.fill(self.WHITE)

# Skateboard
        for x in range(1, 3):
            temp = pygame.image.load('blip.png')
            self.board.append(temp)

        temp = pygame.image.load('board.png')
        self.board.append(temp)

# Scenery

# tree
        #for x in range(0, 2):
        self.scene.treetrunk = pygame.image.load('treetrunk.png')
        self.scene.treetrunkx = 30
        self.scene.treetrunky = 400 - 150
        self.scene.treehead = pygame.image.load('treehead.png')
        self.scene.treeheadx = 30 - 10
        self.scene.treeheady = 400 - 150 - 10

    def on_event(self, event ):
        """
        Event handler for MusicEvents events
        """
        # print "game recieved frequency value: " + str(event.data[1])
        # BEAT = "beatEvent"
        # BASS = "bassEvent"
        # MIDS = "midsEvent"
        # HIGHS = "highsEvent"
        # HIGHDROP = "highDropEvent"
        # MIDSDROP = "midsDropEvent"
        # BASSDROP = "bassDropEvent"
        if event.type == "highDropEvent":
            print "highDropEvent"
            self.treeshake = event.data
            jumping = 1
        if event.type == "midsDropEvent":
            print "midsDropEvent"
            self.trunkshake = event.data
        if event.type == "bassDropEvent":
            print "bassDropEvent"
            self.jumpvalue = event.data
        # self.caty = self.jumpvalue
        # print caty * 10
        # self.DISPLAYSURF.fill(self.WHITE)
        # self.DISPLAYSURF.blit(self.catPic[1], (self.catx, self.caty))
        # pygame.display.update()
        # self.fpsClock.tick(self.FPS)

    def update( self ):
        self.skt.boardy = self.jumpvalue * 2

        scope = []
        self.scene.treetrunky = self.trunkshake * 2
        self.scene.treetrunkx -= 0.5
        if self.scene.treetrunkx < -50:
            self.scene.treetrunkx = 800

        self.scene.treeheady = self.treeshake * 2
        self.scene.treeheadx -= 0.5
        if self.scene.treeheadx < -50:
            self.scene.treeheadx = 800

    def render( self ):
        print "in renderer"
        while (1==1):
            self.update()

            # this is super necessary
            # print "skate: {0} tree: {1} trunk: {2}".format(self.skt.boardy, self.scene.treeheady, self.scene.treetrunky)
            print self.skt.boardy

            # clear screen
            self.DISPLAYSURF.fill(self.WHITE)

            # scener
            # trees
            # print self.scene.treeheady
            # print self.scene.treetrunky
            self.DISPLAYSURF.blit(self.scene.treetrunk, (self.scene.treetrunkx, 400 - 150 - self.scene.treetrunky))
            self.DISPLAYSURF.blit(self.scene.treehead, (self.scene.treeheadx, 400 - 150 - 10 - self.scene.treeheady))

            # draw board
            self.DISPLAYSURF.blit(self.board[0], (self.skt.boardx - 20, 400 - 1.5 - self.skt.boardy))
            self.DISPLAYSURF.blit(self.board[1], (self.skt.boardx + 20, 400 - 1.5 - self.skt.boardy))
            self.DISPLAYSURF.blit(self.board[2], (self.skt.boardx - 30, 400 - 6.5 - self.skt.boardy))


            pygame.display.update()

        return
