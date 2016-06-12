from kivy.lang import Builder
from kivy.properties import VariableListProperty, OptionProperty
from kivy.uix.boxlayout import BoxLayout

from music.tracks import TrackItem


class SimpleTrackInfo(TrackItem, BoxLayout):
    align = OptionProperty('left', options=['left', 'center', 'right', 'justify'])
    font_size = VariableListProperty([20, 15], length=2)


Builder.load_string("""

<NiceLabel@Label>:
    text_size: (self.width, None)
    size_hint_y: None
    height: self.texture_size[1]
    shorten: True
    shorten_from: 'right'

<SimpleTrackInfo>:
    BoxLayout:
        orientation:'vertical'
        spacing: 2
        #size_hint_y: None
        #height: sum([children.height + 2 for children in self.children])
        pos_hint: {'top': 1}

        NiceLabel:
            #id: lbl_title
            text: root.title
            bold: True
            halign: root.align
            font_size: root.font_size[0]

        NiceLabel:
            #id: lbl_artists
            text: root.artists
            halign: root.align
            font_size: root.font_size[1]

        NiceLabel:
            #id: lbl_album
            text: root.album
            halign: root.align
            font_size: root.font_size[1]
""")
