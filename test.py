#!/usr/bin/python
import kivy
kivy.require('1.9.2')

import time
    
from kivy.base import runTouchApp
from kivy.lang import Builder
from kivy.properties import ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

from kivy.clock import triggered


class TestWidget(BoxLayout):

    def __init__(self, **kwargs):
        super(TestWidget, self).__init__(**kwargs)
        self.label = Label(font_size=60)
        self.add_widget(self.label)
        self.update_label()
    
    @triggered(3, interval=True)
    def update_label(self, *args):
        self.label.text = time.strftime('%d-%b %H:%M:%S', time.localtime())

if __name__ == '__main__':
    print time.strftime('%H%M%S', time.localtime())
    runTouchApp(widget=TestWidget())

# Builder.load_string("""

# <TestWidget>:
    # Label:
        # text: time.strtime('%HMMSS', time.localtime())

# """)
