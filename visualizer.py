from thread import *
from threading import Thread

import drawing
import streaming
import event

#####################
#       Main
#####################
def main():


    dispatcher = event.EventDispatcher()

    streamer = streaming.MusicStreamer( dispatcher )

    # start_new_thread(streaming.readMusic, ())
    music = Thread(target = streamer.readMusic, args = ())

    print "hello!"
    game = drawing.Game( dispatcher )

    print 0
    music.start()
    print 1
    game.render()
    print 2
    music.join()
    print "done!"

    print "Enter any key..."
    userinput = stdin.readline()

    return

if __name__ == "__main__":
    main()
