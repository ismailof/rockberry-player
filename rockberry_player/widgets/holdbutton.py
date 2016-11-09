#from threading import Timer
from functools import partial

from kivy.clock import Clock
from kivy.properties import NumericProperty, BooleanProperty
from kivy.uix.behaviors.button import ButtonBehavior
from kivy.uix.button import Button


class HoldButtonBehavior(ButtonBehavior):

    _locked = False
    holdtime = NumericProperty(0)
    ticktime = NumericProperty(0)

    def __init__(self, *args, **kwargs):

        self.register_event_type('on_click')
        self.register_event_type('on_hold')
        self.register_event_type('on_tick')

        super(HoldButtonBehavior, self).__init__(*args, **kwargs)

    def on_press(self, *args, **kwargs):
        self.pressed = True

        if self.holdtime:
            Clock.schedule_once(self._dispatch_hold, self.holdtime)

        if self.ticktime:
            Clock.unschedule(self._dispatch_tick)
            Clock.schedule_interval(self._dispatch_tick, self.ticktime)

        super(HoldButtonBehavior, self).on_press(*args, **kwargs)

    def on_release(self, *args, **kwargs):
        Clock.unschedule(self._dispatch_tick)
        Clock.unschedule(self._dispatch_hold)

        if self.pressed:
            self.dispatch('on_click')
        self.pressed = False

        super(HoldButtonBehavior, self).on_release(*args, **kwargs)

    def _dispatch_hold(self, *args):
        self.pressed = False
        if self.state == 'down':
            self.dispatch('on_hold')

    def _dispatch_tick(self, *args):
        if self.state == 'down':
            self.dispatch('on_tick')
        else:
            Clock.unschedule(self._dispatch_tick)

    def on_click(self, *args, **kwargs):
        pass

    def on_hold(self, *args, **kwargs):
        pass

    def on_tick(self, *args, **kwargs):
        pass


class HoldButton(HoldButtonBehavior, Button):
    pass
