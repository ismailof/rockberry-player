from functools import partial

from kivy.clock import Clock
from kivy.properties import StringProperty
from kivy.logger import Logger

from .base import MediaController
from ..utils import delayed


class MediaCache(MediaController):

    _cache = {}
    _callbacks = {}
    _requested_uris = set()

    @classmethod
    def request_item(cls, uri, callback):

        if not uri:
            return

        # Update callback
        cb_set = cls._callbacks.get(uri, set())
        cb_set.add(callback)
        cls._callbacks.update({uri: cb_set})

        # URI is found in cache
        cached_item = cls._cache.get(uri)
        if cached_item:
            Logger.debug(
                "{} : _request_item on uri '{}'. Found in cache".format(
                cls.__name__, uri)
            )
            Clock.schedule_once(partial(callback, cached_item))
            return

        # URI not found in cache. Add to request list
        cls._requested_uris.add(uri)
        Logger.debug(
            "{} : _request_item on uri '{}'. Added to request list".format(
                cls.__name__, uri)
        )

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
    def _update_cache(cls, items):
        if not items:
            return

        Logger.debug('{} : _update_cache: {}'.format (cls.__name__, items))
        cls._cache.update(items)
        for uri in items.keys():
            cls._dispatch_item(uri, items[uri])

    @classmethod
    def _dispatch_item(cls, uri, item):
        cb_set = cls._callbacks.get(uri, set())
        for callback in cb_set:
            Logger.trace(
                "{} : _dispatch_item on uri '{}'. Callback:{}".format(
                cls.__name__, uri, callback))
            Clock.schedule_once(partial(callback, item))

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
    def clear_cache(cls):
        cls._cache = {}
        cls._callbacks = {}
