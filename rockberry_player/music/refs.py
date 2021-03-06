#from __future__ import unicode_literals

from unidecode import unidecode
import re

from kivy.event import EventDispatcher
from kivy.properties import DictProperty, AliasProperty, BooleanProperty

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
            #logger.debug('%s. Item %r is not a Mopidy Model', self.__class__.__name__, item)
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
    def get_media_image(media):
        return ImageUtils.atlas_image(atlas='media', item=media)

    @staticmethod
    def get_words(*text_args):
        # unidecode simplifies accents and tildes from non-ascii letters
        clean_text = unidecode(' '.join(text_args).lower())
        # remove non-alphanumeric and extra spaces
        replace_list = [('[\(\)\[\]\{\}-~_\?\.]', ''),
                        ('\ +', ' ')]
        for orig_str, dest_str in replace_list[:]:
            clean_text = re.sub(orig_str, dest_str, clean_text)

        return set(clean_text.split(' '))


class RefItem(EventDispatcher):

    ref = DictProperty(RefUtils.RefNone, rebind=True)
    item = DictProperty(rebind=True)

    def __init__(self, item=None, **kwargs):
        super(RefItem, self).__init__(**kwargs)
        self.item = item or {}

    def on_item(self, *args):
        self.ref = RefUtils.make_reference(self.item)

    title = AliasProperty(lambda x: RefUtils.get_title(x.ref), None, bind=['ref'])
    reftype = AliasProperty(lambda x: RefUtils.get_type(x.ref), None, bind=['ref'])
    uri = AliasProperty(lambda x: RefUtils.get_uri(x.ref), None, bind=['ref'])
    media = AliasProperty(lambda x: RefUtils.get_media_from_uri(x.uri), None, bind=['uri'])
    typeimg = AliasProperty(lambda x: ImageUtils.get_type_image(x.reftype), None, bind=['reftype'])
    words = AliasProperty(lambda x: RefUtils.get_words(x.title), None, bind=['title'])
