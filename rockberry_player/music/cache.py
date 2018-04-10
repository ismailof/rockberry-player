from functools import partial

from kivy.clock import Clock
from kivy.logger import Logger

from .base import MediaController
from ..utils import triggered


class MediaCache(MediaController):

    def __init__(self, method=None, **kwargs):
        super(MediaCache, self).__init__(**kwargs)
        self._cache = {}
        self._callbacks = {}
        self._requested_uris = set()
        self.server_method = method

    def request_item(self, uri, callback):
        if not uri:
            return

        # Update callback
        cb_set = self._callbacks.get(uri, set())
        cb_set.add(callback)
        self._callbacks.update({uri: cb_set})

        # URI is found in cache
        cached_item = self._cache.get(uri)
        if cached_item:
            Logger.debug(
                "{} : _request_item on uri '{}'. Found in cache".format(
                self.__class__.__name__, uri)
            )
            Clock.schedule_once(partial(callback, cached_item))
            return

        # URI not found in cache. Add to request list
        self._requested_uris.add(uri)
        Logger.debug(
            "{} : _request_item on uri '{}'. Added to request list".format(
                self.__class__.__name__, uri)
        )

        Logger.trace(
            "{} : _request_item on uri '{}'. Callbacks:{}".format(
                self.__class__.__name__, uri, cb_set)
        )

        # Perform server request
        self._get_server_items()

    @triggered(0.5)
    def _get_server_items(self):
        if not self.mopidy:
            return

        if self._requested_uris:
            Logger.debug(
                "{} : _get_server_items for uris: '{}': ".format(
                    self.__class__.__name__, self._requested_uris)
            )
            self.call_method(
                method=self.server_method,
                uris=list(self._requested_uris),
                on_result=self._update_cache
            )
            self._requested_uris.clear()

    def _update_cache(self, items):
        if not items:
            return

        Logger.debug('{} : _update_cache: {}'.format(self.__class__.__name__, items))
        self._cache.update(items)
        for uri in items.iterkeys():
            self._dispatch_item(uri, items[uri])

    def _dispatch_item(self, uri, item):
        cb_set = self._callbacks.get(uri, set())
        for callback in cb_set:
            Logger.trace(
                "{} : _dispatch_item on uri '{}'. Callback:{}".format(
                self.__class__.__name__, uri, callback))
            Clock.schedule_once(partial(callback, item))

    def remove_items(self, uris):
        for uri in uris:
            if uri in self._cache:
                del self._cache[uri]

    def remove_callback(self, callback, uri=None):
        for cb_uri in ([uri] if uri else self._callbacks.keys()):
            self._callbacks[cb_uri].discard(callback)

    def clear_cache(self):
        self._cache = {}
        self._callbacks = {}
