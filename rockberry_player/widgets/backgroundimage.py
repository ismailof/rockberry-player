from kivy.lang import Builder
from kivy.properties import StringProperty, NumericProperty, ListProperty
from kivy.uix.effectwidget import EffectWidget


class BackgroundImage(EffectWidget):
    uri = StringProperty(None, allownone=True)
    default = StringProperty()
    tint = ListProperty([1, 1, 1, 1])
    blur_size = NumericProperty(64)
    outbounds = NumericProperty(0)


Builder.load_string("""
#:import HBlur kivy.uix.effectwidget.HorizontalBlurEffect
#:import VBlur kivy.uix.effectwidget.VerticalBlurEffect
#:import Window kivy.core.window.Window

<BackgroundImage>
    effects: (HBlur(size=10), VBlur(size=10), HBlur(size=self.blur_size), VBlur(size=self.blur_size))
    size_hint: (1 + root.outbounds, 1 + root.outbounds)
    x: - Window.width * root.outbounds/2.0
    y: - Window.height * root.outbounds/2.0

    AlbumCover:
        id: hidden
        keep_ratio: False
        color: root.tint
        default: root.default
        uri: root.uri or ''

    # Image:
        # id: top
        # keep_ratio: False
        # color: root.tint

""")
