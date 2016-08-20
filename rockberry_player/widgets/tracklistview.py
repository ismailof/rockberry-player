from kivy.lang import Builder
from kivy.uix.recycleview import RecycleView
from kivy.properties import ListProperty, NumericProperty, AliasProperty


class TrackListView(RecycleView):

    tracklist = ListProperty()
    tlid = NumericProperty()

    def find_current_index(self):
        if not self.tlid:
            return None
        for index, tl_track in enumerate(self.tracklist):
            if tl_track['tlid'] == self.tlid:
                return index
        return None

    current_id = AliasProperty(find_current_index, None, bind=['tracklist', 'tlid'])

    def on_tracklist(self, *args):
        self.data = [{'item': tl_track['track'],
                      'tlid': tl_track['tlid'],
                      'current': tl_track['tlid'] == self.tlid
                     } for tl_track in self.tracklist]

    def on_current_id(self, *args):
        if self.current_id is None:
            return
        self.scroll_to_index(self.current_id - 1)

    # Scrolls the view to position item 'index' at top
    def scroll_to_index(self, index):
        if not self.tracklist:
            return
        relative_pos = index / float(len(self.tracklist)
                                     - self.height / 70.0)
        self.scroll_y = min(1, max(0, 1 - relative_pos))


Builder.load_string("""
#:import TrackListItem widgets.tracklistitem.TrackListItem

<TrackListView>:
    viewclass: 'TrackListItem'
    bar_width: 20
    bar_margin: 2
    scroll_type: ['bars', 'content']
    RecycleBoxLayout:
        default_size: None, dp(70)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'
""")
