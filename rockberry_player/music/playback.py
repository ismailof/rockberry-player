from __future__ import absolute_import

from kivy.app import App
from kivy.clock import Clock
from kivy.event import EventDispatcher
from kivy.properties import NumericProperty, OptionProperty, \
    AliasProperty, ObjectProperty, DictProperty, StringProperty

from .base import MediaController

from ..utils import scheduled


class PlaybackControl(MediaController):

    STATES = ['stopped', 'playing', 'paused']
    ACTIONS = ['play_pause', 'play', 'pause', 'stop', 'next', 'prev']

    playback_state = OptionProperty(STATES[0],
                                    options=STATES,
                                    errorvalue=STATES[0])

    stream_title = StringProperty('')

    time_position = NumericProperty(0)
    update_interval = NumericProperty(0.25)
    resolution = NumericProperty(0.001)

    def __init__(self, controls=None, **kwargs):
        for action in self.ACTIONS:
            self.register_event_type('on_' + action)
        super(PlaybackControl, self).__init__(**kwargs)

    def refresh(self, *args):
        self.interface.get_state(on_result=self.set_playback_state)
        self.interface.get_time_position(on_result=self.set_time_position)
        self.interface.get_stream_title(on_result=self.set_stream_title)

    def reset(self, *args):
        self.set_playback_state('stopped')
        self.set_time_position(0)
        self.set_stream_title(None)

    def tick_position(self, dt=0, *args):
        self.time_position = self.time_position + dt / float(self.resolution)

    def on_playback_state(self, *args):
        if self.playback_state == 'playing':
            Clock.schedule_interval(self.tick_position, self.update_interval)
        else:
            Clock.unschedule(self.tick_position)

    @scheduled
    def set_playback_state(self, state=None, new_state=None, **kwargs):
        self.playback_state = state or new_state

    @scheduled
    def set_stream_title(self, title, *args, **kwargs):
        self.stream_title = title or ''

    @scheduled
    def set_time_position(self, time_position, *args, **kwargs):
        Clock.unschedule(self.tick_position)
        self.time_position = time_position or 0
        self.on_playback_state()

    def seek(self, time_position, *args):
        self.interface.seek(int(time_position))

    # ACTION BUTTONS METHOD.
    # TODO: Erase all of these

    def on_play_pause(self):
        if self.playback_state == 'playing':
            self.on_pause()
        else:
            self.on_play()

    def on_play(self):
        if self.playback_state == 'paused':
            self.interface.resume()
        else:
            self.interface.play()

    def on_pause(self):
        self.interface.pause()

    def on_stop(self):
        self.interface.stop()

    def on_next(self):
        self.interface.next()

    def on_prev(self):
        self.interface.previous()
