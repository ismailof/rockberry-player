from kivy.app import App
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

    def bind_event(self, method, events):
        if not self.mopidy:
            return

        if type(events) != list:
            events = [events]

        for event in events:
            self.mopidy.bind_event(event, method)