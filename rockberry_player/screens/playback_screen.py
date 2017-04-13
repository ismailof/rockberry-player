from __future__ import absolute_import, print_function

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

from ..widgets.playback_slider import PlaybackSlider
from ..widgets.playbackbar import PlaybackButton
from ..widgets.playbackbar import PlayButton
from ..widgets.albumcover import AlbumCover
from ..widgets.deviceimage import DeviceImage
from ..widgets.trackinfolabel import TrackInfoLabel
from ..widgets.volumebar import VolumeBar


class PlaybackScreen(Screen):
    pass


Builder.load_string("""
#:import RefUtils rockberry_player.music.refs.RefUtils


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

            PlaybackSlider:
                size_hint: (1, 0.12)
                pos_hint: {'center': 1}
                position: app.mm.state.time_position
                duration: app.mm.current.duration
                resolution: app.mm.state.resolution
                default_text: '\u221e'
                shortcut_secs: 30, 30
                on_seek: app.mm.state.seek(args[1])

            BoxLayout:
                size_hint: (1.04, 0.1)
                pos_hint: {'right': 1.02}
                spacing: 5

                Label:
                    text: app.mm.prev.title
                    text_size: self.size
                    halign: 'left'
                    valign: 'top'
                    shorten: True
                    shorten_from: 'right'

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
                    border_width: 2
                    size_hint: (0.3, 1)
                    uri: app.mm.prev.uri

                    PlaybackButton:
                        action: 'prev'
                        color_released: (1, 1, 1, 0.4)
                        size: self.parent.size
                        pos: self.parent.pos

                PlayButton:
                    size_hint_y: 0.9
                    pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                    color_progress: (1, 1, 1, 0)
                    holdtime: 1.5

                AlbumCover:
                    border_width: 2
                    size_hint: (0.3, 1)
                    uri: app.mm.next.uri

                    PlaybackButton:
                        action: 'next'
                        color_released: (1, 1, 1, 0.4)
                        size: self.parent.size
                        pos: self.parent.pos

""")