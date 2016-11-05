from kivy.lang import Builder
from kivy.uix.image import Image
from kivy.properties import StringProperty, NumericProperty, VariableListProperty


class AtlasIcon(Image):
    atlas = StringProperty(None)
    item = StringProperty(None, allownone=True)


Builder.load_string("""

<AtlasIcon>
    allowstretch: True
    mipmap: True
    size: (32, 32)
    size_hint: (None, None)
    source: 'atlas://{}{}/{}'.format(app.IMG_FOLDER, root.atlas, root.item or 'null') if root.atlas else app.IMG_FOLDER + 'transparent.png'

""")
