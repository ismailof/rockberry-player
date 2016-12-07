from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

from ..widgets.inputbar import InputBar
from ..widgets.playbackarea import PlaybackArea
from ..widgets.reflistview import RefListView
from ..widgets.holdbutton import HoldButton


class BrowseScreen(Screen):
    pass


Builder.load_string("""

<BrowseScreen>

    BoxLayout:
        orientation: 'vertical'
        spacing: 5

        #InputBar:
            #id: searchbar
            #title: 'Search'
            #opacity: 0.6

        BoxLayout:
            size_hint_y: None
            height: 45
            spacing: 5

            Button:
                text: 'Home'
                on_press: app.mm.browser.browse_home()
            Button:
                text: 'Back'
                on_press: app.mm.browser.browse_back()
            HoldButton:
                text: 'Refresh'
                holdtime: 1.5
                on_click: app.mm.browser.refresh()
                on_hold: app.mm.browser.server_refresh()
            Button:
                text: 'Playlists'
                on_press: app.mm.browser.browse_playlists()

        BoxLayout:
            spacing: 5

            PlaybackArea:
                size_hint_x: 0.4
                ref: app.mm.browser.browse_ref

                ToggleButton:
                    text: 'Mix'
                    size_hint_y: 0.3
                    state: 'down' if app.mm.queue.shuffle_mode else 'normal'
                    on_state: app.mm.queue.shuffle_mode = self.state == 'down'

                Button:
                    text: 'Add'
                    on_press: app.mm.add_to_tracklist(refs=app.mm.browser.reflist)
                    size_hint_y: 0.3

            RefListView:
                viewclass: 'RefListItem'
                item_height: 56
                reflist: app.mm.browser.reflist

""")
