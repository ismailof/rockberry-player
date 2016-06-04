from kivy.uix.label import Label
from utils import MopidyRef


class ReferenceLabel(Label):

    references = []
    
    def __init__(self, **kwargs):
        super(ReferenceLabel, self).__init__(**kwargs)
        self.register_event_type('on_item_press')
        
    def new_ref(self, item):
        refid = len(self.references)
        self.references.append(MopidyRef(item))
        return refid
    
    def clear_refs(self):
        self.references[:] = []
    
    def on_ref_press(self, refid):
        try:
            self.dispatch('on_item_press', self.references[int(refid)])
        except:
            # TODO: log something
            pass 
    
    def on_item_press(self, *args):
        pass

    