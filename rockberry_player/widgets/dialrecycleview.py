from __future__ import division, absolute_import

from kivy.lang import Builder
from kivy.properties import NumericProperty, AliasProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior

from ..widgets.dialbehavior import DialBehavior
from ..utils import delayed


class DialSelectableLayout(LayoutSelectionBehavior, RecycleBoxLayout):
    pass


class DialRecycleView(DialBehavior, RecycleView):

    selected_id = NumericProperty(None, allowNone=True)
    item_height = NumericProperty(45)

    _last_sel_id = None

    def _get_reftop_id(self):
        return (1 - self.scroll_y) * (self.num_items - self.items_per_page)

    def _set_reftop_id(self, index_f):
        relative_pos = index_f / (self.num_items - self.items_per_page)
        self.scroll_y = min(1, max(0, 1 - relative_pos))

    num_items = AliasProperty(lambda self: len(self.data), None,
        bind=['data'])

    items_per_page = AliasProperty(lambda self: self.height / self.item_height, None,
        bind=['size'])

    reftop_id = AliasProperty(_get_reftop_id, _set_reftop_id,
        bind=['scroll_y', 'num_items', 'items_per_page'])

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
        self.selected_id = self.constraint(self.selected_id + dial_value,
                                               min=0, max=self.num_items - 1)

    @delayed(0.2)
    def apply_selection(self):
        self._apply_selection(self._last_sel_id, False)
        self._last_sel_id = self.selected_id
        self._apply_selection(self.selected_id, True)

    def _apply_selection(self, index, is_visible):
        if index is None:
            return
        node = self.view_adapter.get_visible_view(index)
        self.layout_manager.apply_selection(index, node, is_visible)

    def on_selected_id(self, instance, index):
        self.scroll_to_index(index)
        self.apply_selection()


class SelectableItem(RecycleDataViewBehavior, BoxLayout):
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableItem, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableItem, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        if is_selected:
            rv.selected_id = index


Builder.load_string("""

<DialRecycleView>:
    bar_width: 40
    bar_margin: 2
    scroll_type: ['bars', 'content']
    DialSelectableLayout:
        key_selection: 'touch'
        orientation: 'vertical'
        size_hint: (None, None)
        width: root.width - root.bar_width - root.bar_margin
        height: self.minimum_height
        default_size_hint: (None, None)
        default_size: (self.width, root.item_height)

<SelectableItem>:
    canvas:
        Color:
            rgba: (0.9, 0.8, 0.8, 0.9) if root.selected else (0,0,0,0)
        Line:
            width: 2
            rectangle: (self.x + 5, self.y, self.width - 10, self.height)

""")


if __name__ == '__main__':
    import kivy
    kivy.require('1.9.2')
    from kivy.base import runTouchApp

    class TestItem(SelectableItem):
        pass

    class TestRecycleView(DialRecycleView):
        pass

    Builder.load_string("""

    <TestItem>:
        Label:
            text: 'Item #%02d' % root.number

    <TestRecycleView>:
        dial_axis: 'y'
        viewclass: 'TestItem'
        data: [{'number': i} for i in range(0, 100)]

    """)

    runTouchApp(widget=TestRecycleView())
