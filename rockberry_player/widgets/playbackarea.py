from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty

from widgets.mediaicon import MediaIcon


class PlaybackArea(BoxLayout):

    item = ObjectProperty(None, rebind=True)


Builder.load_string("""
<PlaybackArea>

    orientation: 'vertical'
    padding: 15
    spacing: 15

    canvas.before:
        Color:
            rgba: (0.4, 0.4, 0.4, 0.2)
        Rectangle:
            pos: self.pos
            size: self.size

    BoxLayout:
        spacing:  10
        orientation: 'vertical'

        RelativeLayout:
            AlbumCover:
                id: cover
                uri: root.item.uri if root.item else ''
                border_width: 2
                background: (0.3, 0.3, 0.3, 0.5)
                size_hint_x: 0.9
                pos_hint: {'center_x': 0.5}

            MediaIcon:
                size: (32, 32)
                right: cover.border_rectangle[0] + cover.border_rectangle[2] - 2
                y: cover.border_rectangle[1] + 2
                media: root.item.media if root.item else ''

        Label:
            text: root.item.title if root.item else ''
            multiline: 2
            halign: 'center'
            valign: 'top'
            text_size: self.size
            font_size: 20
            bold: True

        #SimpleTrackInfo:
            #size_hint_y: 0.4
            #align: 'center'
            #font_size: (17, 16)
            #track: app.mm.current.track


        PlaybackBar:
            opacity: 0.5
            controls: ['play_pause', 'next']
            size_hint_y: 0.4
""")
