from kivy.event import EventDispatcher
from kivy.properties import ObjectProperty, ListProperty, AliasProperty

from base import MediaController
from refs import RefUtils, RefItem

from utils import scheduled
from debug import debug_function


class BrowserControl (MediaController):

    reflist = ListProperty([])
    browse_tree = ListProperty([RefUtils.RefNone])
    browse_ref = AliasProperty(lambda self: self.browse_tree[-1], None, bind=['browse_tree'])

    @scheduled
    def set_reflist(self, reflist, *args):
        self.reflist = reflist

    def on_browse_ref(self, *args):
        self.refresh()

    def refresh(self, *args):
        self.reflist = []
        # TEMPORAL WORKAROUND FOR GETTING PLAYLISTS
        if self.browse_ref['uri'] == 'playlists:':
            self.mopidy.playlists.as_list(on_result=self.set_reflist)
        else:
            self.interface.browse(uri=self.browse_ref['uri'],
                                       on_result=self.set_reflist)


    @scheduled
    def browse(self, item):
        self.browse_tree.append(RefUtils.make_reference(item))
        self.app.main.switch_to(screen='browse')

    @scheduled
    def browse_back(self):
        if len(self.browse_tree) > 1:
            self.browse_tree.pop()

    @scheduled
    def browse_home(self):
        self.browse_tree = [RefUtils.RefNone]

    def browse_playlists(self):
        self.browse_tree.append(RefUtils.RefPlaylists)