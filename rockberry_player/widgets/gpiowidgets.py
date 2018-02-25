from kivy.core.window import Window
from kivy.event import EventDispatcher
from kivy.input.providers.gpioinput import GPIOEvent, AXIS_COORDS
from kivy.uix.slider import Slider
from kivy.properties import NumericProperty, OptionProperty
from kivy.logger import Logger


class DialBehavior(EventDispatcher):

    dial_axis = OptionProperty('x', options=AXIS_COORDS.values())
    dial_step = NumericProperty(1)

    def __init__(self, *args, **kwargs):
        super(DialBehavior, self).__init__(*args, **kwargs)
        self.register_event_type('on_dial')
        Window.bind(on_motion=self.on_motion)

    def on_motion(self, instance, evtype, event):
        if not isinstance(event, GPIOEvent):
            return False

        Logger.trace('%s: on_motion: evtype=%r event=%r' %
            (self.__class__.__name__, evtype, event))

        if (not 'dial' in event.profile
                or not self.dial_axis in event.push_attrs):
            return False

        dial_value = getattr(event, self.dial_axis) * self.dial_step
        Logger.debug('DialBehavior: on_motion: dispatching on_dial(axis=%s, value=%d)' %
            (self.dial_axis, dial_value))
        self.dispatch('on_dial', dial_value)

        return False

    def on_dial(self, value):
        pass

    @staticmethod
    def constraint(x, min, max):
        return min if x < min else max if x > max else x


class DialSlider(DialBehavior, Slider):

    def on_dial(self, dial):
        self.value = self.constraint(
            self.value + dial,
            self.min,
            self.max)
