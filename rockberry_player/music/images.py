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
    def _update_cache(self, items):
        if not items:
            return

        Logger.debug('%s:_update_cache: %r' % (self.__name__, items))
        self._cache.update(items)
        for uri in items.keys():
            for callback in self._update_callbacks.pop(uri, []):
                Clock.schedule_once(callback)

    @classmethod
    def request_item(self, uri, callback):
        if not uri or uri in self._cache:
            Clock.schedule_once(callback)
            return

        self._requested_uris.add(uri)

        if uri not in self._update_callbacks:
            self._update_callbacks[uri] = set()
        self._update_callbacks[uri].add(callback)

        self._get_server_items()

    @classmethod
    @delayed(0.5)
    def _get_server_items(self):
        if self.mopidy and self._requested_uris:
            self.server_request(
                uris=list(self._requested_uris),
                on_result=self._update_cache)
            self._requested_uris.clear()

    @classmethod
    def server_request(self, *args, **kwargs):
        if self.interface:
            return self.interface(*args, **kwargs)
        else:
            Logger.warning('%s_server_request. No interface set' % (self.__name__))


class ImageCache(MediaCache):

    @classmethod
    def select_image(self, uri, size=None):
        def compare(a, b):
            if a == 0 or b == 0:
                return 1.0
            return max(a, b) / float(min(a, b))

        if not uri:
            return self.app.IMG_FOLDER + 'neon_R.jpg'
        elif uri not in self._cache:
            return ''

        imagelist = self._cache[uri]

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
            image_url = 'http://' + self.app.MOPIDY_SERVER + image_url

        return image_url
