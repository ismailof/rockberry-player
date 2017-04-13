from kivy.lang import Builder
from kivy.properties import NumericProperty, ListProperty, OptionProperty
from kivy.uix.image import Image

from ..music.playback import PlaybackControl
from .holdbutton import HoldButtonBehavior


class ImageHoldButton(HoldButtonBehavior, Image):
    color_released = ListProperty([1, 1, 1, 1])
    color_pressed = ListProperty([0.8, 0.0, 0.0, 1])
    color_progress = ListProperty([0.8, 0.0, 0.0, 0.25])
    border_width = NumericProperty(2)
    hold_progress = NumericProperty(0)

    def on_tick(self, pressed_time, *args):
        self.hold_progress = pressed_time / self.holdtime \
            if self.state == 'down' else 0

    def on_hold(self, *args):
        self.hold_progress = 1

    def on_release(self, *args):
        self.hold_progress = 0


class PlaybackButton(ImageHoldButton):
    action = OptionProperty(PlaybackControl.ACTIONS[0],
                            options=PlaybackControl.ACTIONS)


Builder.load_string('''

<ImageHoldButton>:
    ticktime: 0.1 if self.holdtime else 0
    color: self.color_released if root.state == 'normal' else self.color_pressed
    pos_hint: {'center_x': 0.5, 'center_y': 0.5}
    allow_stretch: True
    always_release: True
    min_state_time: 0.1

    canvas.before:
        Color:
            rgba: self.color_progress
        Rectangle:
            pos: self.pos
            size: self.width * self.hold_progress, self.height
        Color:
            rgba: [1, 1, 1, 0] if root.state == 'normal' else self.color_pressed
        Line:
            rectangle: self.x, self.y, self.width, self.height
            width: self.border_width

<PlaybackButton>:
    source: 'playback_{}.png'.format(self.action)
    on_release: app.mm.state.dispatch('on_' + self.action)

''')
