from kivy.app import App
from kivy.event import EventDispatcher


class MediaController(EventDispatcher):

    app = None
    interface = None
    mopidy = None

    @classmethod
    def set_interface(cls, interface):
        cls.interface = interface

    def refresh(self, *args):
        pass