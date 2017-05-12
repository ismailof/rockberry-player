from kivy.event import EventDispatcher


class MediaController(EventDispatcher):

    app = None
    interface = None
    mopidy = None

    @classmethod
    def set_interface(cls, interface):
        cls.interface = interface

    @classmethod
    def set_server(cls, mopidy):
        cls.mopidy = mopidy

    def refresh(self, *args, **kwargs):
        pass

    def reset(self, *args, **kwargs):
        pass

    def call_method(self, method, **parameters):
        if not self.mopidy:
            raise Exception('%r.call_method: Mopidy server is not set' %
                self.__class__.__name__)
        if not method:
            raise Exception('%r.call_method: No server method set' %
                self.__class__.__name__)

        return self.mopidy.core.send(method, **parameters)
