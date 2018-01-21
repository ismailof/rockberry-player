#!/usr/bin/python
import kivy
kivy.require('1.10.0')

from kivy.base import runTouchApp
from kivy.lang import Builder

from kivy.uix.boxlayout import BoxLayout

from rockberry_player.widgets.gpiowidgets import GPIODialSlider
class TestWidget(BoxLayout):
    pass


Builder.load_string("""

<TestWidget>:
    orientation: 'vertical'
    padding: 30
 
    GPIODialSlider:
        gpio_group: 'volume'
        size_hint_y: 0.1
        min: 0
        max: 100
        value: 50
 
    GPIODialSlider:
        dial_step: -2
        size_hint_y: 0.1
        min: 0
        max: 100
        value: 50
""")


if __name__ == '__main__':
   runTouchApp(widget=TestWidget())
