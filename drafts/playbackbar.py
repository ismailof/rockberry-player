from __future__ import absolute_import

from kivy.properties import ListProperty
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout

from ..widgets.imageholdbutton import PlaybackButton


class PlaybackBar(BoxLayout):

    controls = ListProperty()

    def on_controls(self, *args):
        self.clear_widgets()
        for item in self.controls:
            if isinstance(item, (int, float)):
                self.add_widget(Widget(size_hint_x=item))
            elif isinstance(item, basestring):
                self.add_widget(
                    PlaybackButton(action=item)
                )
