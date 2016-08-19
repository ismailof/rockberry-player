from kivy.lang import Builder
from kivy.properties import ListProperty
from kivy.uix.recycleview import RecycleView


class BrowseListView(RecycleView):

    reflist = ListProperty()

    def on_reflist(self, *args):
        self.data = [{'ref': ref} for ref in self.reflist]



Builder.load_string("""
#:import BrowseListItem widgets.browselistitem.BrowseListItem

<BrowseListView>:
    viewclass: 'BrowseListItem'
    bar_width: 20
    bar_margin: 2
    scroll_type: ['bars', 'content']
    RecycleBoxLayout:
        default_size: None, dp(56)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'
""")