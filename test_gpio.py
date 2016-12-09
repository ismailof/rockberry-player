#!/usr/bin/python
import kivy
kivy.require('1.9.2')

from time import sleep

from kivy.base import runTouchApp
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.slider import Slider

from gpio_controls.inputs import RotaryEncoder, MomentarySwitch, EdgeDetector
from rockberry_player.gpio import GpioInputProvider, GpioBehavior


def register_gpio_controls():
    GpioInputProvider.add_control(
        RotaryEncoder(
            id='volume',
            group='volume',
            pinout=[13, 19],
            inerce=1.2
        )
    )

    GpioInputProvider.add_control(
        MomentarySwitch(
            id='mute',
            group='volume',
            pinout=[26],
            holdtime=2,
        )
    )

    GpioInputProvider.add_control(
        RotaryEncoder(
            id='tune',
            group='tune',
            pinout=[21, 20],
            inerce=1.4
        )
    )

    GpioInputProvider.add_control(
        MomentarySwitch(
            id='ok',
            group='tune',
            pinout=[16],
            holdtime=1.5
        )
    )


class TestWidget(GpioBehavior, BoxLayout):
    
    def __init__(self, *args, **kwargs):        
                
        super(TestWidget, self).__init__(*args, **kwargs)
                
        self.gpio_group = 'volume'
        self.gpio_inputs = [RotaryEncoder]
        
        self.slider1 = GpioSlider(
            gpio_inputs=[RotaryEncoder, MomentarySwitch],
            gpio_group='tune',
            size_hint_y=0.1,
            min=0,
            max=250
        )
        
        self.slider2 = GpioSlider(
            gpio_inputs=[RotaryEncoder, MomentarySwitch],
            gpio_group='tune',
            size_hint_y=0.1,
            min=0,
            max=250
        )
        
        self.add_widget(self.slider1)
        self.add_widget(self.slider2)
        
        self.slider1.set_focus()
        self.set_focus()

    def on_rotate(self, value):
        if value > 0:
            self.slider2.set_focus()
        else:
            self.slider1.set_focus()
        

class GpioSlider(GpioBehavior, Slider):

    def on_rotate(self, value):
        self.value += value
        if self.value < self.min:
            self.value = self.min
        if self.value > self.max:
            self.value = self.max
        

Builder.load_string("""

<TestWidget>:
    orientation: 'vertical'
    padding: 30

<GpioSlider>:
    canvas.after:
        Color:
            rgba: (0,1,0,0.5) if self.focus else (0,0,0,0)
        Line:
            rectangle: self.x, self.y, self.width, self.height
            width: 2
""")


if __name__ == '__main__':
   register_gpio_controls()
   runTouchApp(widget=TestWidget())
 


    