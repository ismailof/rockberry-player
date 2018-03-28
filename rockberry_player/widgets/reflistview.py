from kivy.lang import Builder
from kivy.properties import ListProperty, AliasProperty
from kivy.uix.boxlayout import BoxLayout

from ..widgets.dialrecycleview import DialRecycleView
from ..widgets.holdbutton import HoldButton
from ..widgets.albumcover import AlbumCover
from ..widgets.atlasicon import AtlasIcon

from ..music.refs import RefItem


class RefListItem(RefItem, BoxLayout):

    def get_ref_action(self, *args):
        return 'play' if self.reftype == 'track' else 'browse'

    action = AliasProperty(get_ref_action, None, bind=['reftype'])


class RefListView(DialRecycleView):

    reflist = ListProperty()

    def on_reflist(self, *args):
        self.data = [{'ref': ref,
                      'index': index}
                     for index, ref in enumerate(self.reflist)]
        self.nav_id = 0


Builder.load_string("""

<RefListView>:
    viewclass: 'RefListItem'
    item_height: 56

<RefListItem>:
    size_hint_y: None
    height: 70
    padding: 2
    spacing: 10

    RelativeLayout:
        size_hint_x: None
        width: cover.height

        AlbumCover:
            id: cover
            border_width: 1
            background: (0.3, 0.3, 0.3, 0.5)
            default: root.typeimg
            mipmap: True
            uri: root.uri

        AtlasIcon:
            atlas: 'media'
            item: root.media
            size: (22, 22)
            right: cover.right

    Label:
        text: root.title
        halign: 'left'
        valign: 'top'
        text_size: self.size
        font_size: 20
        bold: (root.reftype != 'track')

    HoldButton:
        size_hint_x: 0.2
        opacity: 0.7
        text: root.action
        holdtime: 2.5
        on_click: app.mm.play_uris(uris=[root.uri]) if root.action == 'play' else app.mm.browser.browse(root.ref)
        on_hold: app.mm.add_to_tracklist(refs=app.mm.browser.reflist, tune_id=root.index) if root.action == 'play' else app.mm.browser.browse(root.ref)

""")
