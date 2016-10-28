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

    @scheduled
    def set_reflist_from_tracks(self, tracks, *args):
        self.reflist = [RefUtils.make_reference(track)
                        for track in tracks]

    def on_browse_ref(self, *args):
        self.refresh()

    def refresh(self, *args):
        self.reflist = []
        browse_uri = RefUtils.get_uri(self.browse_ref)
        # TEMPORAL WORKAROUND FOR GETTING ALL THE PLAYLISTS
        if browse_uri == 'playlists:':
            self.mopidy.playlists.as_list(
                on_result=self.set_reflist)
        # Browsing means different depending on ref type
        elif RefUtils.get_type(self.browse_ref) == 'playlist':
            self.mopidy.playlists.get_items(
                uri=browse_uri,
                on_result=self.set_reflist)
        elif RefUtils.get_type(self.browse_ref) == 'artist':
            self.mopidy.library.lookup(
                uri=browse_uri,
                on_result=self.set_reflist_from_tracks)
        else:
            self.mopidy.library.browse(
                uri=browse_uri,
                on_result=self.set_reflist)

    def server_refresh(self, *args):
        if self.browse_ref['uri'] == 'playlists:':
            self.mopidy.playlists.refresh()
        else:
            self.mopidy.library.refresh(uri=self.browse_ref['uri'])
        self.refresh()

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
