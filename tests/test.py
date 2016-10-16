#!/usr/bin/python
if __name__ == '__main__':
    import kivy
    kivy.require('1.9.1')

from kivy.base import runTouchApp
from kivy.lang import Builder

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from rockberry_player.widgets import HoldButtonBehavior


class HoldLabel(HoldButtonBehavior, Label):
    pass


class TestWidget(BoxLayout):
    pass


Builder.load_string("""

<TestWidget>:
    orientation: 'vertical'
    HoldLabel:
        holdtime: 2000
        on_press: etiqueta.text = 'on_press'
        on_release: etiqueta.text = 'on_release'
        on_hold: etiqueta.text = 'on_hold'
        on_click: etiqueta.text = 'on_click'
    Label:
        id: etiqueta
""")



if __name__ == '__main__':
   runTouchApp(widget=TestWidget())
