from __future__ import unicode_literals

from kivy.lang import Builder
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.label import Label

from music.tracks import TrackItem
from widgets.referencelabel import ReferenceLabel
from utils import MarkupText


class TrackInfoLabel(TrackItem, ReferenceLabel):

    #font_size = NumericProperty(25)

    def format_title(self):
        if not self.item:
            return MarkupText('<Nothing playing>', size=27, color='#80f0f0')

        parts = self.title.replace('(', '~(').replace('[', '~[').replace(' - ', '~').split('~')
        parts = [MarkupText(item,
                            size=self.font_size if index > 0
                                 else int(self.font_size * 1.3),
                            color='#ffffff',
                            b=True)
                 for index, item in enumerate(parts)]

        return MarkupText('\n'.join(parts),
                          ref=self.new_ref(self.item))

    def format_artists(self):
        if not self.item or 'artists' not in self.item:
            return ''

        artists = self.item['artists']
        artists_list = [MarkupText(artist.get('name'),
                                   size=max(self.font_size - len(artists) // 2, 10),
                                   color='#d0d0d0',
                                   ref=self.new_ref(artist),
                                   )
                        for artist in artists]

        return ' \xb7 '.join(artists_list)

    def format_album(self):
        if not self.item or 'album' not in self.item:
            return ''

        album = self.item['album']

        parts = album.get('name').replace('(', '~(').replace('[', '~[').split('~')
        parts = [MarkupText(item,
                            size=self.font_size if index == 0
                                 else self.font_size - 2)
                 for index, item in enumerate(parts)]

        return MarkupText(''.join(parts),
                          color='#e7e7e7',
                          ref=self.new_ref(album),
                          )

    full_text = StringProperty('')

    def __init__(self, **kwargs):
        super(TrackInfoLabel, self).__init__(**kwargs)
        self.bind(item=self.update_text, stream_title=self.update_text)

    def update_text(self, *args):
        self.clear_refs()
        self.full_text = '\n'.join([self.format_title(),
                                    self.format_artists(),
                                    self.format_album()])


Builder.load_string("""

<TrackInfoLabel>
    text: root.full_text
    markup: True
    halign: 'center'
    valign: 'middle'
    split_str: ' '
    text_size: self.size

""")
