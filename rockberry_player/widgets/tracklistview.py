from kivy.lang import Builder
from kivy.properties import ListProperty, NumericProperty, AliasProperty

from ..widgets.reflistview import RefListView


class TrackListView(RefListView):

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
        self.scroll_to_current()

    def on_current_id(self, *args):
        self.scroll_to_current()

    def on_size(self, *args):
        self.scroll_to_current()

    def scroll_to_current(self):
        if self.current_id is not None:
            self.scroll_to_index(self.current_id - 1)


Builder.load_string("""
#:import TrackListItem rockberry_player.widgets.tracklistitem.TrackListItem

<TrackListView>:
    viewclass: 'TrackListItem'
    item_height: dp(70)

""")
