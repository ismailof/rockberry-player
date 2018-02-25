#!/usr/bin/python
import kivy
kivy.require('1.10.0')

from kivy.base import runTouchApp
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout

from rockberry_player.widgets.dialbehavior import DialSlider


class TestWidget(BoxLayout):
    pass


Builder.load_string("""

<TestWidget>:
    orientation: 'vertical'
    padding: 30

    DialSlider:
        dial_axis: 'x'
        size_hint_y: 0.1
        min: 0
        max: 200
        value: 100

    DialSlider:
        dial_axis: 'y'
        size_hint_y: 0.1
        min: 0
        max: 200
        value: 100

    DialSlider:
        dial_device: 'rot_menu'
        dial_axis: 'x'
        size_hint_y: 0.1
        min: 0
        max: 200
        value: 100

    DialSlider:
        dial_device: 'rot_menu'
        dial_axis: 'y'
        size_hint_y: 0.1
        min: 0
        max: 200
        value: 100

""")


if __name__ == '__main__':
   runTouchApp(widget=TestWidget())
