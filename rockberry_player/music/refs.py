from __future__ import unicode_literals

from kivy.event import EventDispatcher
from kivy.properties import DictProperty, AliasProperty

from ..utils import scheduled
from ..music.images import ImageUtils


class RefUtils(object):

    RefNone = {'__model__': 'Ref',
               'type': '',
               'name': '',
               'uri': None}

    RefPlaylists = {'__model__': 'Ref',
                    'type': 'directory',
                    'name': 'Playlists',
                    'uri': 'playlists:'}

    @staticmethod
    def make_reference(item):
        if not item:
            return RefUtils.RefNone

        if '__model__' not in item:
            print 'item %r is not a Mopidy Model' % item
            return RefUtils.RefNone

        if item['__model__'] == 'Ref':
            return item

        return {'__model__': 'Ref',
                'type': item.get('__model__'),
                'name': item.get('name'),
                'uri': item.get('uri')
                }

    @staticmethod
    def get_title(item):
        return item.get('name', '') \
            if item else ''

    @staticmethod
    def get_type(item):
        return item.get('type', '').lower() \
            if item else ''

    @staticmethod
    def get_uri(item):
        return item.get('uri', '') \
            if item else ''

    @staticmethod
    def get_media_from_uri(uri):
        specials = {'spotifyweb': 'spotify',
                    'yt': 'youtube',
                    'm3u': 'local',
                   }
        uri_header = uri.split(':')[0].split('+')[0] if uri else ''
        if uri_header in specials:
            return specials[uri_header]
        else:
            return uri_header

    @staticmethod
    def get_type_image(reftype):
        def_imgs = {'directory': 'browse_folder.png',
                    'playlist': 'browse_pl.png',
                    'track': 'default_track.png',
                    'album': 'default_album.png',
                    'artist': 'browse_artist.png'}
        return def_imgs.get(reftype, ImageUtils.IMG_LOGO)

    @staticmethod
    def get_media_image(media):
        return ImageUtils.atlas_image(atlas='media', 
                                      item=media)


class RefItem(EventDispatcher):

    ref = DictProperty(RefUtils.RefNone, rebind=True)
    item = DictProperty(rebind=True)

    def __init__(self, item=None, **kwargs):
        super(RefItem, self).__init__(**kwargs)
        self.item = item or {}

    def on_item(self, *args):
        self.ref = RefUtils.make_reference(self.item)

    def get_title(self):
        return RefUtils.get_title(self.ref)

    def get_reftype(self):
        return RefUtils.get_type(self.ref)

    def get_uri(self):
        return RefUtils.get_uri(self.ref)

    def get_media(self):
        return RefUtils.get_media_from_uri(self.uri)

    def get_typeimg(self):
        return RefUtils.get_type_image(self.reftype)

    title = AliasProperty(get_title, None, bind=['ref'])
    reftype = AliasProperty(get_reftype, None, bind=['ref'])
    uri = AliasProperty(get_uri, None, bind=['ref'])
    media = AliasProperty(get_media, None, bind=['uri'])
    typeimg = AliasProperty(get_typeimg, None, bind=['reftype'])
