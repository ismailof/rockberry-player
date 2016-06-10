from kivy.lang import Builder
from kivy.properties import NumericProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout

from music.tracks import TrackBehavior
from widgets.albumcover import AlbumCover
from widgets.mediaicon import MediaIcon
from widgets.simpletrackinfo import SimpleTrackInfo


class TrackListItem(TrackBehavior, BoxLayout):
    current = BooleanProperty(False)


Builder.load_string("""

<TrackListItem>
    size_hint_y: None
    height: 70
    padding: 5
    spacing: 10

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
            mipmap: True
            uri: root.uri

        MediaIcon:
            size: (22, 22)
            right: cover.right
            media: root.media

    SimpleTrackInfo:
        track: root.track

    Image:
        size_hint_x: 0.15
        source: app.IMG_FOLDER + ('playing.zip' if root.current and app.mm.state.playing else 'transparent.png')
        anim_delay: 0.12

    Button:
        size_hint_x: 0.2
        opacity: 0.7
        text: 'play'
        on_press: app.mm.mopidy.playback.play(tlid=root.tlid)

    Button:
        size_hint_x: 0.2
        opacity: 0.7
        text: 'del'
        on_press: app.mm.mopidy.tracklist.remove(criteria={'tlid':[root.tlid]})
""")