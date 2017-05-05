from __future__ import unicode_literals

from kivy.event import EventDispatcher
from kivy.properties import DictProperty, NumericProperty, StringProperty, AliasProperty

from base import MediaController
from ..utils import scheduled
from refs import RefUtils, RefItem


class TrackUtils(object):

    time_resolution = 0.001

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
        return RefUtils.get_words(
            TrackUtils.title_text(track),
            TrackUtils.artists_text(track),
            TrackUtils.album_text(track))

    @staticmethod
    def format_time(time):
        if time is None:
            return ''

        time_secs = int(round(time * TrackUtils.time_resolution))
        time_st = {'s': time_secs % 60,
                   'm': (time_secs // 60) % 60,
                   'h': time_secs // 3600}

        time_format = '{h:d}:{m:02d}:{s:02d}' if time_st['h'] \
            else '{m:d}:{s:02d}'

        return time_format.format(**time_st)

    @staticmethod
    def split_title(text,  max=None):
        separators = [(' - ', '~'), ('[', '~['), ('(', '~('), (' | ', '~')]
        for sep, sub in separators:
            if max:
                remain = max - text.count('~') - 1
                if remain <= 0:
                    break
                text = text.replace(sep, sub, remain)
            else:
                text = text.replace(sep, sub)
        text = text.strip('~')        
        return [part.strip(' \t\n\r') for part in text.split('~')]
        

class TrackItem(RefItem):

    tlid = NumericProperty(0)

    def get_duration(self):
        return self.item.length \
            if self.item and 'length' in self.item \
                else None

    title = AliasProperty(lambda x: TrackUtils.title_text(x.item), None, bind=['item'])
    album = AliasProperty(lambda x: TrackUtils.album_text(x.item), None, bind=['item'])
    artists = AliasProperty(lambda x: TrackUtils.artists_text(x.item), None, bind=['item'])
    words = AliasProperty(lambda x: RefUtils.get_words(x.title, x.album, x.artists), None,
                          bind=['title', 'album', 'artists'])
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
            self.call_method(
                self.refresh_method,
                on_result=self.set_tl_track,
                **self.refresh_args
            )

    def reset(self, *args):
        self.set_tl_track(tl_track=None)