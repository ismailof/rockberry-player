from kivy.lang import Builder
from kivy.properties import ListProperty, NumericProperty
from kivy.uix.recycleview import RecycleView


class ItemListView(RecycleView):

    reflist = ListProperty()
    item_height = NumericProperty(56)

    def on_reflist(self, *args):
        self.data = [{'ref': ref} for ref in self.reflist]
        self.scroll_to_index(0)
        
    # Scrolls the view to position item 'index' at top
    def scroll_to_index(self, index):
        if not self.data:
            return
        relative_pos = index / float(len(self.data)
                                     - self.height / self.item_height)
        self.scroll_y = min(1, max(0, 1 - relative_pos))


Builder.load_string("""
#:import BrowseListItem widgets.browselistitem.BrowseListItem
            
<ItemListView>:
    viewclass: 'BrowseListItem'
    bar_width: 20
    bar_margin: 2
    scroll_type: ['bars', 'content']
    RecycleBoxLayout:
        default_size: None, root.item_height
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'
""")