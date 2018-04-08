from __future__ import division

import time as tm
from datetime import timedelta, datetime as dt

from kivy.lang import Builder
from kivy.clock import Clock
from kivy.properties import ListProperty, NumericProperty, \
    ObjectProperty, AliasProperty
from kivy.uix.boxlayout import BoxLayout

from ..widgets.dialrecycleview import DialRecycleView
from ..widgets.refitemimage import RefItemImage
from ..widgets.holdbutton import HoldButton

from ..music.refs import RefItem


def format_time_diff(time, now):   

    elapsed_secs = now - time
    if elapsed_secs < 60:
        return ('Ahora')
    if elapsed_secs < 3600:
        return ('Hace %d minutos' % round(elapsed_secs / 60))
    if elapsed_secs < 3600 * 6:
        return ('Hace %d horas' % round(elapsed_secs / 3600))

    dt_time = dt.fromtimestamp(time)
    dt_now = dt.fromtimestamp(now)
    
    if dt_time.date() == dt_now.date():
        return 'Hoy %s' % dt_time.strftime('%H:%M')    
    if dt_time.date() == dt_now.date() - timedelta(days=1):
        return 'Ayer %s' % dt_time.strftime('%H:%M')

    return dt_time.strftime('%d-%b %H:%M')


class HistoryItem(RefItem, BoxLayout):
    time = NumericProperty(0)
    now = NumericProperty(0)    

    def __init__(self, **kwargs):
        super(HistoryItem, self).__init__(**kwargs)
        self._refresh_event = Clock.schedule_interval(self._refresh_now, 30)
        Clock.schedule_once(self._refresh_now)
    
    time_str = AliasProperty(lambda self: format_time_diff(self.time, self.now),
        None, bind=['time', 'now'])

    def _refresh_now(self, *args):
        self.now = int(tm.time())
        if self.now - self.time > 2 * 24 * 3600:            
            self._refresh_event.cancel()


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
