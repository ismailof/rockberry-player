import time
from functools import partial

from kivy.clock import Clock
from kivy.properties import NumericProperty, BooleanProperty
from kivy.uix.behaviors.button import ButtonBehavior
from kivy.uix.button import Button


class HoldButtonBehavior(ButtonBehavior):

    holdtime = NumericProperty(0)
    ticktime = NumericProperty(0)

    def __init__(self, *args, **kwargs):
        self._press_start = None

        self.register_event_type('on_click')
        self.register_event_type('on_hold')
        self.register_event_type('on_tick')

        super(HoldButtonBehavior, self).__init__(*args, **kwargs)

    def on_touch_down(self, touch, *args):
        if not self.collide_point(*touch.pos):
            return False

        self._press_start = time.time()

        if self.ticktime:
            Clock.unschedule(self._dispatch_tick)
            Clock.schedule_interval(self._dispatch_tick, self.ticktime)

        if self.holdtime:
            Clock.schedule_once(self._dispatch_hold, self.holdtime)

        return super(HoldButtonBehavior, self).on_touch_down(touch, *args)

    def on_touch_up(self, touch, *args):
        super(HoldButtonBehavior, self).on_touch_up(touch, *args)

        if touch.grab_current is None:
            return False

        Clock.unschedule(self._dispatch_tick)
        Clock.unschedule(self._dispatch_hold)

        if self._press_start is not None:
            self.dispatch('on_click')
        self._press_start = None

        return True

    def _dispatch_hold(self, *args):
        self._press_start = None
        if self.state == 'down':
            self.dispatch('on_hold')

    def _dispatch_tick(self, *args):
        if self.state == 'down' and self._press_start is not None:
            self.dispatch('on_tick', time.time() - self._press_start)
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

