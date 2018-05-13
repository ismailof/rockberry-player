from kivy.lang import Builder
from kivy.logger import Logger
from kivy.uix.screenmanager import Screen
from kivy.properties import NumericProperty, ListProperty

from ..widgets.playbackarea import PlaybackArea
from ..widgets.historyview import HistoryView


class HistoryScreen(Screen):
    pass


Builder.load_string("""

<HistoryScreen>

    BoxLayout:
        spacing: 5

        PlaybackArea:
            size_hint_x: 0.4
            item: app.mm.current.item

            Label:
                text: 'History: %d tracks' % len(app.mm.history.historylist)
                size_hint_y: 0.3
                font_size: 20
                text_size: self.size
                halign: 'right'

            HoldButton:
                size_hint_y: 0.5
                text: 'Refresh'
                on_click: app.mm.history.refresh()


        HistoryView:
            id: tlview
            historylist: app.mm.history.historylist
            dial_axis: 'y'
""")
