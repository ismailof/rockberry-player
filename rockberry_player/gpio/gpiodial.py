from kivy.properties import NumericProperty
from .gpio import GpioBehavior

class GpioDialBehavior(GpioBehavior):

    gpio_step = NumericProperty(5)

    def __init__(self, *args, **kwargs):
        super(GpioDialBehavior, self).__init__(*args, **kwargs)
        self.register_event_type('on_rotate')
        self.register_event_type('on_press')
        self.register_event_type('on_release')
        self.register_event_type('on_click')
        self.register_event_type('on_hold')

    def on_rotate(self, value):
        pass

    def on_press(self):
        pass

    def on_release(self):
        pass

    def on_click(self):
        pass

    def on_hold(self):
        pass