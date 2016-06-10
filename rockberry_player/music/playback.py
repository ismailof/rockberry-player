from kivy.app import App
from kivy.clock import Clock
from kivy.event import EventDispatcher
from kivy.properties import NumericProperty, OptionProperty, \
    AliasProperty, ObjectProperty, DictProperty

from utils import scheduled
from debug import debug_function


class PlaybackControl(EventDispatcher):

    _statelist = ['stopped', 'playing', 'paused']
    interface = ObjectProperty(basetype=callable)

    playback_state = OptionProperty(_statelist[0],
                                    options=_statelist,
                                    errorvalue=_statelist[0])

    playing = AliasProperty(lambda self: self.playback_state == 'playing',
                            None,
                            bind=['playback_state'])

    time_position = NumericProperty(0, allowNone=True)
    update_interval = NumericProperty(0.25)
    resolution = NumericProperty(0.001)

    def __init__(self, controls=None, **kwargs):
        self.register_event_type('on_play_pause')
        self.register_event_type('on_stop')
        self.register_event_type('on_next')
        self.register_event_type('on_prev')
        super(PlaybackControl, self).__init__(**kwargs)

    def tick_position(self, dt=0, *args):
        self.time_position = self.time_position + dt / float(self.resolution)

    def on_playing(self, *args):
        if self.playing:
            Clock.schedule_interval(self.tick_position, self.update_interval)
        else:
            Clock.unschedule(self.tick_position)
            
    def refresh(self, *args):
        self.interface.get_state(on_result=self.set_playback_state)
        self.interface.get_time_position(on_result=self.update_time_position)

    @scheduled
    def set_playback_state(self, state):
        self.playback_state = state

    @scheduled
    def update_time_position(self, time_position, *args, **kwargs):
        self.time_position = time_position

    @scheduled
    def reset_time_position(self, *args, **kwargs):
        self.time_position = 0

    def seek(self, time_position, *args):
        self.interface.seek(time_position)

    def on_play_pause(self):
        if self.playback_state == 'playing':
            self.interface.pause()
        elif self.playback_state == 'paused':
            self.interface.resume()
        else:
            self.interface.play()

    def on_next(self):
        self.interface.next()

    def on_prev(self):
        self.interface.previous()

    def on_stop(self):
        self.interface.stop()


class PlaybackStateAware(EventDispatcher):
    playback_state = PlaybackControl.playback_state
    baseparm = ObjectProperty('')
    parmlist = DictProperty({_state: '' for _state in PlaybackControl._statelist})
    stateparm = ObjectProperty('')

    def __init__(self, **kwargs):
        super(PlaybackStateAware, self).__init__(**kwargs)
        App.get_running_app().mm.state.bind(playback_state=self.update_state)

    def on_baseparm(self, *args):
        self.parmlist = {state: self.baseparm for state in PlaybackControl._statelist}
        self.on_playback_state()

    def update_state(self, instance, playback_state):
        self.playback_state = playback_state

    def on_playback_state(self, *args):
        self.stateparm = self.parmlist[self.playback_state] \
            if self.playback_state in self.parmlist \
                else self.baseparm