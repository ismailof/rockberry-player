from kivy.lang import Builder
from kivy.properties import NumericProperty, StringProperty,\
    ListProperty, AliasProperty
from kivy.uix.image import AsyncImage

from music.images import ImageCache


class AlbumCover(AsyncImage):

    border_width = NumericProperty(0)
    uri = StringProperty('', allownone=True)
    default = StringProperty('')
    background = ListProperty([0, 0, 0, 0])

    def get_border_rectangle(self):
        return (self.center_x - self.norm_image_size[0] / 2.0,
                self.center_y - self.norm_image_size[1] / 2.0,
                self.norm_image_size[0],
                self.norm_image_size[1])

    border_rectangle = AliasProperty(get_border_rectangle,
                                     None,
                                     bind=['center', 'size', 'image_ratio'])

    def update_image(self, *args):
        new_source = ImageCache.select_image(uri=self.uri,
                                             size=self.size)

        if self.source != new_source:
            self.source = new_source

    def on_uri(self, *args):
        ImageCache.request_item(self.uri, self.update_image)

    def on_size(self, *args):
        self.update_image()

    def on_source(self, *args):
        if not self.source and self.default:
            self.source = self.default

    def on_default(self, instance, source):
        if not self.source and self.default:
            self.source = self.default

    def refresh(self, *args):
        ImageCache.remove_items(uris=[self.uri])
        ImageCache.request_item(self.uri, self.update_image)


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

    default: app.IMG_FOLDER + 'default_track.png'
    allow_stretch: True

""")
