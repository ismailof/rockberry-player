from kivy.event import EventDispatcher
from kivy.properties import ObjectProperty, ListProperty

from base import MediaController
from refs import RefUtils, RefItem

from utils import scheduled
from debug import debug_function


class BrowserControl (MediaController):

    browse_item = ObjectProperty(RefItem(), rebind=True)
    browse_list = ListProperty([])

    def refresh(self, *args):
        @scheduled
        def set_browse_list(result, *args):
            self.browse_list = result
            self.app.main.switch_to(screen='browse')

        self.interface.browse(uri=self.browse_item.uri, on_result=set_browse_list)

    @scheduled
    def browse(self, reference):        
        self.browse_item.ref = RefUtils.make_reference(reference)
        self.refresh()

