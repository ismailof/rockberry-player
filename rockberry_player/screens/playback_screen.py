from __future__ import absolute_import, print_function

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

from ..widgets.albumcover import AlbumCover
from ..widgets.deviceimage import DeviceImage
from ..widgets.trackinfolabel import TrackInfoLabel
from ..widgets.volumebar import VolumeBar
from ..widgets.imageholdbutton import PlaybackButton
from ..widgets.progress_rectangle import ProgressRectangle


class PlaybackScreen(Screen):
    pass


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
                    size_hint: (0.3, 1)
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
                        progress_color: (1, 1, 1, 0.3)
                        progress_value: app.mm.state.time_position or 0
                        progress_max: app.mm.current.duration or 0

                    BoxLayout:
                        size: self.parent.size
                        pos: self.parent.pos

                        Label:
                            text: TrackUtils.format_time(app.mm.state.time_position) if app.mm.current.duration else ''
                            halign: 'left'
                            text_size: self.size

                        Label:
                            text: TrackUtils.format_time(app.mm.current.duration)
                            halign: 'right'
                            text_size: self.size

                AlbumCover:
                    size_hint: (0.3, 1)
                    border_width: 2
                    uri: app.mm.next.uri

                    PlaybackButton:
                        action: 'next'
                        color_released: (1, 1, 1, 0.75)
                        pos: self.parent.pos
                        size: self.parent.size

""")