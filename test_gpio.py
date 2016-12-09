#!/usr/bin/python
import kivy
kivy.require('1.9.2')

from time import sleep

from kivy.base import runTouchApp
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.slider import Slider

from rockberry_player.widgets.gpioslider import GpioSlider
from rockberry_player.gpio import GpioBehavior


class TestWidget(BoxLayout):

    def __init__(self, *args, **kwargs):
        super(TestWidget, self).__init__(*args, **kwargs)
        #self.register_event_type('on_rotate')

        #self.gpio_group = 'volume'

        self.slider1 = GpioSlider(
            gpio_group='tune',
            size_hint_y=0.1,
            min=0,
            max=250
        )

        self.slider2 = GpioSlider(
            gpio_group='volume',
            size_hint_y=0.1,
            min=0,
            max=250
        )

        self.add_widget(self.slider1)
        self.add_widget(self.slider2)

        self.slider2.focus = True

        #print '{0}:{0.focus}'.format(self)
        print '{0}:{0.focus}'.format(self.slider1)
        print '{0}:{0.focus}'.format(self.slider2)

    #def on_rotate(self, value):
        #if value > 0:
            #self.slider2.focus = True
        #else:
            #self.slider1.focus = True


Builder.load_string("""

<TestWidget>:
    orientation: 'vertical'
    padding: 30

<GpioSlider>:
    canvas.after:
        Color:
            rgba: (0,0,1,0.5) if self.focus else (0,0,0,0)
        Line:
            rectangle: self.x, self.y, self.width, self.height
            width: 2
""")


if __name__ == '__main__':
   runTouchApp(widget=TestWidget())



