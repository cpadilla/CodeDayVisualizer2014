import numpy as np
import pyaudio
import wave
import sys

class MusicStreamer( object ):

    def __init__(self, event_dispatcher):
        self.event_dispatcher = event_dispatcher

    def readMusic(self):
        CHUNK = 1024
        print "in this method!"
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

        while data != '':
            stream.write(data)

            indata = np.array(wave.struct.unpack("%dh"%(len(data)/swidth), data))

            # take the fft and square each value
            fftData = abs(np.fft.rfft(indata))**2
            nums = fftData[1] / 10000000000
            print '{0:20f}'.format(fftData[1])

            # read some more data
            data = wf.readframes(CHUNK)

        # stop stream (4)
        stream.stop_stream()
        stream.close()

        # close PyAudio (5)
        p.terminate()
        return
