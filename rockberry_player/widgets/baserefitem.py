from kivy.lang import Builder
from kivy.properties import NumericProperty, BooleanProperty, AliasProperty
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout

from ..widgets.albumcover import AlbumCover
from ..widgets.atlasicon import AtlasIcon
from ..music.refs import RefItem


class RefItemImage(RefItem, RelativeLayout):
    iconsize = NumericProperty(32)


class BaseRefListItem(RefItem, BoxLayout):

    is_current = BooleanProperty(False)
    is_playing = BooleanProperty(False)
    is_paused = BooleanProperty(False)

    def get_ref_action(self, *args):
        return 'play' if self.reftype == 'track' else 'browse'

    def get_action_image(self, *args):
        if self.action == 'browse':
            return 'action_browse.png'
        if self.is_playing:
            return 'playing.zip'
        elif self.is_paused:
            return 'playback_pause.png'

        return 'playback_play.png'

    action = AliasProperty(get_ref_action, None, bind=['reftype'])
    action_imgsrc = AliasProperty(get_action_image, None,
        bind=['action', 'is_current', 'is_playing', 'is_paused'])


Builder.load_string("""

<BaseRefListItem>:
    canvas.before:
        Color:
            rgba: (0.4, 0.2, 0.2, 0.5) if root.is_current else (0,0,0,0)
        Rectangle:
            pos: self.pos
            size: self.size

    is_current: root.uri == app.mm.current.uri
    is_playing: root.is_current and app.mm.state.playback_state == 'playing'
    is_paused: root.is_current and app.mm.state.playback_state == 'paused'

<RefItemImage>:

    AlbumCover:
        id: cover
        uri: root.uri
        default: root.typeimg
        border_width: int(self.width / 100) + 1
        background: (0.3, 0.3, 0.3, 0.5)

    AtlasIcon:
        atlas: 'media'
        item: root.media
        mimpap: True
        size: (root.iconsize, root.iconsize)
        right: cover.border_rectangle[0] + cover.border_rectangle[2] - 2
        y: cover.border_rectangle[1] + 2


 """)