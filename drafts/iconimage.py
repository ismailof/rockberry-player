from kivy.uix.image import Image
from kivy.atlas import Atlas
from kivy.graphics.texture import Texture
from kivy.properties import StringProperty, ObjectProperty, AliasProperty


class IconImage (Image):

    icon = StringProperty(None, allownone=True)
    default = StringProperty('null')
    atlasname = StringProperty('')
    atlas = ObjectProperty(None)

    def get_atlas_keys(self):
        return self.atlas.textures.keys() if self.atlas else []

    keys = AliasProperty(get_atlas_keys, None, bind=['atlas'])

    def on_atlasname(self, *args):
        self.atlas = Atlas(self.atlasname + '.atlas')

    def on_default(self, *args):
        if self.atlas:
            assert self.default in self.keys, "'%s' is not a key of Atlas '%s'" % (self.default, self.atlasname)

    def on_icon(self, *args):
        if self.atlas and self.icon is not None:
            if self.icon in self.keys:
                self.texture = self.atlas[self.icon]
            else:
                self.icon = self.default
                self.texture = self.atlas[self.default]
        else:
            self.texture = Texture.create()
