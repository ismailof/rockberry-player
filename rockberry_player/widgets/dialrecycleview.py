from __future__ import division

from kivy.lang import Builder
from kivy.properties import NumericProperty, BoundedNumericProperty, \
    AliasProperty, BooleanProperty, ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleboxlayout import RecycleBoxLayout

from dialbehavior import DialBehavior


class DialRecycleView(DialBehavior, RecycleView):

    nav_id = NumericProperty(None, allownone=True)
    nav_border_color = ListProperty([0.9, 0.9, 0.9, 0.9])

    item_height = NumericProperty(45)

    def _get_reftop_id(self):
        if self.num_items < self.items_per_page:
            return 0.0
        return (1 - self.scroll_y) * (self.num_items - self.items_per_page)

    def _set_reftop_id(self, index_f):
        relative_pos = index_f / (self.num_items - self.items_per_page)
        self.scroll_y = min(1, max(0, 1 - relative_pos))

    def _constraint_nav_id(self):
        if not self.num_items:
            self.nav_id = None
            return

        if self.nav_id < 0:
            self.nav_id = 0
        elif self.nav_id >= self.num_items:
            self.nav_id = self.num_items - 1

    def _get_nav_border(self):
        if self.nav_id is None:
            return None
        return (self.x,
            self.top - (self.nav_id - self.reftop_id + 1) * self.item_height,
            self.width - self.bar_width - self.bar_margin,
            self.item_height)

    num_items = AliasProperty(lambda self: len(self.data), None,
        bind=['data'])

    items_per_page = AliasProperty(lambda self: self.height / self.item_height, None,
        bind=['size'])

    reftop_id = AliasProperty(_get_reftop_id, _set_reftop_id,
        bind=['scroll_y', 'num_items', 'items_per_page'])

    nav_border = AliasProperty(_get_nav_border, None,
       bind=['nav_id', 'reftop_id', 'item_height', 'pos', 'size'])

    # Scrolls the view to position item 'index' at top
    def scroll_to_index(self, index):
        if not self.data:
            return

        if self.reftop_id is None:
            self.reftop_id = index - 1
        elif index < self.reftop_id:
            self.reftop_id = index - 0.5
        elif index > self.reftop_id + self.items_per_page - 1.49:
            self.reftop_id = index - self.items_per_page + 1.5
        else:
            return

    def on_dial(self, dial_value):
        if self.nav_id is None:
            self.nav_id = 0
        else:
            self.nav_id += dial_value

    def on_num_items(self, instance, index):
        self._constraint_nav_id()

    def on_nav_id(self, instance, index):
        self._constraint_nav_id()
        self.scroll_to_index(self.nav_id)

    def on_touch_down(self, touch):
        super(DialRecycleView, self).on_touch_down(touch)

        if self.collide_point(*touch.pos):
            self.nav_id = int(self.reftop_id + (self.top - touch.y) / self.item_height)
            return True

        return False


Builder.load_string("""

<DialRecycleView>:
    canvas.before:
        Color:
            rgba: root.nav_border_color if root.nav_border else (0,0,0,0)
        Line:
            width: 2
            rectangle: root.nav_border or (0,0,0,0)

    bar_width: 40
    bar_margin: 2
    scroll_type: ['bars', 'content']
    RecycleBoxLayout:
        key_selection: 'touch'
        orientation: 'vertical'
        size_hint: (None, None)
        width: root.width - root.bar_width - root.bar_margin
        height: self.minimum_height
        default_size_hint: (None, None)
        default_size: (self.width, root.item_height)

""")


if __name__ == '__main__':
    import kivy
    kivy.require('1.9.2')
    from kivy.base import runTouchApp

    class TestItem(BoxLayout):
        number = NumericProperty(0)

    Builder.load_string("""

<TestItem>:
    Label:
        text: 'Item #%02d' % root.number

<DialRecycleView>:
    dial_axis: 'y'
    viewclass: 'TestItem'
    data: [{'number': i} for i in range(0, 100)]

    """)

    runTouchApp(widget=DialRecycleView())
