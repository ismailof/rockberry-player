from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout

from kivy.properties import AliasProperty

from music.refs import RefItem
from widgets.albumcover import AlbumCover
from widgets.mediaicon import MediaIcon


class BrowseListItem(RefItem, BoxLayout):

    def get_ref_action(self, *args):
        return 'play' if self.reftype == 'track' else 'browse'

    action = AliasProperty(get_ref_action, None, bind=['reftype'])


Builder.load_string("""

<BrowseListItem>
    size_hint_y: None
    height: 70
    padding: 5
    spacing: 10

    RelativeLayout:
        size_hint_x: None
        width: cover.height

        AlbumCover:
            id: cover
            border_width: 1
            background: (0.3, 0.3, 0.3, 0.5)
            default: app.IMG_FOLDER + root.defaultimg
            mipmap: True
            uri: root.uri

        MediaIcon:
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
        bold: True

    Button:
        size_hint_x: 0.2
        opacity: 0.7
        text: root.action
        on_press: app.mm.play_uris([root.uri]) if root.action == 'play' else app.mm.browser.browse(root.ref)
""")
