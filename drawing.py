from pygame.locals import *
from thread import *
import random
import numpy as np
import pygame
import time
import sys
import event
import skater
import scene
import streaming

class Game( object ):

    skt = skater.Skater()
    sk8erJump = 0
    scene = [] # scene.Scene()

    board = []
    boardDelta = 4
    sktrheight = 10
    jumping = 0
    jumpvalue = 0
    treeshake = 0
    trunkshake = 0
    distBtwTrees = 120
    treeScrollSpd = 0.75
    gcount = 0
    gcountTHRESH = 100
    countdown = False
    TREES = 10
    WHITE = (255, 255, 255)
    FPS = 30
    fpsClock = pygame.time.Clock()
    YELLOW = (255, 200, 0)

    def __init__(self, event_dispatcher):
        self.event_dispatcher = event_dispatcher
        print "Game dispatcher: {0}".format(self.event_dispatcher)

        pygame.font.init()

        # Listen for Frequency events
        # BEAT = "beatEvent"
        # BASS = "bassEvent"
        # MIDS = "midsEvent"
        # HIGHS = "highsEvent"
        # HIGHDROP = "highDropEvent"
        # MIDSDROP = "midsDropEvent"
        # BASSDROP = "bassDropEvent"
        # KILLMEPLZ = "KillMePlz"
        self.event_dispatcher.add_event_listener(
            event.MusicEvent.KILLMEPLZ, self.on_event
        )
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
        for x in range(0, self.TREES):
            temp = scene.Scene()
            self.scene.append(temp)
            self.scene[x].treetrunk = pygame.image.load('treetrunk.png')
            self.scene[x].treetrunkx = 30 + x * self.distBtwTrees + random.randrange(1,100)
            self.scene[x].treetrunky = 400 - 150
            self.scene[x].treehead = pygame.image.load('treehead.png')
            self.scene[x].treeheadx = 60 + x * self.distBtwTrees + random.randrange(-5, 5)
            self.scene[x].treeheady = 400 - 150 - 10

    def raiseKillMePlzEvent(self, value):
        """
        Dispatch the frequency event
        """
        print "raising Kill Me Plz event"
        event.MusicEvent.data = value

        self.event_dispatcher.dispatch_event(
            event.MusicEvent( event.MusicEvent.KILLMEPLZ, self )
        )

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
        # KILLMEPLZ = "KillMePlz"
        if event.type == "midsEvent":
            # print event.type
            if self.countdown == False:
                self.gcount += 1
            else:
                self.gcount -= 1
                if self.gcount == 0:
                    self.countdown = False
        if event.type == "baseEvent":
            print "hellooooooooo!!!!!"
            self.sk8erJump = event.data
        if event.type == "highDropEvent":
            # print event.type
            self.treeshake = event.data
            jumping = 1
        if event.type == "midsDropEvent":
            # print event.type
            self.trunkshake = event.data
        if event.type == "bassDropEvent":
            # print event.type
            self.jumpvalue = event.data
        if event.type == "KillMePlz":
            quit()
        # self.caty = self.jumpvalue
        # print caty * 10
        # self.DISPLAYSURF.fill(self.WHITE)
        # self.DISPLAYSURF.blit(self.catPic[1], (self.catx, self.caty))
        # pygame.display.update()
        # self.fpsClock.tick(self.FPS)

    def update( self ):
        self.skt.boardy = self.jumpvalue * self.boardDelta

        # print ":o"
        # print self.jumpvalue
        # print streaming.MusicStreamer.BASSDROPTHRESH + 1

        # move the board
        if self.jumpvalue <= streaming.MusicStreamer.BASSDROPTHRESH + 1:
            print ":D"
            # ftext = pygame.font.Font.render(":D heloo!OO!O", True, 0, background=None)
            self.skt.boardy = 0 + self.sktrheight # Board wheels
        scope = []
        # move the trees
        for x in range(0, len(self.scene)):
            self.scene[x].treetrunky = self.trunkshake * 2
            self.scene[x].treetrunkx -= self.treeScrollSpd
            if self.scene[x].treetrunkx < -50 - x * self.distBtwTrees:
                self.scene[x].treetrunkx = 800

            self.scene[x].treeheady = self.treeshake * 2
            self.scene[x].treeheadx -= self.treeScrollSpd
            if self.scene[x].treeheadx < -50 - x * self.distBtwTrees:
                self.scene[x].treeheadx = 800


        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raiseKillMePlzEvent(111)
                    self.quit()
                    pygame.quit()
                    sys.exit()
                # check if key is pressed
                # if you use event.key here it will give you error at runtime
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.quit()
                        pygame.quit()
                        sys.exit()

    def render( self ):
        # print "in renderer"
        count = 0
        while (1==1):
            self.update()

            # this is super necessary
            # print "skate: {0} tree: {1} trunk: {2}".format(self.skt.boardy, self.scene.treeheady, self.scene.treetrunky)
            # print self.skt.boardy
            print self.sk8erJump

            # clear screen
            self.DISPLAYSURF.fill(self.YELLOW)

            # sk8er
            sk8er = pygame.image.load("sk8er.png")

            # scener
            # trees
            # print self.scene.treeheady
            # print self.scene.treetrunky
            BG = pygame.image.load("BG1.png")
            BG2 = pygame.image.load("BG2.png")
            BG3 = pygame.image.load("BG1.png")
            if self.gcount <= -800 * 2:
                self.gcount = 0
            # print "count: {0}".format(self.gcount)
            if self.gcount % self.gcountTHRESH == 0:
                # self.gcount += self.gcountTHRESH
                self.countdown = True

            count += 1


            self.DISPLAYSURF.blit(BG, (self.gcount,0))
            self.DISPLAYSURF.blit(BG2, (self.gcount+800,0))
            self.DISPLAYSURF.blit(BG3, (self.gcount+800+800,0))
            for x in range(0, len(self.scene)):
                self.DISPLAYSURF.blit(self.scene[x].treetrunk, (self.scene[x].treetrunkx + x * self.distBtwTrees, 400 - 150 - self.scene[x].treetrunky))
                self.DISPLAYSURF.blit(self.scene[x].treehead, (self.scene[x].treeheadx + x * self.distBtwTrees, 400 - 150 - self.sktrheight - self.scene[x].treeheady))
            # print self.scene.treetrunky
            

            # draw board
            self.DISPLAYSURF.blit(self.board[0], (self.skt.boardx - 20, 400 - 1.5 - self.skt.boardy))
            self.DISPLAYSURF.blit(self.board[1], (self.skt.boardx + 20, 400 - 1.5 - self.skt.boardy))
            self.DISPLAYSURF.blit(self.board[2], (self.skt.boardx - 30, 400 - 6.5 - self.skt.boardy))

            print self.sk8erJump

            self.DISPLAYSURF.blit(sk8er, (self.skt.boardx - 30, 400 - 6.5 - self.skt.boardy - 124 + self.sk8erJump * 6))


            pygame.display.update()

        return

    def quit( self ):
        print "OOOOOUUUUUUUHHHHH"
        self.raiseKillMePlzEvent(111)
        EXIT = 1
        self.stop()

    def stop(self):
        self._stop.set()
