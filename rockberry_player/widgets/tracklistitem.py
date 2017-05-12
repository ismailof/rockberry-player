from kivy.lang import Builder
from kivy.properties import BooleanProperty
from kivy.uix.boxlayout import BoxLayout

from ..music.tracks import TrackItem
from ..widgets.albumcover import AlbumCover
from ..widgets.atlasicon import AtlasIcon
from ..widgets.simpletrackinfo import SimpleTrackInfo


class TrackListItem(TrackItem, BoxLayout):
    current = BooleanProperty(False)


Builder.load_string("""

<TrackListItem>
    size_hint_y: None
    height: 70
    padding: 5
    spacing: 5

    current: root.tlid and root.tlid == app.mm.current.tlid

    #canvas:
        #Color:
            #rgba: (0, 0.9, 0.9, 0.5) if root.current else (0,0,0,0)
        #Line:
            #width: 1
            #rectangle: (self.x + 5, self.y, self.width - 10, self.height)

    canvas.before:
        Color:
            rgba: (0.4, 0.2, 0.2, 0.5) if root.current else (0,0,0,0)
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
            default: root.typeimg
            mipmap: True
            uri: root.uri

        AtlasIcon:
            atlas: 'media'
            item: root.media
            size: (22, 22)
            right: cover.right

    Widget:
        size_hint_x: 0
        width: 1

    SimpleTrackInfo:
        item: root.item

    ImageHoldButton:
        size_hint: 0.15, 0.5
        source: 'playback_play.png' if not root.current else 'playing.zip' if app.mm.state.playback_state == 'playing' else 'playback_pause.png'
        anim_delay: 0.12
        on_release: app.mm.mopidy.playback.play(tlid=root.tlid)

    ImageHoldButton:
        size_hint: 0.15, 0.5
        source: 'action_delete.png'
        on_release: app.mm.mopidy.tracklist.remove(criteria={'tlid':[root.tlid]})

""")
