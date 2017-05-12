from kivy.clock import mainthread
from kivy.properties import BoundedNumericProperty, \
    BooleanProperty, AliasProperty
from ..utils import delayed

from base import MediaController


class MixerControl(MediaController):

    volume = BoundedNumericProperty(50, min=0, max=100, allownone=True)
    mute = BooleanProperty(False, allownone=True)
    disabled = AliasProperty(
        lambda self: self.volume is None or self.mute is None,
        None,
        bind=['volume', 'mute']
    )

    def refresh(self, *args, **kwargs):
        self.interface.get_volume(on_result=self.update_volume)
        self.interface.get_mute(on_result=self.update_mute)

    @mainthread
    def update_volume(self, volume, *args, **kwargs):
        self.volume = volume

    @mainthread
    def update_mute(self, mute, *args, **kwargs):
        self.mute = mute

    @delayed(0.5)
    def set_volume(self, volume, *args):
        self.interface.set_volume(int(volume))

    def set_mute(self, mute, *args):
        self.interface.set_mute(mute)
