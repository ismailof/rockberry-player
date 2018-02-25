from kivy.lang import Builder
from kivy.properties import ListProperty, NumericProperty, AliasProperty, \
    BooleanProperty
from kivy.uix.boxlayout import BoxLayout

from ..widgets.dialrecycleview import DialRecycleView, SelectableItem
#from ..widgets.reflistview import RefListView
from ..widgets.albumcover import AlbumCover
from ..widgets.atlasicon import AtlasIcon
from ..widgets.simpletrackinfo import SimpleTrackInfo

from ..music.tracks import TrackItem


class TrackListItem(TrackItem, SelectableItem):
    current = BooleanProperty(False)


class TrackListView(DialRecycleView):
    tracklist = ListProperty()
    tlid = NumericProperty()

    def find_current_index(self):
        if not self.tlid:
            return None
        for index, tl_track in enumerate(self.tracklist):
            if tl_track['tlid'] == self.tlid:
                return index
        return None

    current_id = AliasProperty(find_current_index, None, bind=['tracklist', 'tlid'])

    def on_tracklist(self, *args):
        self.data = [{'item': tl_track['track'],
                      'tlid': tl_track['tlid'],
                      'current': tl_track['tlid'] == self.tlid
                     } for tl_track in self.tracklist]
        self.scroll_to_current()

    def on_current_id(self, *args):
        self.scroll_to_current()

    def on_size(self, *args):
        self.scroll_to_current()

    def scroll_to_current(self):
        if self.current_id is not None:
            self.selected_id = self.current_id
            self.scroll_to_index(self.current_id)


Builder.load_string("""

<TrackListView>:
    viewclass: 'TrackListItem'
    item_height: dp(70)

<TrackListItem>
    size_hint_y: None
    height: 70
    padding: 5
    spacing: 5

    current: root.tlid and root.tlid == app.mm.current.tlid

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
