import numpy as np
import pyaudio
import wave
import sys
import event

BASSTHRESH = 14
MIDTHRESH = 14
HIGHTHRESH = 14
bass = [2,3,4,5]
mids = [6,7,8,9]
highs = [10,12,13,14]

class MusicStreamer( object ):

    def __init__(self, event_dispatcher):
        self.event_dispatcher = event_dispatcher
        print "Music dispatcher: {0}".format(self.event_dispatcher)

    def raiseFrequencyEvent(self, value):
        """
        Dispatch the frequency event
        """
        # print "raising frequency event"
        event.MusicEvent.data = value

        self.event_dispatcher.dispatch_event(
            event.MusicEvent( event.MusicEvent.FREQUENCY, self )
        )

    def raiseBassFrequencyEvent(self, value):
        """
        Dispatch the frequency event
        """
        print "raising Bass frequency event"
        event.MusicEvent.data = value

        self.event_dispatcher.dispatch_event(
            event.MusicEvent( event.MusicEvent.BASS, self )
        )

    def raiseBassDropFrequencyEvent(self, value):
        """
        Dispatch the frequency event
        """
        print "raising Bass Drop frequency event"
        event.MusicEvent.data = value

        self.event_dispatcher.dispatch_event(
            event.MusicEvent( event.MusicEvent.BASSDROP, self )
        )

    def raiseMidsFrequencyEvent(self, value):
        """
        Dispatch the frequency event
        """
        print "raising Mids frequency event"
        event.MusicEvent.data = value

        self.event_dispatcher.dispatch_event(
            event.MusicEvent( event.MusicEvent.MIDS, self )
        )

    def raiseMidsDropFrequencyEvent(self, value):
        """
        Dispatch the frequency event
        """
        print "raising Mids Drop frequency event"
        event.MusicEvent.data = value

        self.event_dispatcher.dispatch_event(
            event.MusicEvent( event.MusicEvent.MIDSDROP, self )
        )

    def raiseHighFrequencyEvent(self, value):
        """
        Dispatch the frequency event
        """
        print "raising High frequency event"
        event.MusicEvent.data = value

        self.event_dispatcher.dispatch_event(
            event.MusicEvent( event.MusicEvent.HIGHS, self )
        )

    def raiseHighsDropFrequencyEvent(self, value):
        """
        Dispatch the frequency event
        """
        print "raising Highs Drop frequency event"
        event.MusicEvent.data = value

        self.event_dispatcher.dispatch_event(
            event.MusicEvent( event.MusicEvent.HIGHDROP, self )
        )

    def raiseKillMePlzEvent(self, value):
        """
        Dispatch the frequency event
        """
        print "raising Kill Me Plz event"
        event.MusicEvent.data = value

        self.event_dispatcher.dispatch_event(
            event.MusicEvent( event.MusicEvent.KILLMEPLZ, self )
        )

    def readMusic(self):
        CHUNK = 1024
        # print "in this method!"

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

        oldBass = []
        oldMids = []
        oldHighs = []
        matrixMean = 0
        meanCounter = 0

        while data != '':
            stream.write(data)

            indata = np.array(wave.struct.unpack("%dh"%(len(data)/swidth), data))

            # take the fft and square each value

            fftData = np.abs(np.fft.rfft(indata))
            fftData = np.delete(fftData,len(fftData)-1)
            power = np.log10(np.abs(fftData))**2
            power = np.reshape(power,(16,CHUNK/16))
            matrix = np.int_(np.average(power,axis=1))
            print(matrix)

            ### BASS Events ###
            if np.abs(oldBass - np.mean(matrix[bass])) > 4:
                self.raiseBassDropFrequencyEvent(np.abs(oldBass - np.mean(matrix[bass])))

            oldBass = np.mean(matrix[bass])

            if np.mean(matrix[bass]) > BASSTHRESH:
                self.raiseBassFrequencyEvent(np.mean(matrix[bass]))

            ### MIDS Events ###
            if np.abs(oldMids - np.mean(matrix[mids])) > 4:
                self.raiseMidsDropFrequencyEvent(np.abs(oldMids - np.mean(matrix[mids])))

            oldMids = np.mean(matrix[mids])

            if np.mean(matrix[mids]) > MIDTHRESH:
                self.raiseMidsFrequencyEvent(np.mean(matrix[mids]))

            ### HIGHS Events ###
            if np.abs(oldHighs - np.mean(matrix[highs])) > 4:
                self.raiseHighsDropFrequencyEvent(np.abs(oldHighs - np.mean(matrix[highs])))

            oldHighs = np.mean(matrix[highs])

            if np.mean(matrix[highs]) > HIGHTHRESH:
                self.raiseHighsDropFrequencyEvent(np.mean(matrix[highs]))

            ### KILL EVENT ###

            if matrixMean == matrix:
                meanCounter += 1

            matrixMean = matrix

            if meanCounter > 20:
                self.raiseKillMePlzEvent(111)

            # read some more data
            data = wf.readframes(CHUNK)

        # stop stream (4)
        stream.stop_stream()
        stream.close()

        # close PyAudio (5)
        p.terminate()
        return

