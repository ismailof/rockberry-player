from pyechonest import config
from pyechonest import song
import sys

config.ECHO_NEST_API_KEY="9BTWYWYBMQHYQIHSV"

from mopidy_json_client.common import *


def get_info_song(title, artist):
    songs = song.search(title=str(title),
                        artist=str(artist),
                        buckets=['song_type', 'song_hotttnesss', 'id:spotify'])
    return songs[0] if songs else None


@debug_function
def get_genre(title, artist):
    song = get_info_song(title, artist)
    return song.get_song_type(cache=False) if song else []


if __name__ == '__main__':
    title = sys.argv[1]
    artist = sys.argv[2]
    print 'Buscando info sobre %s - %s' % (title, artist)
    songs = get_info_song(title, artist)
    if songs is None:
        print 'Sin Resultados'
    else:
        print 'Generos: %s' % ', '.join(songs.song_type)
