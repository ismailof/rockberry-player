from kivy.lang import Builder
from kivy.properties import ListProperty, NumericProperty
from kivy.uix.recycleview import RecycleView


class RefListView(RecycleView):

    reflist = ListProperty()
    item_height = NumericProperty(56)

    def on_reflist(self, *args):
        self.data = [{'ref': ref,
                      'index': index}
                     for index, ref in enumerate(self.reflist)]
        self.scroll_to_index(0)

    # Scrolls the view to position item 'index' at top
    def scroll_to_index(self, index):
        if not self.data:
            return
        relative_pos = index / float(len(self.data)
                                     - self.height / self.item_height)
        self.scroll_y = min(1, max(0, 1 - relative_pos))


Builder.load_string("""
#:import RefListItem rockberry_player.widgets.reflistitem.RefListItem

<RefListView>:
    viewclass: 'RefListItem'
    bar_width: 20
    bar_margin: 2
    scroll_type: ['bars', 'content']
    RecycleBoxLayout:
        orientation: 'vertical'
        size_hint: (None, None)
        width: root.width - root.bar_width - root.bar_margin
        height: self.minimum_height
        default_size_hint: (None, None)
        default_size: (self.width, root.item_height)

""")