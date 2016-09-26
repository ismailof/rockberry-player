from kivy.lang import Builder
from kivy.logger import Logger
from kivy.properties import AliasProperty
from kivy.uix.label import Label

from music.refs import RefUtils


class ReferenceLabel(Label):

    def set_item(self, item):
        self.clear_refs()
        self.new_ref(item)
        self.text = '[ref=0]' + RefUtils.get_title(self.references[0]) + '[/ref]'

    def get_item_reference(self):
        if not self.references:
            return None
        else:
            return self.references[0]

    item = AliasProperty(get_item_reference, set_item)

    def __init__(self, **kwargs):
        super(ReferenceLabel, self).__init__(**kwargs)
        self.references = []
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


Builder.load_string("""

<ReferenceLabel>
    markup: True
    halign: 'center'
    valign: 'middle'
    split_str: ' '
    text_size: self.size
    on_item_press: app.mm.browser.browse(args[1])

""")