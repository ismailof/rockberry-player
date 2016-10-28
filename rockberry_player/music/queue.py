from kivy.clock import Clock
from kivy.event import EventDispatcher
from kivy.properties import ListProperty, NumericProperty, \
    BooleanProperty

from base import MediaController

from utils import scheduled


class QueueControl(MediaController):

    tracklist = ListProperty()
    queue_point = NumericProperty(0)
    shuffle_mode = BooleanProperty(True)

    def __init__(self, **kwargs):
        super(QueueControl, self).__init__(**kwargs)
        self.trigger_refresh = Clock.create_trigger(self._triggered_refresh, timeout=2)

    def refresh(self, *args):
        self.trigger_refresh()

    def reset(self, *args):
        self.set_tracklist(None)

    def _triggered_refresh(self, *args):
        if self.interface:
            self.interface.get_tl_tracks(on_result=self.set_tracklist)

    @scheduled
    def set_tracklist(self, tracklist, *args):
        self.tracklist = tracklist or []
        self.queue_point = 0

    def shuffle(self, *args):
        self.interface.shuffle(start=self.queue_point)

    def clear(self, *args):
        self.interface.clear()