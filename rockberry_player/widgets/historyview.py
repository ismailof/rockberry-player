from __future__ import division

import time as tm

from kivy.lang import Builder
from kivy.clock import Clock
from kivy.properties import ListProperty, NumericProperty, \
    ObjectProperty, AliasProperty
from kivy.uix.boxlayout import BoxLayout

from ..widgets.dialrecycleview import DialRecycleView
from ..widgets.refitemimage import RefItemImage
from ..widgets.holdbutton import HoldButton

from ..music.refs import RefItem
from ..utils import format_timestamp


class HistoryItem(RefItem, BoxLayout):
    time = NumericProperty(0)
    now = NumericProperty(0)

    def __init__(self, **kwargs):
        super(HistoryItem, self).__init__(**kwargs)
        self.bind(time=self._refresh_now)
        self._refresh_event = Clock.create_trigger(self._refresh_now, 
                                                   timeout=30, interval=True)
        Clock.schedule_once(self._refresh_now)

    time_str = AliasProperty(lambda self: format_timestamp(self.time, self.now),
        None, bind=['time', 'now'])

    def _refresh_now(self, *args):
        self.now = int(tm.time())
        if self.now - self.time > 2 * 24 * 3600:
            self._refresh_event.cancel()
        else:
            self._refresh_event()


class HistoryView(DialRecycleView):

    historylist = ListProperty()

    def on_historylist(self, *args):
        self.data = [{'ref': ref,
                      'time': int(time_ms / 1000)}
                     for time_ms, ref in self.historylist]
        self.nav_id = 0


Builder.load_string("""

<HistoryView>:
    viewclass: 'HistoryItem'
    item_height: 50

<HistoryItem>:
    size_hint_y: None
    height: 70
    padding: 2
    spacing: 10

    RefItemImage:
        ref: root.ref
        size_hint_x: None
        width: self.height
        iconsize: 22

    BoxLayout:
        orientation: 'vertical'
        Label:
            text: root.title
            halign: 'left'
            valign: 'top'
            text_size: self.size
            font_size: 18

        Label:
            text: root.time_str
            text_size: self.size
            halign: 'right'
            font_size: 16

    HoldButton:
        size_hint_x: 0.2
        opacity: 0.7
        text: 'play'
        on_click: app.mm.play_uris(uris=[root.uri])

""")
