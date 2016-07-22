from kivy.clock import Clock
from kivy.event import EventDispatcher
from kivy.properties import ListProperty, NumericProperty

from base import MediaController

from utils import scheduled, triggered


class QueueControl(MediaController):

    tracklist = ListProperty()
    queue_point = NumericProperty(0)

    def __init__(self, **kwargs):
        super(QueueControl, self).__init__(**kwargs)
        self.trigger_refresh = Clock.create_trigger(self._triggered_refresh, timeout=1)

    def refresh(self, *args):
        self.trigger_refresh()

    def _triggered_refresh(self, *args):
        if self.interface:
            self.interface.get_tl_tracks(on_result=self.update_tracklist)

    @scheduled
    def update_tracklist(self, tracklist, *args):
        self.tracklist = tracklist

    def shuffle(self, *args):
        self.interface.shuffle(start=self.queue_point)

    #def index(self, tlid=None, *args):
