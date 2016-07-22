from __future__ import unicode_literals
from unidecode import unidecode
import re

from kivy.event import EventDispatcher
from kivy.properties import DictProperty, NumericProperty, StringProperty, AliasProperty

from utils import scheduled
from refs import RefUtils, RefItem


class TrackItem(RefItem):

    track = DictProperty(rebind=True)
    tlid = NumericProperty(0)
    stream_title = StringProperty(None, allownone=True)

    def get_title(self):
        return TrackUtils.title_text(self.track, self.stream_title)

    def get_album(self):
        return TrackUtils.album_text(self.track)

    def get_artists(self):
        return TrackUtils.artists_text(self.track)

    def get_duration(self):
        return self.track.length \
            if self.track and 'length' in self.track \
                else None

    title = AliasProperty(get_title, None, bind=['track', 'stream_title'])
    album = AliasProperty(get_album, None, bind=['track'])
    artists = AliasProperty(get_artists, None, bind=['track'])
    duration = AliasProperty(get_duration, None, bind=['track'])

    def on_track(self, *args):
        self.ref = RefUtils.make_reference(self.track)


class TrackControl(TrackItem):

    _refresh_function = None

    @scheduled
    def set_tl_track(self, tl_track=None, *args, **kwargs):
        self.tlid = tl_track.get('tlid') if tl_track else 0
        self.track = tl_track.get('track') if tl_track else {}

    @scheduled
    def set_track(self, track=None, *args, **kwargs):
        self.track = track if track else {}

    @scheduled
    def set_stream_title(self, title, *args, **kwargs):
        self.stream_title = title

    @scheduled
    def reset_stream_title(self, *args, **kwargs):
        self.stream_title = None

    def refresh(self, *args, **kwargs):
        if self._refresh_function:
            self._refresh_function(
                on_result=self.set_tl_track)


class TrackUtils(object):

    @staticmethod
    def title_text(track, stream_title=None):
        return stream_title or track.get('name', '') \
            if track else ''

    @staticmethod
    def artists_text(track, separator=', '):
        return separator.join([artist.get('name', '')
                               for artist in track.get('artists', [])]) \
            if track else ''

    @staticmethod
    def album_text(track):
        return track.get('album', {}).get('name', '') \
            if track else ''

    @staticmethod
    def words_in_track(track):
        full_text = ' '.join([TrackUtils.title_text(track),
                              TrackUtils.artists_text(track),
                              TrackUtils.album_text(track)]).lower()

        clean_text = unidecode(full_text)

        replace_list = [('[\(\)\[\]\{\}-~_\?]', ''),
                        ('\ +', ' '),
                        ]

        for orig_str, dest_str in replace_list[:]:
            clean_text = re.sub(orig_str, dest_str, clean_text)

        return set(clean_text.split(' '))
