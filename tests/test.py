#!/usr/bin/python
if __name__ == '__main__':
    import kivy
    kivy.require('1.9.1')

from kivy.base import runTouchApp
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import AsyncImage
from kivy.properties import ListProperty, NumericProperty

from tracklist_screen import TrackListScreen

import json

Builder.load_string("""

<TestWidget>:
    orientation: 'vertical'
    AsyncImage:
        source: '/home/pi/bunbury.mp3'
    AsyncImage:
        source: '/home/pi/bunbury.jpg'
    AsyncImage:
        source: '/home/pi/nada.jpg'
""")


class TestWidget(BoxLayout):
    pass
#    tracklist = ListProperty()
#    tlid = NumericProperty(10399)

#    def __init__(self, **kwargs):
#        super(TestWidget, self).__init__(**kwargs)
#
#        with open('results/result_tracklist.json') as json_file:
#            tracklist = json.load(json_file)
#
#        self.tracklist = tracklist


if __name__ == '__main__':
   runTouchApp(widget=TestWidget())
