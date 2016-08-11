from kivy.event import EventDispatcher
from kivy.properties import BoundedNumericProperty, BooleanProperty
from utils import scheduled

from base import MediaController


class MixerControl(MediaController):

    volume = BoundedNumericProperty(50, min=0, max=100)
    mute = BooleanProperty(False)

    def refresh(self, *args, **kwargs):
        if not self.interface:
            self.interface = self.mopidy.mixer

        self.interface.get_volume(on_result=self.update_volume)
        self.interface.get_mute(on_result=self.update_mute)

    @scheduled
    def update_volume(self, volume, *args, **kwargs):
        self.volume = volume

    @scheduled
    def update_mute(self, mute, *args, **kwargs):
        self.mute = mute or False

    def set_volume(self, volume, *args):
        self.interface.set_volume(int(volume))

    def set_mute(self, mute, *args):
        self.interface.set_mute(mute)
