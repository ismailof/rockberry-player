from kivy.uix.label import Label
from kivy.logger import Logger
from music.refs import RefUtils


class ReferenceLabel(Label):

    references = []

    def __init__(self, **kwargs):
        super(ReferenceLabel, self).__init__(**kwargs)
        self.register_event_type('on_item_press')

    def new_ref(self, item):
        refid = len(self.references)
        self.references.append(RefUtils.make_reference(item))
        return refid

    def clear_refs(self):
        self.references[:] = []

    def on_ref_press(self, refid):
        try:
            self.dispatch('on_item_press', self.references[int(refid)])
        except Exception as ex:
            Logger.exception('Exception dispatching on_item_press(%s)\n%r' %
                             (self.references[int(refid)], ex)
                            )

    def on_item_press(self, *args):
        pass
