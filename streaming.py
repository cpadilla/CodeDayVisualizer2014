import threading
import numpy as np
import pyaudio
import wave
import sys
import event

BASSTHRESH = 7 # 14 /4
MIDTHRESH = 14 /2
HIGHTHRESH = 14 /2
bass = [2,3,4,5]
mids = [6,7,8,9]
highs = [10,12,13,14]

class MusicStreamer( threading.Thread ):

    BASSDROPTHRESH = 4

    EXIT = 0

    def __init__(self, event_dispatcher):
        self.event_dispatcher = event_dispatcher
        # print "Music dispatcher: {0}".format(self.event_dispatcher)

        self.event_dispatcher.add_event_listener(
            event.MusicEvent.KILLMEPLZ, self.on_event
        )

        # print "adding kill me plz listener..."
        # self.event_dispatcher.add_event_listener(
        #     event.MusicEvent.KILLMEPLZ, self.readMusic
        # )
        # print "added!"

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
        # print "raising Bass frequency event"
        event.MusicEvent.data = value

        self.event_dispatcher.dispatch_event(
            event.MusicEvent( event.MusicEvent.BASS, self )
        )

    def raiseBassDropFrequencyEvent(self, value):
        """
        Dispatch the frequency event
        """
        # print "raising Bass Drop frequency event"
        event.MusicEvent.data = value

        self.event_dispatcher.dispatch_event(
            event.MusicEvent( event.MusicEvent.BASSDROP, self )
        )

    def raiseMidsFrequencyEvent(self, value):
        """
        Dispatch the frequency event
        """
        # print "raising Mids frequency event"
        event.MusicEvent.data = value

        self.event_dispatcher.dispatch_event(
            event.MusicEvent( event.MusicEvent.MIDS, self )
        )

    def raiseMidsDropFrequencyEvent(self, value):
        """
        Dispatch the frequency event
        """
        # print "raising Mids Drop frequency event"
        event.MusicEvent.data = value

        self.event_dispatcher.dispatch_event(
            event.MusicEvent( event.MusicEvent.MIDSDROP, self )
        )

    def raiseHighFrequencyEvent(self, value):
        """
        Dispatch the frequency event
        """
        # print "raising High frequency event"
        event.MusicEvent.data = value

        self.event_dispatcher.dispatch_event(
            event.MusicEvent( event.MusicEvent.HIGHS, self )
        )

    def raiseHighsDropFrequencyEvent(self, value):
        """
        Dispatch the frequency event
        """
        # print "raising Highs Drop frequency event"
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

    def on_event(self, event ):
        # KILLMEPLZ = "KillMePlz"
        print "hello!"
        if event.type == "KillMePlz":
            print "good bye!"

            self.stop()
            # stream.stop_stream()
            # stream.close()
            EXIT = 1

            # close PyAudio (5)
            # p.terminate()

    def readMusic(self ):
        CHUNK = 1024
        print "in this method!"

        # use a Blackman window
        window = np.blackman(CHUNK)
        wf = wave.open('music.wav', 'rb')
        swidth = wf.getsampwidth()

        # instantiate PyAudio (1)
        self.p = pyaudio.PyAudio()

    # open stream (2)
        self.stream = self.p.open(format=self.p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
    # read data
        data = wf.readframes(CHUNK)

        oldBass = []
        oldMids = []
        oldHighs = []
        matrixMean = []
        meanCounter = 0

        while data != '':

            self.stream.write(data)

            indata = np.array(wave.struct.unpack("%dh"%(len(data)/swidth), data))

            # take the fft and square each value

            fftData = np.abs(np.fft.rfft(indata))
            fftData = np.delete(fftData,len(fftData)-1)
            power = np.log10(np.abs(fftData))**2
            power = np.reshape(power,(16,CHUNK/16))
            matrix = np.int_(np.average(power,axis=1))
            # print(matrix)

            ### BASS Events ###
            if np.abs(oldBass - np.mean(matrix[bass])) > MusicStreamer.BASSDROPTHRESH:
                self.raiseBassDropFrequencyEvent(np.abs(oldBass - np.mean(matrix[bass])))

            oldBass = np.mean(matrix[bass])

            print ("B-B-B-Bassssss: " , np.mean(matrix[bass]))
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

            # if matrixMean == matrix
                # meanCounter += 1

            # matrixMean = matrix

            if meanCounter > 20:
                print "D:"
                self.raiseKillMePlzEvent(111)

            ### KILL EVENT ###
            if self.EXIT == 1:
                print "HNGGGGG"
                self.stream.stop_stream()
                self.stream.close()

                # close PyAudio (5)
                self.p.terminate()
                data = ''
                continue

            # read some more data
            data = wf.readframes(CHUNK)

        # stop stream (4)
        stream.stop_stream()
        stream.close()

        # close PyAudio (5)
        self.p.terminate()
        return

    def quit(self):
        print "OOOOOUUUUUUUHHHHH"
        EXIT = 1
        self.raiseKillMePlzEvent(111)
        self.stop()

    def stop(self):
        print "XP"
        # self._stop.set()
        # stop stream (4)
        self.stream.stop_stream()
        self.stream.close()

        # close PyAudio (5)
        self.p.terminate()
        return
