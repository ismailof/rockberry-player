from functools import partial

from kivy.clock import Clock
from kivy.event import EventDispatcher
from kivy.properties import ListProperty, NumericProperty, \
    BooleanProperty, ObjectProperty

from .base import MediaController
from .tracks import TrackItem
from ..utils import scheduled, delayed


class QueueControl(MediaController):

    tracklist = ListProperty()
    queue_point = NumericProperty(0)
    shuffle_mode = BooleanProperty(True)
    
    prev = ObjectProperty(TrackItem(), rebind=True)
    next = ObjectProperty(TrackItem(), rebind=True)
    eot = ObjectProperty(TrackItem(), rebind=True)

    def reset(self, *args):
        self.set_tracklist(None)
        for track_item in (self.prev, self.next, self.eot):
                track_item.reset()

    @delayed(2)
    def refresh(self, *args):
        if self.interface:
            self.interface.get_tl_tracks(on_result=self.set_tracklist)

    @scheduled
    def set_tracklist(self, tracklist, *args):
        self.tracklist = tracklist or []
        self.queue_point = 0
        if tracklist:
            self.refresh_context_info()

    def shuffle(self, *args):
        self.interface.shuffle(start=self.queue_point)

    def clear(self, *args):
        self.interface.clear()
        
    @delayed(1)
    def refresh_context_info(self, *args):
        self.interface.get_previous_tlid(
            on_result=partial(self.set_context_track, track_item=self.prev))
        self.interface.get_next_tlid(
            on_result=partial(self.set_context_track, track_item=self.next))
        self.interface.get_eot_tlid(
            on_result=partial(self.set_context_track, track_item=self.eot))
   
    @scheduled
    def set_context_track(self, tlid, track_item):
        if not tlid:
            track_item.set_tl_track(None)
            return

        track_item.set_tl_track(
            {'tlid': tlid,
             'track': next((tl_track.track
                               for track in self.tracklist 
                               if track.tlid == tlid),
                           None)
            })
