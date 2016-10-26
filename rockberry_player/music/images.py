from kivy.clock import Clock
from kivy.properties import StringProperty, DictProperty
from kivy.logger import Logger

from utils import delayed
from base import MediaController


class MediaCache(MediaController):

    _cache = {}
    _requested_uris = set()
    _update_callbacks = {}

    @classmethod
    def _update_cache(cls, items):
        if not items:
            return

        Logger.debug('%s:_update_cache: %r' % (cls.__name__, items))
        cls._cache.update(items)
        for uri in items.keys():
            for callback in cls._update_callbacks.pop(uri, []):
                Clock.schedule_once(callback)

    @classmethod
    def request_item(cls, uri, callback):
        if not uri or uri in cls._cache:
            Clock.schedule_once(callback)
            return

        cls._requested_uris.add(uri)

        if uri not in cls._update_callbacks:
            cls._update_callbacks[uri] = set()
        cls._update_callbacks[uri].add(callback)

        cls._get_server_items()

    @classmethod
    @delayed(0.5)
    def _get_server_items(cls):
        if cls.mopidy and cls._requested_uris:
            cls._server_request(
                uris=list(cls._requested_uris),
                on_result=cls._update_cache)
            cls._requested_uris.clear()

    @classmethod
    def _server_request(cls, *args, **kwargs):
        if cls.interface:
            return cls.interface(*args, **kwargs)
        else:
            Logger.warning('%s_server_request. No interface set' % (cls.__name__))

    @classmethod
    def remove_items(cls, uris):
        for uri in uris:
            if uri in cls._cache:
                del cls._cache[uri]

    @classmethod
    def clear_cache(cls):
        cls._cache = {}

class ImageCache(MediaCache):

    _cache = {}
    _requested_uris = set()
    _update_callbacks = {}
    interface = None

    @classmethod
    def select_image(cls, uri, size=None):
        def compare(a, b):
            if a == 0 or b == 0:
                return 1.0
            return max(a, b) / float(min(a, b))

        if not uri:
            return cls.app.IMG_FOLDER + 'neon_R.jpg'
        elif uri not in cls._cache:
            return ''

        imagelist = cls._cache[uri]

        if not imagelist:
            return ''

        if not size or len(imagelist) == 1:
            # Select first image
            item_fit = 0
        else:
            # Select fittest image to size
            size_diff = [compare(image.get('width', 0) + image.get('height', 0),
                                 size[0] + size[1])
                         for image in imagelist]
            item_fit = size_diff.index(min(size_diff))

        image_url = imagelist[item_fit].get('uri', '')

        # Local images. Add server path
        if '://' not in image_url:
            image_url = 'http://' + cls.app.MOPIDY_SERVER + image_url

        return image_url
