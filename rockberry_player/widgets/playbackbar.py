from __future__ import absolute_import, print_function

from kivy.lang import Builder
from kivy.properties import OptionProperty, ListProperty, NumericProperty
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image

from ..widgets.holdbutton import HoldButtonBehavior


playback_controls = ['play_pause', 'stop', 'next', 'prev']


class PlaybackButton(HoldButtonBehavior, Image):
    action = OptionProperty(None, options=playback_controls)
    aura_color = ListProperty([1, 1, 1, 0])
    aura_color_pressed = ListProperty([0.8, 0.0, 0.0, 1])
    aura_radius = NumericProperty(50)
    aura_width = NumericProperty(2)


class PlaybackBar(BoxLayout):

    controls = ListProperty()

    def on_controls(self, *args):
        self.clear_widgets()
        for item in self.controls:
            if isinstance(item, (int, float)):
                self.add_widget(Widget(size_hint_x=item))
            elif isinstance(item, basestring):
                self.add_widget(
                    PlaybackButton(action=item)
                )


Builder.load_string("""

<PlaybackButton>:
    allow_stretch: True
    source: 'playback_{}.png'.format(self.action)
    on_click: app.mm.state.dispatch('on_' + self.action)
    aura_radius: min(self.size) / 2 + self.aura_width
    color: (1,1,1,1) if root.state == 'normal' else self.aura_color_pressed

    canvas.before:
        Color:
            rgba: self.aura_color if root.state == 'normal' else self.aura_color_pressed
        Line:
            #circle: (self.center_x, self.center_y, self.aura_radius)
            rectangle: self.x, self.y, self.width, self.height
            width: self.aura_width

<PlaybackBar>
    playback_state: app.mm.state.playback_state

""")
