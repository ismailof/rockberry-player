from __future__ import absolute_import

from kivy.lang import Builder
from kivy.properties import OptionProperty, ListProperty, NumericProperty
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image

from ..music.playback import PlaybackControl
from ..widgets.imageholdbutton import ImageHoldButton


class PlaybackButton(ImageHoldButton):
    action = OptionProperty(PlaybackControl.ACTIONS[0],
                            options=PlaybackControl.ACTIONS)


class PlayButton(PlaybackButton):
    playback_state = OptionProperty(PlaybackControl.STATES[0],
                                    options=PlaybackControl.STATES)

    def on_playback_state(self, *args):
        if self.playback_state == 'playing':
            self.action = 'pause'
        else:
            self.action = 'play'

    def on_hold(self, *args):
        self.action = 'stop'

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
    source: 'playback_{}.png'.format(self.action)
    on_release: app.mm.state.dispatch('on_' + self.action)

<PlayButton>:
    playback_state: app.mm.state.playback_state

""")
