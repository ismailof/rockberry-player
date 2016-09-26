from kivy.lang import Builder
from kivy.event import EventDispatcher
from kivy.properties import OptionProperty, ListProperty
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

from music.playback import PlaybackControl, PlaybackStateAware


playback_controls = ['play_pause', 'stop', 'next', 'prev']


class PlaybackButton(PlaybackStateAware, Button):
    action = OptionProperty(None, options=playback_controls)

    def on_action(self, instance, action):
        if action == 'play_pause':
            self.baseparm = 'play'
            self.parmlist.playing = '||'
        elif action == 'stop':
            self.baseparm = 'stop'
        elif action == 'next':
            self.baseparm = '>>'
        elif action == 'prev':
            self.baseparm = '<<'

    def on_press(self, *args):
        self.parent.dispatch('on_' + self.action)


class PlaybackBar(PlaybackControl, BoxLayout):

    controls = ListProperty()

    def on_controls(self, *args):

        self.clear_widgets()
        for item in self.controls:
            if type(item) in (int, float):
                self.add_widget(Widget(size_hint_x=item))
            elif type(item) in (str, unicode):
                self.add_widget(PlaybackButton(action=item))
            else:
                # TODO: Aprender de una vez a lanzar excepciones!
                pass


Builder.load_string("""

<PlaybackButton>
    text: self.stateparm
    font_size: 24

<PlaybackBar>
    playback_state: app.mm.state.playback_state

""")
