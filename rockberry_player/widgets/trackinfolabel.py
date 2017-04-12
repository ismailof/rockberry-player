from __future__ import unicode_literals

from kivy.properties import StringProperty

from ..widgets.referencelabel import ReferenceLabel
from ..music.tracks import TrackItem
from ..utils import MarkupText


class TrackInfoLabel(TrackItem, ReferenceLabel):

    full_text = StringProperty('')
    stream_title = StringProperty('')

    def __init__(self, **kwargs):
        super(TrackInfoLabel, self).__init__(**kwargs)
        self.bind(item=self.update_text, stream_title=self.update_text)
        self.update_text()

    def update_text(self, *args):
        self.clear_refs()
        self.text = self.format_track()

    def format_track(self, *args):
        # Text for No Track
        if not self.item:
            return MarkupText('Browse Music ...',
                              size=30,
                              color='#80f0f0',
                              b=True,
                              ref=self.new_ref(None))

        # Use stream_title as 'Artist - Track'.
        if self.stream_title:
            try:
                artist, title = self.stream_title.split(' - ', 1)
                return '\n'.join([self.format_title(title),
                                  self.format_artists([{'name': artist,
                                                        '__model__': 'artist'}]),
                                  self.format_album(self.item.get('album', ''))])
            except:
                pass

        # Tunein station with no stream_title. Return only station name
        if self.media == 'tunein' and not self.stream_title:
            return self.format_title(self.title)

        # Usual format
        return '\n'.join([self.format_title(self.stream_title or self.title),
                          self.format_artists(self.item.get('artists')),
                          self.format_album(self.item.get('album', ''))])

    def format_title(self, title):
        parts = title.replace('(', '~(').replace('[', '~[').replace(' - ', '~').split('~')
        parts = [MarkupText(textpart,
                            size=self.font_size if index > 0
                                 else int(self.font_size * 1.3),
                            color='#ffffff',
                            b=True)
                 for index, textpart in enumerate(parts)]

        return MarkupText('\n'.join(parts),
                          ref=self.new_ref(self.item))

    def format_artists(self, artists):
        if not artists:
            return ''

        artists_list = [
            MarkupText(artist.get('name'),
                       size=max(self.font_size - len(artists) // 2, 10),
                       color='#d0d0d0',
                       ref=self.new_ref(artist))
            for artist in artists]

        return ' \xb7 '.join(artists_list)

    def format_album(self, album):
        parts = album.get('name').replace('(', '~(').replace('[', '~[').split('~')
        parts = [
            MarkupText(item,
                       size=self.font_size if index == 0 else self.font_size - 2)
            for index, item in enumerate(parts)]

        return MarkupText(''.join(parts),
                          color='#e7e7e7',
                          ref=self.new_ref(album))



