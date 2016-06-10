from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout

from kivy.properties import AliasProperty

from music.refs import RefBehavior
from widgets.albumcover import AlbumCover
from widgets.mediaicon import MediaIcon


class BrowseListItem(RefBehavior, BoxLayout):

    def get_ref_action(self, *args):
        return 'play' if self.reftype == 'track' else 'browse'

    def get_default_image(self, *args):
        def_imgs = {None: 'transparent.png',
                    'directory': 'browse_folder.png',
                    'playlist': 'browse_pl.png',
                    'track': 'default_track.png',
                    'album': 'default_album.png',
                    'artist': 'browse_artist.png'}
        return def_imgs.get(self.reftype , def_imgs[None])

    action = AliasProperty(get_ref_action, None, bind=['reftype'])
    defaultimg = AliasProperty(get_default_image, None, bind=['reftype'])


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
            size: (22, 22)
            right: cover.right
            media: root.media

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
        on_press: app.mm.play_uris([root.uri]) if root.action == 'play' else app.mm.browse(root.ref)
""")