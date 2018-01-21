from kivy.core.window import Window
from kivy.event import EventDispatcher
from kivy.input.providers.gpioinput import GPIOEvent
from kivy.uix.slider import Slider
from kivy.properties import StringProperty, NumericProperty

def _constraint(x, min, max):
    return min if x < min else max if x > max else x

class GPIOBehavior(EventDispatcher):

    gpio_group = StringProperty(None, allownone=True)

    def __init__(self, *args, **kwargs):
        super(GPIOBehavior, self).__init__(*args, **kwargs)
        self.register_event_type('on_dial')
        Window.bind(on_motion=self.on_motion)
 
    def on_motion(self, instance, evtype, event):
        if not isinstance(event, GPIOEvent):
            return
        if self.gpio_group is not None and self.gpio_group != event.gpio_group:
            return
        if 'dial' in event.profile:
            self.dispatch('on_dial', event.device, event.dial)
 
    def on_dial(self, device, value):
        pass


class GPIODialSlider(GPIOBehavior, Slider):
    dial_step = NumericProperty(1)
 
    def on_dial(self, device, dial):
        self.value = _constraint(
            self.value + dial * self.dial_step,
            self.min,
            self.max)
