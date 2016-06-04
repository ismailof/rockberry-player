from kivy.clock import Clock
from kivy.event import EventDispatcher
from kivy.properties import NumericProperty, BooleanProperty

from utils import scheduled


class PlaybackState(EventDispatcher):
    
    time_position = NumericProperty(0, allowNone=True)
    playback_state = OptionProperty('stopped',
                                    options=['playing', 'paused', 'stopped'],
                                    errorvalue='stopped')
    
    update_interval = NumericProperty(0.25)
    resolution = NumericProperty(0.001)
    
    def tick_position(self, dt=0, *args):
        self.time_position = self.time_position + dt / float(self.resolution)

    def on_playback_state(self, *args):
        if self.playback_state == 'playing':
            Clock.schedule_interval(self.tick_position, self.update_interval)
        else:
            Clock.unschedule(self.tick_position)

    @scheduled
    def set_position(self, time_position):
        self.time_position = time_position