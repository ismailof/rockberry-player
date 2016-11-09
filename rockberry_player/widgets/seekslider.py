from kivy.properties import NumericProperty, BooleanProperty
from kivy.uix.slider import Slider


class SeekSlider(Slider):

    _locked = False
    constraint = BooleanProperty(False)
    cached_value = NumericProperty(0)

    def __init__(self, **kwargs):
        super(SeekSlider, self).__init__(**kwargs)
        self.register_event_type('on_seek')
        if 'value' in kwargs:
            self.cached_value = self.value
        elif 'cached_value' in kwargs:
            self.value = self.cached_value

    def on_seek(self, *args):
        pass

    def on_cached_value(self, *args):
        if not self._locked:
            self.value = self.cached_value

    def on_touch_down(self, touch, *args):
        if self.collide_point(*touch.pos):
            self.cached_value = self.value
            self._locked = True
        super(SeekSlider, self).on_touch_down(touch, *args)

    def on_touch_move(self, touch, *args):
        if touch.grab_current is not None:
            if self.collide_point(*touch.pos) or not self.constraint:
                self._locked = True
                super(SeekSlider, self).on_touch_move(touch, *args)
            else:
                self._locked = False
                self.value = self.cached_value

    def on_touch_up(self, touch, *args):
        super(SeekSlider, self).on_touch_up(touch, *args)
        if touch.grab_current is not None:
            if self.collide_point(*touch.pos) or not self.constraint:
                self.dispatch('on_seek', self.value)
            else:
                self.value = self.cached_value
            self._locked = False

    def manual_step(self, step, lock=False, *args):
        self.value += step
        if lock:
            self._locked = True
        else:
            self.dispatch('on_seek', self.value)

    def manual_release(self, *args):
        if self._locked:
            self.dispatch('on_seek', self.value)
        self._locked = False
