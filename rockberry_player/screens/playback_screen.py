from __future__ import absolute_import, print_function

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

from ..widgets.albumcover import AlbumCover
from ..widgets.deviceimage import DeviceImage
from ..widgets.trackinfolabel import TrackInfoLabel
from ..widgets.volumebar import VolumeBar
from ..widgets.imageholdbutton import PlaybackButton
from ..widgets.progress_rectangle import ProgressRectangle

from ..music.tracks import TrackUtils
from ..utils import MarkupText


class PlaybackScreen(Screen):

    def format_time(self, time):
        if time is None:
            return ''

        time_secs = int(round(time * TrackUtils.time_resolution))
        time_st = {'s': time_secs % 60,
                   'm': (time_secs // 60) % 60,
                   'h': time_secs // 3600}

        if time_secs >= 3600:
            time_format = MarkupText('{h:d} ', size=18) \
                + MarkupText('{m:02d} ', size=18, b=True) \
                + MarkupText('{s:02d}', size=14)
        elif time_secs >= 60:
            time_format = MarkupText('{m:d} ', size=18, b=True) \
                + MarkupText('{s:02d}', size=14)
        else:
            time_format = MarkupText(' ', size=18, b=True) \
                + MarkupText('{s:02d}', size=14)

        return time_format.format(**time_st)


Builder.load_string("""

<PlaybackScreen>:
    BoxLayout:
        spacing:10

        FloatLayout:
            id: albumzone
            size_hint: (0.54, 1)

            AlbumCover:
                id: cover
                uri: app.mm.current.uri
                default: RefUtils.get_media_image(app.mm.current.media) if app.mm.current.media else ImageUtils.IMG_LOGO
                border_width: 0 if device_image.device in ['radio'] else 3
                pos_hint: {'center_x': 0.5, 'y': 0.36}
                size_hint: (None, None)
                height: albumzone.width * 0.87
                width: self.height * min(self.image_ratio, 1.3)
                on_click: app.mm.browser.browse(app.mm.current.item.get('album'))
                on_hold: self.refresh()

            DeviceImage:
                id: device_image
                size_hint_x: 1.2
                pos_hint: {'right': 1.1, 'center_y': 0.26}
                media: app.mm.current.media
                playing: app.mm.state.playback_state == 'playing'

        BoxLayout:
            orientation: 'vertical'
            spacing: 10

            VolumeBar:
                size_hint: (1, 0.1)
                pos_hint: {'right': 1}
                opacity: 0.4
                text: 'MASTER'
                mixer: app.mm.mixer

            TrackInfoLabel:
                item: app.mm.current.item
                stream_title: app.mm.state.stream_title
                font_size: 23
                padding_x: 20

            BoxLayout:
                size_hint: (1.04, 0.1)
                pos_hint: {'right': 1.02}
                spacing: 10

                Label:
                    text: app.mm.prev.title
                    text_size: self.size
                    halign: 'left'
                    valign: 'top'
                    shorten: True
                    shorten_from: 'right'

                Widget:

                Label:
                    text: app.mm.next.title
                    text_size: self.size
                    halign: 'right'
                    valign: 'top'
                    shorten: True
                    shorten_from: 'right'

            BoxLayout:
                size_hint_y: 0.4
                spacing: 20

                AlbumCover:
                    size_hint_x: None
                    width: self.height
                    border_width: 2
                    uri: app.mm.prev.uri

                    PlaybackButton:
                        action: 'prev'
                        color_released: (1, 1, 1, 0.75)
                        pos: self.parent.pos
                        size: self.parent.size

                PlaybackButton:
                    action: 'pause' if app.mm.state.playback_state == 'playing' else 'play'
                    on_hold: self.action = 'stop'
                    size_hint_y: 0.8
                    holdtime: 1.5

                    ProgressRectangle:
                        size: self.parent.size
                        pos: self.parent.pos
                        color: (1, 1, 1, 0.3)
                        value: app.mm.state.time_position or 0
                        max: app.mm.current.duration or 0

                    BoxLayout:
                        orientation: 'vertical'
                        size: self.parent.size
                        pos: self.parent.pos

                        Label:
                            text: root.format_time(app.mm.state.time_position) if app.mm.current.duration else ''
                            markup: True
                            halign: 'right'
                            valign: 'top'
                            text_size: self.size

                        Label:
                            text: root.format_time(app.mm.current.duration)
                            markup: True
                            halign: 'right'
                            valign: 'bottom'
                            text_size: self.size

                AlbumCover:
                    size_hint_x: None
                    width: self.height
                    border_width: 2
                    uri: app.mm.next.uri

                    PlaybackButton:
                        action: 'next'
                        color_released: (1, 1, 1, 0.75)
                        pos: self.parent.pos
                        size: self.parent.size

""")
