from kivy.lang import Builder
from kivy.properties import ListProperty, NumericProperty, AliasProperty, \
    BooleanProperty
from kivy.uix.boxlayout import BoxLayout

from ..widgets.dialrecycleview import DialRecycleView
from ..widgets.refitemimage import RefItemImage
from ..widgets.simpletrackinfo import SimpleTrackInfo

from ..music.tracks import TrackItem


class TrackListItem(TrackItem, BoxLayout):
    pass


class TrackListView(DialRecycleView):
    tracklist = ListProperty()
    tlid = NumericProperty()

    def find_is_current_index(self):
        if not self.tlid:
            return None
        for index, tl_track in enumerate(self.tracklist):
            if tl_track['tlid'] == self.tlid:
                return index
        return None

    current_id = AliasProperty(find_is_current_index, None, bind=['tracklist', 'tlid'])

    def on_tracklist(self, *args):
        self.data = [{'item': tl_track['track'],
                      'tlid': tl_track['tlid'],
                     } for tl_track in self.tracklist]

    def on_current_id(self, *args):
        self.nav_id = self.current_id


Builder.load_string("""

<TrackListView>:
    viewclass: 'TrackListItem'
    item_height: dp(70)

<TrackListItem>
    size_hint_y: None
    height: 70
    padding: 5
    spacing: 5

    canvas.before:
        Color:
            rgba: (0.4, 0.2, 0.2, 0.5) if root.is_current else (0,0,0,0)
        Rectangle:
            pos: self.pos
            size: self.size

    RefItemImage:
        ref: root.ref
        size_hint_x: None
        width: self.height
        iconsize: 24

    Widget:
        size_hint_x: 0
        width: 1

    SimpleTrackInfo:
        item: root.item

    ImageHoldButton:
        size_hint: 0.15, 0.5
        source: 'playing.zip' if root.is_playing else 'playback_pause.png' if root.is_paused else 'playback_play.png'
        anim_delay: 0.12
        on_release: app.mm.mopidy.playback.play(tlid=root.tlid)

    ImageHoldButton:
        size_hint: 0.15, 0.5
        source: 'action_delete.png'
        on_release: app.mm.mopidy.tracklist.remove(criteria={'tlid':[root.tlid]})

""")
