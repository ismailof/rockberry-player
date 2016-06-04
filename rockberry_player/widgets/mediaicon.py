from kivy.lang import Builder
from kivy.uix.image import Image
from kivy.properties import StringProperty, NumericProperty, VariableListProperty


class MediaIcon(Image):
    media = StringProperty(None, allownone=True)
    #icon_size = NumericProperty(32)
    #size = VariableListProperty(32, length=2)


Builder.load_string("""

<MediaIcon>
    allowstretch: True
    mipmap: True
    size: (32, 32)
    size_hint: (None, None)
    source: 'atlas://{}media/{}'.format(app.IMG_FOLDER, root.media or 'null')

""")
