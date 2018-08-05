from kivy.clock import mainthread, triggered
from kivy.properties import ListProperty, NumericProperty, \
    BooleanProperty

from base import MediaController


class QueueControl(MediaController):

    tracklist = ListProperty()
    queue_point = NumericProperty(0)
    shuffle_mode = BooleanProperty(True)

    def reset(self, *args):
        self.set_tracklist(None)

    @triggered(2)
    def refresh(self, *args):
        if self.interface:
            self.interface.get_tl_tracks(on_result=self.set_tracklist)

    @mainthread
    def set_tracklist(self, tracklist, *args):
        self.tracklist = tracklist or []
        self.queue_point = 0

    def shuffle(self, *args):
        self.interface.shuffle(start=self.queue_point)

    def clear(self, *args):
        self.interface.clear()
