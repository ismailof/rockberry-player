from kivy.uix.slider import Slider

from ..gpio.gpiodial import GpioDialBehavior


class GpioSlider(GpioDialBehavior, Slider):

    def __init__(self, *args, **kwargs):
        super(GpioSlider, self).__init__(*args, **kwargs)
        self.register_event_type('on_rotate')

    def on_rotate(self, value):
        self.value += value
        if self.value < self.min:
            self.value = self.min
        if self.value > self.max:
            self.value = self.max
