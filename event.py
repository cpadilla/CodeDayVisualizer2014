
class Event( object ):
    """
    Generic event to use with EventDispatcher.
    """

    def __init__(self, event_type, data=None):
        """
        The constructor accepts an event type as string and a custom data
        """
        self._type = event_type
        self._data = data

    @property
    def type(self):
        """
        Returns the event type
        """
        return self._type

    @property
    def data(self):
        """
        Returns the data associated to the event
        """
        return self._data

class MusicEvent( Event ):
    TEMPO = "tempoEvent"
    FREQUENCY = "frequencyEvent"
    BEAT = "beatEvent"
    BASS = "bassEvent"
    MIDS = "midsEvent"
    HIGHS = "highsEvent"
    HIGHDROP = "highDropEvent"
    MIDSDROP = "midsDropEvent"
    BASSDROP = "bassDropEvent"
    KILLMEPLZ = "KillMePlz"

    data = 0

class EventDispatcher( object ):
    """
    Generic event dispatcher which listen and dispatch events
    """

    def __init__(self):
        print "event initialized"
        self._events = dict()

    def __del__(self):
        """
        Remove all listener references at destruction time
        """
        self._events = None

    def getEvents(self):
        return self._events

    def has_listener(self, event_type, listener):
        """
        Return true if listener is register to event_type
        """
        # Check for event type and for the listener
        if event_type in self._events.keys():
            return listener in self._events[ event_type ]
        else:
            return False

    def dispatch_event(self, event):
        """
        Dispatch an instance of Event class
        """
        # print "dispatching event... {0}".format(event.type)
        # Dispatch the event to all the associated listeners
        if event.type in self._events.keys():
            listeners = self._events[ event.type ]

            for listener in listeners:
                listener( event )

    def add_event_listener(self, event_type, listener):
        """
        Add an event listener for an event type
        """
        print "adding event listener..."
        # Add listener to the event type
        if not self.has_listener( event_type, listener ):
            print "added"
            listeners = self._events.get( event_type, [] )

            listeners.append( listener )

            self._events[ event_type ] = listeners

    def remove_event_listener(self, event_type, listener):
        """
        Remove event listener.
        """
        print "removing event listener"

        # Remove the listener from the event type
        if self.has_listener( event_type, listener ):
            listeners = self._events[ event_type ]

            if len( listeners ) == 1:
                # Only this listener remains so remove the key
                del self._events[ event_type ]

            else:
                # Update listeners chain
                listeners.remove( listener )

                self._events[ event_type ] = listeners



