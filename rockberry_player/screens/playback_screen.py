from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

from widgets.playback_slider import PlaybackSlider
from widgets.playbackbar import PlaybackBar
from widgets.albumcover import AlbumCover
from widgets.deviceimage import DeviceImage
from widgets.trackinfolabel import TrackInfoLabel


class PlaybackScreen(Screen):
    pass



Builder.load_string("""
#:set default_atlas 'atlas:///usr/local/lib/python2.7/dist-packages/kivy/data/images/defaulttheme/'
#:import ImageUtils music.images.ImageUtils

<OptionsBar@BoxLayout>:
    spacing: 5
    padding_x: 10

    CheckBox:
        active: app.mm.options.random
        on_active: app.mm.options.set_random(args[1])
        background_checkbox_down: 'atlas://images/options/random_on'
        background_checkbox_normal: 'atlas://images/options/random_off'

    CheckBox:
        active: app.mm.options.single
        on_active: app.mm.options.set_single(args[1])
        background_checkbox_down: 'atlas://images/options/single_on'
        background_checkbox_normal: 'atlas://images/options/single_off'

    CheckBox:
        active: app.mm.options.repeat
        on_active: app.mm.options.set_repeat(args[1])
        background_checkbox_down: 'atlas://images/options/repeat_on'
        background_checkbox_normal: 'atlas://images/options/repeat_off'

<VolumeBar@BoxLayout>:
    spacing: 5

    CheckBox:
        id: chk_mute
        active: app.mm.mixer.mute or False
        disabled: app.mm.mixer.disabled
        on_active: app.mm.mixer.set_mute(args[1])
        background_checkbox_down: default_atlas + 'audio-volume-muted'
        background_checkbox_normal: default_atlas + 'audio-volume-high'
        size_hint_x: 0.2

    SeekSlider:
        range: (0, 100)
        value: app.mm.mixer.volume or 0
        disabled: app.mm.mixer.disabled
        on_seek: app.mm.mixer.set_volume(args[1])

<PlaybackScreen>:
    BoxLayout:
        spacing:10

        FloatLayout:
            id: albumzone
            size_hint: (0.54, 1)

            AlbumCover:
                id: cover
                uri: app.mm.current.uri
                default: ImageUtils.atlas_image('media', app.mm.current.media)
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
                size_hint: (0.6, 0.1)
                pos_hint: {'right': 1}
                opacity: 0.4

            TrackInfoLabel:
                item: app.mm.current.item
                stream_title: app.mm.state.stream_title
                font_size: 23
                padding_x: 20

            PlaybackSlider:
                size_hint: (1.02, 0.12)
                pos_hint: {'right': 1}
                position: app.mm.state.time_position
                duration: app.mm.current.duration
                resolution: app.mm.state.resolution
                shortcut_secs: 10, 30
                on_seek: app.mm.state.seek(args[1])

            BoxLayout:
                size_hint: (1.02, 0.1)
                pos_hint: {'right': 1}
                spacing: 5

                ReferenceLabel:
                    item: app.mm.prev.item
                    halign: 'left'
                    valign: 'top'
                    shorten: True
                    shorten_from: 'right'

                ReferenceLabel:
                    item: app.mm.next.item
                    halign: 'right'
                    valign: 'top'
                    shorten: True
                    shorten_from: 'right'

            BoxLayout:
                size_hint_y:0.25
                spacing: 20

                OptionsBar:
                    size_hint_x: 0.25
                    pos_hint: {'right': 1}

                PlaybackBar:
                    size_hint_x: 0.8
                    pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                    opacity: 0.5
                    spacing: 5
                    controls: ['stop', 0.1, 'prev', 'play_pause', 'next']

""")
