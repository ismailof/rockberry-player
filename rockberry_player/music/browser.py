from kivy.event import EventDispatcher
from kivy.properties import ObjectProperty, ListProperty, AliasProperty

from base import MediaController
from refs import RefUtils, RefItem

from utils import scheduled
from debug import debug_function


class BrowserControl (MediaController):

    browse_list = ListProperty([])
    browse_tree = ListProperty([RefUtils.RefNone])

    browse_ref = AliasProperty(lambda self: self.browse_tree[-1], None, bind=['browse_tree'])

    @scheduled
    def set_browse_list(self, reflist, *args):
        self.browse_list = [{'ref': ref} for ref in reflist]

    def on_browse_ref(self, *args):
        self.refresh()

    def refresh(self, *args):
        # TEMPORAL WORKAROUND FOR GETTING PLAYLISTS
        if self.browse_ref['uri'] == 'playlists:':
            self.mopidy.playlists.as_list(on_result=self.set_browse_list)
        else:
            self.mopidy.library.browse(uri=self.browse_ref['uri'],
                                       on_result=self.set_browse_list)


    @scheduled
    def browse(self, item):
        self.browse_tree.append(RefUtils.make_reference(item))

    @scheduled
    def back(self):
        if len(self.browse_tree) > 1:
            self.browse_tree.pop()

    @scheduled
    def home(self):
        self.browse_tree = [RefUtils.RefNone]


    def browse_playlists(self):
        self.browse_tree.append(RefUtils.RefPlaylists)