from functools import partial

from kivy.clock import Clock
from kivy.properties import StringProperty
from kivy.logger import Logger

from utils import delayed
from base import MediaController


class MediaCache(MediaController):

    _default_cache = {}
    _cache = {}
    _callbacks = {}
    _requested_uris = set()

    @classmethod
    def _update_cache(cls, items):
        if not items:
            return

        Logger.debug('{} : _update_cache: {}'.format (cls.__name__, items))
        cls._cache.update(items)
        for uri in items.keys():
            cb_set = cls._callbacks.get(uri, [])
            Logger.trace(
                "{} : _update_cache on uri '{}'. Callbacks:{}".format(
                    cls.__name__, uri, cb_set)
            )
            for callback in cb_set:
                Clock.schedule_once(partial(callback, items[uri]))

    @classmethod
    def request_item(cls, uri, callback):

        # URI is found in cache
        if not uri or uri in cls._cache:
            Logger.debug(
                "{} : _request_item on uri '{}'. Found in cache".format(
                    cls.__name__, uri)
            )
            Clock.schedule_once(partial(callback, cls._cache.get(uri)))
            return

        # URI not found in cache. Add to request list
        cls._requested_uris.add(uri)
        Logger.debug(
            "{} : _request_item on uri '{}'. Added to request list".format(
                cls.__name__, uri)
        )

        # Update callback
        cb_set = cls._callbacks.get(uri, set())
        cb_set.add(callback)
        cls._callbacks.update({uri: cb_set})

        Logger.trace(
            "{} : _request_item on uri '{}'. Callbacks:{}".format(
                cls.__name__, uri, cb_set)
        )

        # Perform server request
        cls._get_server_items()

    @classmethod
    @delayed(0.5)
    def _get_server_items(cls):
        if not cls.mopidy:
            return

        if cls._requested_uris:
            Logger.debug(
                "{} : _get_server_items for uris: '{}': ".format(
                    cls.__name__, cls._requested_uris)
            )
            cls._server_request(
                uris=list(cls._requested_uris),
                on_result=cls._update_cache
            )
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
    def remove_callback(cls, callback, uri=None):
        for cb_uri in ([uri] if uri else cls._callbacks.keys()):
            cls._callbacks[cb_uri].discard(callback)

    @classmethod
    def set_default_cache(cls, default_cache):
        cls._default_cache.clear()
        cls._default_cache.update(default_cache)

    @classmethod
    def clear_cache(cls):
        cls._cache = dict(cls._default_cache)
        cls._callbacks = {}


class ImageCache(MediaCache):

    _cache = {}
    _requested_uris = set()
    _callbacks = {}
    interface = None

    @classmethod
    def select_image(cls, uri, size=None):
        if not uri:
            return cls.app.IMG_FOLDER + 'neon_R.jpg'

        try:
            imagelist = cls._cache[uri]
        except KeyError:
            return ''

        return get_fittest_image(imagelist, size)

    @classmethod
    def get_fittest_image(cls, imagelist=[], size=None):

        def compare(a, b):
            if a == 0 or b == 0:
                return 1.0
            return max(a, b) / float(min(a, b))

        if not imagelist:
            return ''

        if not size or len(imagelist) == 1:
            # Select first image
            item_fit = 0
        else:
            # Select closest image to size
            size_diff = [compare(image.get('width', 0) + image.get('height', 0),
                                 size[0] + size[1])
                         for image in imagelist]
            item_fit = size_diff.index(min(size_diff))

        image_url = imagelist[item_fit].get('uri', '')

        # Local images. Add server path
        if '://' not in image_url:
            image_url = 'http://' + cls.app.MOPIDY_SERVER + image_url

        return image_url
