from kivy.lang import Builder
from kivy.loader import Loader
from kivy.properties import NumericProperty, StringProperty,\
    ListProperty, AliasProperty
from kivy.uix.image import AsyncImage

from widgets.holdbutton import HoldButtonBehavior
from music.base import MediaController
from music.images import ImageUtils, ImageCache
from music.refs import RefUtils
from utils import scheduled

from debug import debug_function


class AlbumCover(AsyncImage):

    border_width = NumericProperty(0)
    uri = StringProperty('', allownone=True)
    default = StringProperty(ImageUtils.IMG_NONE)
    imagelist = ListProperty([])
    background = ListProperty([0, 0, 0, 0])

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
        if not self.uri:
            self.source = ImageUtils.IMG_LOGO
            return

        self.source = self.default
        ImageCache.remove_callback(self.update_imagelist)
        ImageCache.request_item(self.uri, self.update_imagelist)

    def on_parent(self, _, parent):
        if self.parent is None:
            ImageCache.remove_callback(self.update_imagelist)

    def on_imagelist(self, *args):
        self.select_image()

    def on_size(self, *args):
        self.select_image()

    @scheduled
    def on_error(self, error):
        self.source = self.default

    def update_imagelist(self, imagelist, _):
        self.imagelist = imagelist or []

    def select_image(self, *args):
        img_source = ImageUtils.get_fittest_image(
            imagelist=self.imagelist,
            size=self.size)

        # TODO: Currently here. Move anywhere else
        # Local backend. Add server path
        if img_source \
            and RefUtils.get_media_from_uri(self.uri) == 'local' \
            and '://' not in img_source:
            img_source = 'http://' + ImageCache.app.MOPIDY_SERVER + img_source

        self.source = img_source or self.default


class RefreshableCover(HoldButtonBehavior, AlbumCover):

    def refresh(self, *args):
        self.imagelist = []
        ImageCache.remove_items(uris=[self.uri])
        ImageCache.request_item(self.uri, self.update_imagelist)

    def on_hold(self, *args):
        self.refresh()


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

""")
