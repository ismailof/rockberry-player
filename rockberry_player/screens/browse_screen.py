from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, NumericProperty, ListProperty

from widgets.inputbar import InputBar
from widgets.playbackarea import PlaybackArea
from widgets.itemlistview import ItemListView


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
            Button:
                text: 'Refresh'
                on_press: app.mm.browser.refresh()
            Button:
                text: 'Playlists'
                on_press: app.mm.browser.browse_playlists()

        BoxLayout:
            spacing: 5

            PlaybackArea:
                size_hint_x: 0.4
                ref: app.mm.browser.browse_ref

                Button:
                    text: 'Mix'
                    on_press: app.mm.add_to_tracklist(refs=app.mm.browser.reflist, tune_id=0, mixing=True)
                    size_hint_y: 0.3
                Button:
                    text: 'Add'
                    on_press: app.mm.add_to_tracklist(refs=app.mm.browser.reflist)
                    size_hint_y: 0.3

            ItemListView:
                viewclass: 'BrowseListItem'
                item_height: 56
                reflist: app.mm.browser.reflist

""")
