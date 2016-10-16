from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout

from widgets.atlasicon import AtlasIcon
from music.refs import RefItem


class PlaybackArea(RefItem, BoxLayout):
    pass


Builder.load_string("""

<PlaybackArea>:

    orientation: 'vertical'
    padding: 15
    spacing: 5

    canvas.before:
        Color:
            rgba: (0.4, 0.4, 0.4, 0.2)
        Rectangle:
            pos: self.pos
            size: self.size

    RelativeLayout:

        RefreshableCover:
            id: cover
            uri: root.uri
            default: app.IMG_FOLDER + root.defaultimg
            border_width: 2
            background: (0.3, 0.3, 0.3, 0.5)
            size_hint_x: 0.9
            pos_hint: {'center_x': 0.5}

        AtlasIcon:
            atlas: 'media'
            item: root.media
            size: (32, 32)
            right: cover.border_rectangle[0] + cover.border_rectangle[2] - 2
            y: cover.border_rectangle[1] + 2

    Label:
        text: root.title
        size_hint_y: 0.4
        halign: 'center'
        valign: 'top'
        text_size: self.size
        font_size: 20
        bold: True

""")
