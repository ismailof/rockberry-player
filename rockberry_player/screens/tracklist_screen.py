from kivy.lang import Builder
from kivy.logger import Logger
from kivy.clock import triggered
from kivy.uix.screenmanager import Screen
from kivy.properties import NumericProperty, ListProperty

from ..widgets.inputbar import InputBar
from ..widgets.playbackarea import PlaybackArea
from ..widgets.tracklistview import TrackListView

from ..music.tracks import TrackUtils


class TracklistScreen(Screen):

    tracklist = ListProperty()
    filter_words = ListProperty('')
    filtered_tracklist = ListProperty()

    def __init__(self, **kwargs):
        super(TracklistScreen, self).__init__(**kwargs)
        self.bind(tracklist=self.do_filter,
                  filter_words=self.do_filter)

    @triggered(1.7)
    def do_filter(self, *args):
        self.filtered_tracklist = self.get_filtered_tracklist()

    def get_filtered_tracklist(self, *args):
        if not(self.filter_words):
            return self.tracklist

        return [tl_track for tl_track in self.tracklist
                if TrackUtils.matches_words(
                    tl_track['track'],
                    self.filter_words)]

    def format_tracknumber(self, filtered_tl):
        total_no = '%d Tracks' % len(self.tracklist)
        if not(self.filter_words):
            return total_no
        return '%d/%s' % (len(filtered_tl), total_no)


Builder.load_string("""

<OptionsBar@BoxLayout>:
    spacing: 5

    CheckBox:
        active: app.mm.options.random
        on_active: app.mm.options.set_random(args[1])
        background_checkbox_down: 'atlas://options/random_on'
        background_checkbox_normal: 'atlas://options/random_off'

    CheckBox:
        active: app.mm.options.single
        on_active: app.mm.options.set_single(args[1])
        background_checkbox_down: 'atlas://options/single_on'
        background_checkbox_normal: 'atlas://options/single_off'

    CheckBox:
        active: app.mm.options.repeat
        on_active: app.mm.options.set_repeat(args[1])
        background_checkbox_down: 'atlas://options/repeat_on'
        background_checkbox_normal: 'atlas://options/repeat_off'


<TracklistScreen>

    tracklist: app.mm.queue.tracklist

    filter_words: filterbar.text.lower().split(' ') \
        if len(filterbar.text) >= 3 else []

    BoxLayout:
        spacing: 5

        PlaybackArea:
            size_hint_x: 0.4
            item: app.mm.current.item
            #on_press: tlview.scroll_to_index(tlview.current_id - 1)

            BoxLayout:
                spacing: 5
                opacity: 0.5
                size_hint_y: 0.3

                ImageButton:
                    source: 'button_delete.png'
                    on_press: app.mm.queue.clear()

                ImageButton:
                    source: 'button_mix.png'
                    on_press: app.mm.queue.shuffle()

            OptionsBar:
                size_hint_y: 0.3

        BoxLayout:
            orientation: 'vertical'
            spacing: 10

            BoxLayout:
                spacing: 5
                size_hint_y: None
                height: 45
                spacing: 30

                InputBar:
                    id: filterbar
                    title: 'Filter'
                    opacity: 0.6

                Label:
                    text: root.format_tracknumber(root.filtered_tracklist)
                    font_size: 20
                    size_hint_x: 0.2
                    text_size: self.size
                    halign: 'right'

            TrackListView:
                id: tlview
                tlid: app.mm.current.tlid
                tracklist: root.filtered_tracklist
                dial_axis: 'y'
""")
