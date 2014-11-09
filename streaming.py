import numpy as np
import pyaudio
import wave
import sys
import event

class MusicStreamer( object ):

    def __init__(self, event_dispatcher):
        self.event_dispatcher = event_dispatcher
        print "Music dispatcher: {0}".format(self.event_dispatcher)

    def raiseFrequencyEvent(self, value):
        """
        Dispatch the frequency event
        """
        print "raising frequency event"
        event.MusicEvent.data = value

        self.event_dispatcher.dispatch_event(
            event.MusicEvent( event.MusicEvent.FREQUENCY, self )
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

        while data != '':
            stream.write(data)

            indata = np.array(wave.struct.unpack("%dh"%(len(data)/swidth), data))

            # take the fft and square each value

            fftData = np.abs(np.fft.rfft(indata))
            fftData = np.delete(fftData,len(fftData)-1)
            power = np.log10(np.abs(fftData))**2
            power = np.reshape(power,(8,CHUNK/8))
            matrix = np.int_(np.average(power,axis=1)/4)
            print(matrix)

            # raise an event (value)
            self.raiseFrequencyEvent(matrix)

            # read some more data
            data = wf.readframes(CHUNK)

        # stop stream (4)
        stream.stop_stream()
        stream.close()

        # close PyAudio (5)
        p.terminate()
        return

