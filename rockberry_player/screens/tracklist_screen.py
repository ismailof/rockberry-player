from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, NumericProperty, ListProperty

from widgets.inputbar import InputBar
from widgets.playbackarea import PlaybackArea
from widgets.tracklistview import TrackListView

from music.tracks import TrackUtils


class TracklistScreen(Screen):

    tracklist = ListProperty()
    tlid = NumericProperty(0)
    filter = StringProperty('')
    filtered_tracklist = ListProperty()

    def __init__(self, **kwargs):
        super(TracklistScreen, self).__init__(**kwargs)
        self.trigger_filter = Clock.create_trigger(self.do_filter, timeout=1.7)
        self.trigger_filter()

    def matches_filter(self, track, filter):
        filter_words = filter.lower().split(' ')
        track_words = TrackUtils.words_in_track(track)
        return all([any([track_word.startswith(filter_word)
                        for track_word in track_words])
                   for filter_word in filter_words])

    def filter_tracklist(self, *args):
        if len(self.filter) < 3:
            return self.tracklist

        return [tl_track for tl_track in self.tracklist
                if self.matches_filter(tl_track['track'], self.filter)]

    def on_tracklist(self, *args):
        self.do_filter()

    def on_filter(self, *args):
        self.trigger_filter()

    def do_filter(self, *args):
        #self.ids['tlview'].scroll_to(0)
        self.filtered_tracklist = self.filter_tracklist()


Builder.load_string("""

<TracklistScreen>

    filter: filterbar.text

    BoxLayout:
        orientation: 'vertical'
        spacing: 5

        InputBar:
            id: filterbar
            title: 'Filter'
            opacity: 0.6

        BoxLayout:
            spacing: 5

            PlaybackArea:
                size_hint_x: 0.4
                item: app.mm.current.item

            TrackListView:
                id: tlview
                tlid: root.tlid
                tracklist: root.filtered_tracklist
""")
