from threading import Timer
from functools import partial

from kivy.properties import NumericProperty, BooleanProperty
from kivy.uix.behaviors.button import ButtonBehavior
from kivy.uix.button import Button


class HoldButtonBehavior(ButtonBehavior):

    holdsecs = NumericProperty(1)
    pressed = BooleanProperty(False)
    _hold_timer = None

    def __init__(self, *args, **kwargs):
        super(HoldButtonBehavior, self).__init__(*args, **kwargs)
        self.register_event_type('on_hold')
        self.register_event_type('on_click')

    def on_press(self, *args, **kwargs):

        self.pressed = True

        if self.holdsecs:
            self._hold_timer = Timer(self.holdsecs,
                                     self.dispatch_hold)
            self._hold_timer.start()

        super(HoldButtonBehavior, self).on_press(*args, **kwargs)

    def on_release(self, *args, **kwargs):

        if self._hold_timer:
            self._hold_timer.cancel()
            self._hold_timer = None
        if self.pressed:
            self.dispatch('on_click')

        self.pressed = False
        super(HoldButtonBehavior, self).on_release(*args, **kwargs)

    def dispatch_hold(self):
        self.pressed = False
        self.dispatch('on_hold')

    def on_hold(self, *args, **kwargs):
        pass

    def on_click(self, *args, **kwargs):
        pass


class HoldButton(HoldButtonBehavior, Button):
    pass