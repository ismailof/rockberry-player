import collections

from kivy.lang import Builder
from kivy.properties import NumericProperty, ListProperty, OptionProperty, \
    DictProperty, ObjectProperty
from kivy.uix.image import Image

from ..music.playback import PlaybackControl
from .holdbutton import HoldButtonBehavior


class ImageHoldButton(HoldButtonBehavior, Image):
    color_released = ListProperty([1, 1, 1, 1])
    color_pressed = ListProperty([0.8, 0.0, 0.0, 1])
    border_width = NumericProperty(2)


class PlaybackButton(ImageHoldButton):
    action = OptionProperty(PlaybackControl.ACTIONS[0],
                            options=PlaybackControl.ACTIONS)
    call = ObjectProperty(baseclass=collections.Callable)
    args = DictProperty(defaultvalue={}, rebind=True)


Builder.load_string('''

<ImageHoldButton>:
    color: self.color_released if root.state == 'normal' else self.color_pressed
    pos_hint: {'center_x': 0.5, 'center_y': 0.5}
    allow_stretch: True
    always_release: True
    min_state_time: 0.1
    anim_delay: 0.12

    canvas:
        Color:
            rgba: [1, 1, 1, 0] if root.state == 'normal' else self.color_pressed
        Line:
            rectangle: self.x, self.y, self.width, self.height
            width: self.border_width

<PlaybackButton>:
    source: 'playback_{}.png'.format(self.action)
    args: {'event_type': 'on_' + self.action}
    on_release: self.call(**self.args)

''')
