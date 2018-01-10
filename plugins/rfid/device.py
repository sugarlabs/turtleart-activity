import gobject


class RFIDDevice(gobject.GObject):
    """
    Ancestor class for every supported device.
    The main class for the device driver must be called "RFIDReader".
    """
    # signal "tag-read" has to be emitted when a tag has been read.
    # The handler must receive the ISO-11784 hex value of the tag.
    # signal "disconnected" has to be emitted when the device is
    # unplugged or an error has been detected.
    __gsignals__ = {
        'tag-read': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE,
                     (gobject.TYPE_STRING,)),
        'disconnected': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE,
                         (gobject.TYPE_STRING,))
    }

    def __init__(self):
        """
        Initializer. Subclasses must call this method.
        """
        self.__gobject_init__()

    def get_present(self):
        """
        This method must detect if the device is present, returning True if so,
        or False otherwise.
        """
        raise NotImplementedError

    def get_version(self):
        """
        Returns a descriptive text of the device.
        """
        raise NotImplementedError

    def do_connect(self):
        """
        Connects to the device.
        Must return True if successfull, False otherwise.
        """
        raise NotImplementedError

    def do_disconnect(self):
        """
        Disconnects from the device.
        """
        raise NotImplementedError

    def read_tag(self):
        """
        Returns the 64 bit data in hex format of the last read tag.
        """
        raise NotImplementedError

    def write_tag(self, hex_val):
        """
        Could be implemented if the device is capable of writing tags.
        Receives the hex value (according to ISO 11784) to be written.
        Returns True if successfull or False if something went wrong.
        """
