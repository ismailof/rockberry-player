from __future__ import absolute_import, print_function

from kivy.lang import Builder
from kivy.clock import mainthread
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ObjectProperty

from ..music.mixer import MixerControl
from ..widgets.seekslider import SeekSlider
from ..widgets.gpiowidgets import DialBehavior


class VolumeBar(DialBehavior, BoxLayout):

    text = StringProperty('')
    mixer = ObjectProperty(None, rebind=True)

    @mainthread
    def on_dial(self, value):
        self.ids['sld_volume'].manual_step(value)

    @mainthread
    def on_click(self):
        self.mixer.set_mute(not self.mixer.mute)


Builder.load_string("""
#:set default_atlas 'atlas:///usr/local/lib/python2.7/dist-packages/kivy/data/images/defaulttheme/'

<VolumeBar>:
    spacing: 5
    gpio_group: 'volume'
    disabled: root.mixer is None or root.mixer.disabled

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
        active: (root.mixer and root.mixer.mute) or False
        on_active: root.mixer.set_mute(args[1])

    SeekSlider:
        id: sld_volume
        range: (0, 100)
        cached_value: root.mixer and root.mixer.volume or 0
        on_seek: root.mixer.set_volume(args[1])
        value_track: True
        value_track_color: [0, 1, 1, 1]
        cursor_image: 'slider_knob.png'
        cursor_disabled_image: 'slider_knob.png'
""")
