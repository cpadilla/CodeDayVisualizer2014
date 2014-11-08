from pygame.locals import *
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

catPic = pygame.image.load('blip.png')
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
    while data != '':
        stream.write(data)

        indata = np.array(wave.struct.unpack("%dh"%(len(data)/swidth), data))

        # take the fft and square each value
        fftData = abs(np.fft.rfft(indata))**2

        # print (fftData[1] / 100).radjust(20)
        nums = fftData[1] / 10000000000

        lin = "|"
        bar = ""
        for x in range(1, int(nums)):
            bar = bar + lin
        print bar
        #print '{0:20f}'.format(fftData[1]

        # catx = 10
        # caty = fftData[1] * .001
        # DISPLAYSURF.blit(catPic, (catx, caty))
	# pygame.display.update()
	# fpsClock.tick(FPS)


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
