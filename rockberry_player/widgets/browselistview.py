from kivy.lang import Builder
from kivy.properties import ListProperty
from kivy.uix.recycleview import RecycleView

from widgets.browselistitem import BrowseListItem


class BrowseListView(RecycleView):
    pass


Builder.load_string("""
#:import BrowseListItem widgets.browselistitem.BrowseListItem

<BrowseListView>:
    viewclass: 'BrowseListItem'
    RecycleBoxLayout:
        default_size: None, dp(56)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'
""")