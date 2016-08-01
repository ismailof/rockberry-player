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

    def refresh(self, *args):
        @scheduled
        def set_browse_list(result, *args):
            self.browse_list = result

        self.interface.browse(uri=self.browse_ref['uri'], 
                              on_result=set_browse_list)

    def on_browse_ref(self, *args):        
        self.refresh()

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
        
