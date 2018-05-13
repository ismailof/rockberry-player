from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout

from ..widgets.baserefitem import RefItemImage
from ..music.refs import RefItem


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

    RefItemImage:
        ref: root.ref
        iconsize: 32
        size_hint_x: 0.9
        pos_hint: {'center_x': 0.5}
        #on_hold: self.refresh()

    Label:
        text: root.title
        size_hint_y: 0.4
        halign: 'center'
        valign: 'top'
        text_size: self.size
        font_size: 20
        bold: True

""")
