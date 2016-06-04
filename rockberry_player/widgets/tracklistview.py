from kivy.properties import ListProperty, NumericProperty, AliasProperty
from kivy.uix.listview import ListView
from kivy.adapters.simplelistadapter import SimpleListAdapter

from widgets.tracklistitem import TrackListItem


class TrackListView(ListView):

    tracklist = ListProperty()
    tlid = NumericProperty()

    def find_current_index(self):
        if not self.tlid:
            return None
        for index, tl_track in enumerate(self.tracklist):
            if tl_track['tlid'] == self.tlid:
                return index

    current_id = AliasProperty(find_current_index, None, bind=['tracklist', 'tlid'])

    def __init__(self, **kwargs):
        super(TrackListView, self).__init__(**kwargs)
        self.adapter = SimpleListAdapter(data=[],
                                         args_converter=self.my_args_converter,
                                         cls=TrackListItem)

    def on_content(self, *args):
        if self.content:
            self.scroll = self.content.parent
            self.scroll.scroll_type = ['bars', 'content']
            self.scroll.bar_width = '20dp'

    def on_tracklist(self, *args):
        self.adapter.data = self.tracklist

    def on_current_id(self, *args):
        try:
            if len(self.tracklist > 5):
                self.scroll_to(max(self.current_id - 1, 0))
        except:
            pass

    def my_args_converter(self, row_index, item):
        track_items = {'tlid': item['tlid'],
                       'track': item['track'],
                       'current': row_index == self.current_id}
        return track_items
