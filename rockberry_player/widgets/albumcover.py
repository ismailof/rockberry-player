from kivy.lang import Builder
from kivy.clock import mainthread
from kivy.properties import NumericProperty, StringProperty,\
    ListProperty, AliasProperty
from kivy.uix.image import AsyncImage

from ..widgets.holdbutton import HoldButtonBehavior
from ..music.images import ImageUtils
from ..music.cache import MediaCache
from ..music.refs import RefUtils


class AlbumCover(HoldButtonBehavior, AsyncImage):

    border_width = NumericProperty(0)
    uri = StringProperty('', allownone=True)
    default = StringProperty(None, allownone=True)
    imagelist = ListProperty([])
    background = ListProperty([0, 0, 0, 0])

    cache = MediaCache(method='library.get_images')
    _prev_uri = ''

    def get_border_rectangle(self):
        return (self.center_x - self.norm_image_size[0] / 2.0,
                self.center_y - self.norm_image_size[1] / 2.0,
                self.norm_image_size[0],
                self.norm_image_size[1])

    border_rectangle = AliasProperty(
        get_border_rectangle,
        None,
        bind=['center', 'size', 'image_ratio']
    )

    def on_uri(self, _, uri):
        if self.uri == self._prev_uri:
            return
        self._prev_uri = self.uri
        self.source = self.default
        self.cache.remove_callback(self.update_imagelist)
        self.cache.request_item(uri=self.uri, callback=self.update_imagelist)

    def on_parent(self, _, parent):
        if self.parent is not None:
            self.source = self.select_image()
        else:
            self.cache.remove_callback(self.update_imagelist)

    def on_size(self, *args):
        self.source = self.select_image()

    @mainthread
    def on_error(self, error):
        self.source = self.default or ImageUtils.IMG_NONE

    @mainthread
    def update_imagelist(self, imagelist, _):
        self.imagelist = imagelist or []
        self.source = self.select_image()

    def select_image(self, *args):
        # Get URL (source) of the fittest image on imagelist
        image = ImageUtils.get_fittest_image(self.imagelist, self.size)
        img_source = image.get('uri')
        if not img_source:
            return self.default

        # Tweeks
        if self.is_uri(img_source):
            # Do not use https
            if img_source.startswith('https:'):
                img_source = 'http:' + img_source[6:]
        else:
            # Local backend. Add server path
            if RefUtils.get_media_from_uri(self.uri) == 'local':
                img_source = 'http://{}{}'.format(MediaCache.app.MOPIDY_SERVER,
                                                  img_source)

        return img_source

    def refresh(self, *args):
        self.imagelist = []
        self.cache.remove_items(uris=[self.uri])
        self.cache.request_item(self.uri, self.update_imagelist)


Builder.load_string("""

<AlbumCover>:
    canvas.before:
        Color:
            rgba: self.background
        Rectangle:
            pos: self.border_rectangle[0], self.border_rectangle[1]
            size: self.border_rectangle[2], self.border_rectangle[3]
    canvas:
        Color:
            rgba: (0.2, 0.2, 0.2, 0.6) if self.border_width else (0,0,0,0)
        Line:
            rectangle: self.border_rectangle
            width: max(self.border_width, 1)

    allow_stretch: True
    holdtime: 1.5
    disabled: not (self.uri or self.default)
    opacity: 0 if self.disabled else 1

""")
