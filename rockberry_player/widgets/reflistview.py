from kivy.lang import Builder
from kivy.properties import ListProperty

from ..widgets.dialrecycleview import DialRecycleView
from ..widgets.imageactionbutton import ImageActionButton
from ..widgets.baserefitem import BaseRefListItem, RefItemImage

from ..music.refs import RefItem


class RefListView(DialRecycleView):

    reflist = ListProperty()

    def on_reflist(self, *args):
        self.data = [{'ref': ref,
                      'index': index}
                     for index, ref in enumerate(self.reflist)]
        self.nav_id = 0


Builder.load_string("""

<RefListView>:
    viewclass: 'RefListItem'
    item_height: 56


<RefListItem@BaseRefListItem>:
    size_hint_y: None
    height: 70
    padding: 2
    spacing: 10

    RefItemImage:
        ref: root.ref
        size_hint_x: None
        width: self.height
        iconsize: 24

    Label:
        text: root.title
        halign: 'left'
        valign: 'top'
        text_size: self.size
        font_size: 20
        bold: (root.reftype != 'track')

    ImageActionButton:
        size_hint: 0.15, 0.5
        opacity: 0.7
        source: root.action_imgsrc
        holdtime: 2.5
        on_click: app.mm.play_uris(uris=[root.uri]) if root.action == 'play' else app.mm.browser.browse(root.ref)
        on_hold: app.mm.add_to_tracklist(refs=app.mm.browser.reflist, tune_id=root.index) if root.action == 'play' else app.mm.browser.browse(root.ref)

""")
