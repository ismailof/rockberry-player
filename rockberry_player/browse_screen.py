from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, NumericProperty, ListProperty

from widgets.inputbar import InputBar
from widgets.playbackarea import PlaybackArea
from widgets.browselistview import BrowseListView


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
                text: 'Start'
                on_press: app.mm.browse(None)
            Button:
                text: 'Refresh'
                on_press: app.mm.browse(app.mm.browse_item.ref)
            Button:
                text: 'Tune'
                on_press: app.mm.add_to_tracklist(refs=app.mm.browse_list, tunning=True)
            Button:
                text: 'Add'
                on_press: app.mm.add_to_tracklist(refs=app.mm.browse_list)

        BoxLayout:
            spacing: 5

            PlaybackArea:
                size_hint_x: 0.4
                item: app.mm.browse_item

            BrowseListView:
                reflist: app.mm.browse_list
""")
