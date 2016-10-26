from __future__ import unicode_literals
from unidecode import unidecode
import re

from kivy.event import EventDispatcher
from kivy.properties import DictProperty, NumericProperty, StringProperty, AliasProperty

from base import MediaController
from utils import scheduled
from refs import RefUtils, RefItem


class TrackUtils(object):

    @staticmethod
    def title_text(track):
        return track.get('name', '') \
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


class TrackItem(RefItem):

    tlid = NumericProperty(0)

    def get_title(self):
        return TrackUtils.title_text(self.item)

    def get_album(self):
        return TrackUtils.album_text(self.item)

    def get_artists(self):
        return TrackUtils.artists_text(self.item)

    def get_duration(self):
        return self.item.length \
            if self.item and 'length' in self.item \
                else None

    title = AliasProperty(get_title, None, bind=['item'])
    album = AliasProperty(get_album, None, bind=['item'])
    artists = AliasProperty(get_artists, None, bind=['item'])
    duration = AliasProperty(get_duration, None, bind=['item'])


class TrackControl(TrackItem, MediaController):

    refresh_method = StringProperty('')
    refresh_args = DictProperty({})

    @scheduled
    def set_tl_track(self, tl_track=None, *args, **kwargs):
        self.tlid = tl_track.get('tlid') if tl_track else 0
        self.item = tl_track.get('track') if tl_track else {}

    @scheduled
    def set_track(self, track=None, *args, **kwargs):
        self.item = track if track else {}

    def refresh(self, *args, **kwargs):
        if self.refresh_method:
            self.mopidy.core.send(
                self.refresh_method,
                on_result=self.set_tl_track,
                **self.refresh_args
            )

    def reset(self, *args):
        self.set_tl_track(tl_track=None)