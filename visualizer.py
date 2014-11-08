from pygame.locals import *
from thread import *
import numpy as np
import pygame
import time
import pyaudio
import wave
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

def run():
    CHUNK = 1024
    print ("hello!")

    # use a Blackman window
    window = np.blackman(CHUNK)

    wf = wave.open('music.wav', 'rb')
    swidth = wf.getsampwidth()

    # instantiate PyAudio (1)
    p = pyaudio.PyAudio()

    # open stream (2)
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    # read data
    data = wf.readframes(CHUNK)

    # play stream (3)
    frame = 0
    while data != '':
        stream.write(data)

        indata = np.array(wave.struct.unpack("%dh"%(len(data)/swidth), data))

        # take the fft and square each value
        fftData = abs(np.fft.rfft(indata))**2

        # print (fftData[1] / 100).radjust(20)
        # print int(fftData[1])

        ''' lin = "|"
        bar = ""
        for x in range(1, int(nums)):
            bar = bar + lin
        print bar '''
        #print '{0:20f}'.format(fftData[1]

        DISPLAYSURF.fill(WHITE)
        for x in range(1,20):
            nums = fftData[x] / 10000000000
            catx = 10 * x
            caty = nums / 10
            if (frame == 5):
                print x
                DISPLAYSURF.blit(catPic[x], (catx, caty))
                pygame.display.update()
                fpsClock.tick(FPS)
                frame = 0
            else:
                frame = frame + 1


        # read some more data
        data = wf.readframes(CHUNK)

    # stop stream (4)
    stream.stop_stream()
    stream.close()

    # close PyAudio (5)
    p.terminate()
    return

pygame.init()

" class Game(object):"
# PyGame window vars

run()
