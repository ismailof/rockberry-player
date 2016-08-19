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

    current_id = AliasProperty(find_current_index, None, bind=['tracklist', 'tlid'])

    def on_tracklist(self, *args):
        self.data = [{'item': tl_track['track'],
                      'tlid': tl_track['tlid'],
                      'current': False
                     } for tl_track in self.tracklist]

    #def on_current_id(self, *args):
        #try:
            #if len(self.tracklist) > 5:
                #self.scroll_to(max(self.current_id - 1, 0))
            #else:
                #self.scroll_to(0)
        #except:
            #pass


Builder.load_string("""
#:import TrackListItem widgets.tracklistitem.TrackListItem

<TrackListView>:
    viewclass: 'TrackListItem'
    RecycleBoxLayout:
        default_size: None, dp(70)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'
""")