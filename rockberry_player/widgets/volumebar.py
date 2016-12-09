from __future__ import absolute_import, print_function

from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import BooleanProperty, StringProperty,\
    NumericProperty

from ..gpio.gpiodial import GpioDialBehavior
from ..utils import scheduled


class VolumeBar(GpioDialBehavior, BoxLayout):

    volume = NumericProperty(0)
    mute = BooleanProperty(False)

    def __init__(self, *args, **kwargs):
        super(VolumeBar, self).__init__(*args, **kwargs)
        self.register_event_type('on_volume_change')
        self.register_event_type('on_mute_change')

    @scheduled
    def on_rotate(self, value):
        self.ids['sld_volume'].manual_step(value * self.gpio_step)
        #self.ids['sld_volume'].value += value * self.gpio_step
        #self.dispatch('on_volume_change', self.volume)

    @scheduled
    def on_click(self):
        self.mute = not self.mute

    def on_volume_change(self, volume):
        pass

    def on_mute_change(self, mute):
        pass


Builder.load_string("""
#:set default_atlas 'atlas:///usr/local/lib/python2.7/dist-packages/kivy/data/images/defaulttheme/'

<VolumeBar>:
    spacing: 5

    CheckBox:
        id: chk_mute
        size_hint_x: 0.2
        background_checkbox_down: default_atlas + 'audio-volume-muted'
        background_checkbox_normal: default_atlas + 'audio-volume-high'
        active: root.mute
        on_active: root.dispatch('on_mute_change', args[1])

    SeekSlider:
        id: sld_volume
        range: (0, 100)
        cached_value: root.volume
        on_seek: root.dispatch('on_volume_change', args[1])

""")
