from kivy.lang import Builder
from kivy.uix.image import Image
from kivy.properties import StringProperty, NumericProperty, VariableListProperty

from ..music.images import ImageUtils


class AtlasIcon(Image):
    atlas = StringProperty(None)
    item = StringProperty(None, allownone=True)


Builder.load_string("""
#:import ImageUtils rockberry_player.music.images.ImageUtils

<AtlasIcon>
    allowstretch: True
    mipmap: True
    size: (32, 32)
    size_hint: (None, None)
    source: ImageUtils.atlas_image(self.atlas, self.item)

""")
