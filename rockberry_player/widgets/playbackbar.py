from __future__ import absolute_import, print_function

from kivy.lang import Builder
from kivy.properties import OptionProperty, ListProperty
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.behaviors.button import ButtonBehavior

from ..music.playback import PlaybackControl


playback_controls = ['play_pause', 'stop', 'next', 'prev']


class PlaybackButton(ButtonBehavior, Image):
    action = OptionProperty(None, options=playback_controls)


class PlaybackBar(PlaybackControl, BoxLayout):

    controls = ListProperty()

    def on_controls(self, *args):
        self.clear_widgets()
        for item in self.controls:
            if isinstance(item, (int, float)):
                self.add_widget(Widget(size_hint_x=item))
            elif isinstance(item, basestring):
                self.add_widget(PlaybackButton(action=item))


Builder.load_string("""

<PlaybackButton>:
    allow_stretch: True
    source: 'images/playback_%s.png' % self.action
    on_press: self.parent.dispatch('on_' + self.action)

<PlaybackBar>
    playback_state: app.mm.state.playback_state

""")
