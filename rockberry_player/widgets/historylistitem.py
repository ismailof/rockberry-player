from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout

from kivy.properties import AliasProperty, \
    NumericProperty, BooleanProperty

from ..music.refs import RefItem
from ..widgets.albumcover import AlbumCover
from ..widgets.atlasicon import AtlasIcon


class RefListItem(RefItem, HoldButtonBehavior, BoxLayout):

    index = NumericProperty()
    selected = BooleanProperty(False)

    def get_ref_action(self, *args):
        return 'play' if self.reftype == 'track' else 'browse'

    action = AliasProperty(get_ref_action, None, bind=['reftype'])
