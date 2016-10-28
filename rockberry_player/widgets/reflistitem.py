from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout

from kivy.properties import AliasProperty, \
    NumericProperty, BooleanProperty

from music.refs import RefItem
from widgets.holdbutton import HoldButton, HoldButtonBehavior
from widgets.albumcover import AlbumCover
from widgets.atlasicon import AtlasIcon


class RefListItem(RefItem, HoldButtonBehavior, BoxLayout):

    index = NumericProperty()
    selected = BooleanProperty(False)

    def get_ref_action(self, *args):
        return 'play' if self.reftype == 'track' else 'browse'

    action = AliasProperty(get_ref_action, None, bind=['reftype'])


Builder.load_string("""

<RefListItem>
    size_hint_y: None
    height: 70
    padding: 2
    spacing: 10

    on_click: self.selected = not self.selected

    canvas.before:
        Color:
            rgba: (0.4, 0.2, 0.2, 0.5) if root.selected else (0,0,0,0)
        Rectangle:
            pos: self.pos
            size: self.size

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
        hold_secs: 1.5
        on_click: app.mm.play_uris(uris=[root.uri]) if root.action == 'play' else app.mm.browser.browse(root.ref)
        on_hold: app.mm.add_to_tracklist(refs=app.mm.browser.reflist, tune_id=root.index) if root.action == 'play' else app.mm.browser.browse(root.ref)

""")
