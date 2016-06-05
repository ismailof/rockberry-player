
# For browsing popup (TEMPORAL)
from kivy.uix.listview import ListView
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from mopidy_json_client.formatting import format_nice


# Mini test function -> Shows current tracks reported by browse(uri)
def lookup_item(self, item):

    if not item or not item.get('uri'):
        return

    uri = item['uri']
    logger.debug('Browsing on URI: %s', uri)

    info = self.mopidy.library.browse(uri=uri, timeout=40)
    info_tracks = format_nice(info, format='browse').split('\n')

    title = '[%s] %s  (%d items)' % (item['type'], item['name'], len(info_tracks))

    lv = ListView(item_strings=info_tracks, halign='left')
    btn = Button(text='Close', size_hint_y=None, height=50)
    cnt = BoxLayout(orientation='vertical')
    cnt.add_widget(lv)
    cnt.add_widget(btn)

    popup = Popup(title=title,
                    content=cnt,
                    size_hint=(0.8, 0.8),
                    title_size=22,)

    btn.bind(on_press=popup.dismiss)
    popup.open()
