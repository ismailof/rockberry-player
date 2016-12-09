from __future__ import absolute_import, print_function

from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import BooleanProperty, StringProperty,\
    NumericProperty, ObjectProperty

from ..music.mixer import MixerControl
from ..gpio.gpiodial import GpioDialBehavior
from ..utils import scheduled


class VolumeBar(GpioDialBehavior, BoxLayout):

    text = StringProperty('')
    mixer = ObjectProperty(MixerControl(), rebind=True)

    @scheduled
    def on_rotate(self, value):
        self.ids['sld_volume'].manual_step(value * self.gpio_step)

    @scheduled
    def on_click(self):
        self.mixer.set_mute(not self.mixer.mute)


Builder.load_string("""
#:set default_atlas 'atlas:///usr/local/lib/python2.7/dist-packages/kivy/data/images/defaulttheme/'

<VolumeBar>:
    spacing: 5
    disabled: root.mixer.disabled

    Label:
        text: root.text
        halign: 'right'
        valign: 'center'
        fontsize: 10
        text_size: (self.width - 50, self.height)
        shorted: True

    CheckBox:
        id: chk_mute
        size_hint_x: 0.1
        background_checkbox_down: default_atlas + 'audio-volume-muted'
        background_checkbox_normal: default_atlas + 'audio-volume-high'
        active: root.mixer.mute or False
        on_active: root.mixer.set_mute(args[1])

    SeekSlider:
        id: sld_volume
        range: (0, 100)
        cached_value: root.mixer.volume or 0
        on_seek: root.mixer.set_volume(args[1])

""")
