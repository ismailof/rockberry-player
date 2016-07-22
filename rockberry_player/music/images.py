from kivy.event import EventDispatcher
from kivy.clock import Clock
from kivy.cache import Cache
from kivy.properties import StringProperty, DictProperty
from functools import partial
from utils import scheduled, triggered

from base import MediaController


class AlbumCoverRetriever(MediaController):

    _image_cache = {}
    _requested_uris = set()
    _update_callbacks = {}

    @classmethod
    def request_image(self, uri, callback):
        if not uri or uri in self._image_cache:
            Clock.schedule_once(callback)
            return

        self._requested_uris.add(uri)

        if uri not in self._update_callbacks:
            self._update_callbacks[uri] = set()
        self._update_callbacks[uri].add(callback)

        self._get_server_images()

    @classmethod
    @triggered(0.5)
    def _get_server_images(self, *args):
        if self.interface and self._requested_uris:
            self.interface.get_images(uris=list(self._requested_uris),
                                      on_result=self._update_cache)
            self._requested_uris.clear()

    @classmethod
    def _update_cache(self, images):
        if images:
            self._image_cache.update(images)
            for uri in images.keys():
                for callback in self._update_callbacks.pop(uri, []):
                    Clock.schedule_once(callback)

    @classmethod
    def select_image(self, uri, size=None):
        def compare(a, b):
            if a == 0 or b == 0:
                return 1.0
            return max(a, b) / float(min(a, b))

        if not uri or uri not in self._image_cache:
            return ''

        imagelist = self._image_cache[uri]

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
