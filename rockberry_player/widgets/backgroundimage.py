from kivy.lang import Builder
from kivy.properties import StringProperty, NumericProperty, ListProperty
from kivy.uix.effectwidget import EffectWidget

from music.images import AlbumCoverRetriever


class BackgroundImage(EffectWidget):
    uri = StringProperty(None, allownone=True)
    #source = StringProperty()
    default = StringProperty()
    tint = ListProperty([1, 1, 1, 1])
    blur_size = NumericProperty(64)
    outbounds = NumericProperty(0)

    #proxy = ProxyImage()

    #def on_uri(self, *args):
        #AlbumCoverRetriever.request_image(self.uri, self.update_image)

    #def update_image(self, *args):
        #self.proxy.source = AlbumCoverRetriever.select_image(self.uri, self.size)
        #self.proxy.bind(on_load=self.cover_loaded)

    #def cover_loaded(self, *args):
        #self.ids['main'].texture = self.ids['proxy'].texture


Builder.load_string("""
#:import HBlur kivy.uix.effectwidget.HorizontalBlurEffect
#:import VBlur kivy.uix.effectwidget.VerticalBlurEffect
#:import Window kivy.core.window.Window

#:set window_size (800, 480)

<BackgroundImage>
    effects: (HBlur(size=10), VBlur(size=10), HBlur(size=self.blur_size), VBlur(size=self.blur_size))
    size_hint: (1 + root.outbounds, 1 + root.outbounds)
    x: - Window.width * root.outbounds/2.0
    y: - Window.height * root.outbounds/2.0

    AlbumCover:
        id: proxy
        keep_ratio: False
        color: root.tint
        default: root.default
        uri: root.uri or ''

    #Image:
        #id: top
        #keep_ratio: False
        #color: root.tint
        ##on_load: root.album_loaded()

""")
