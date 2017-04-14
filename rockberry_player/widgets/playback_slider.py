from __future__ import absolute_import, print_function

from kivy.lang import Builder
from kivy.clock import Clock
from kivy.properties import StringProperty, NumericProperty, \
    BooleanProperty, AliasProperty, VariableListProperty, \
    ObjectProperty
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.label import Label

from ..widgets.seekslider import SeekSlider
from ..widgets.holdbutton import HoldButtonBehavior


from ..debug import debug_function


class PlaybackSlider(RelativeLayout):

    # Playback state data
    duration = NumericProperty(None, allownone=True)
    position = NumericProperty(None, allownone=True)
    seekable = BooleanProperty(True)

    # Resolution of the data in seconds. Defaults to 1ms
    resolution = NumericProperty(0.001)
    # Text to display when no time is availabe
    default_text = StringProperty('--:--')
    # Seconds on -Xs and +Xs controls
    shortcut_secs = VariableListProperty(0, length=2)

    available = AliasProperty(
        lambda self: self.position is not None \
            and self.duration is not None,
        None,
        bind=['position', 'duration']
        )

    def __init__(self, **kwargs):
        super(PlaybackSlider, self).__init__(**kwargs)
        self.register_event_type('on_seek')

    def on_seek(self, value):
        pass


class SecondsLabel(HoldButtonBehavior, Label):
    secs = NumericProperty(10)
    show = BooleanProperty(True)


Builder.load_string("""

<SecondsLabel>:
    markup: True
    text: '%+ds' % self.secs
    font_size: 18
    size_hint: (None, None)
    size: (60, 25)
    disabled: False if self.secs and self.show else True
    opacity: 0 if self.disabled else 1
    ticktime: 0.5


<PlaybackSlider>:

    SecondsLabel:
        secs: -root.shortcut_secs[0]
        show: root.seekable and root.available
        halign: 'right'
        pos: (slider.x, slider.top)
        resolution: root.resolution
        on_press: slider.manual_step(self.secs/root.resolution, lock=True)
        on_tick: slider.manual_step(self.secs/root.resolution, lock=True)
        on_release: slider.manual_release()

    SecondsLabel:
        secs: root.shortcut_secs[1]
        show: root.seekable and root.available
        halign: 'left'
        pos: (slider.right - self.width, slider.top)
        resolution: root.resolution
        on_press: slider.manual_step(self.secs/root.resolution, lock=True)
        on_tick: slider.manual_step(self.secs/root.resolution, lock=True)
        on_release: slider.manual_release()

    BoxLayout:
        orientation: 'horizontal'

        Label:
            text: TrackUtils.format_time(slider.value if root.available else root.position) or root.default_text
            halign: 'right'
            size_hint_x: None
            width: 25

        SeekSlider:
            id: slider
            min: 0
            max: root.duration if root.available else 2
            cached_value: root.position if root.available else 1
            disabled: not root.seekable if root.available else True
            constraint: True
            value_track: True if root.available else False
            value_track_color: [0.5, 0, 0, 1]
            value_track_width: 2
            cursor_image: 'slider_knob.png'
            cursor_disabled_image: 'slider_knob.png'
            on_seek: root.dispatch('on_seek', int(args[1]))

        Label:
            text: TrackUtils.format_time(root.duration) or root.default_text
            halign: 'left'
            size_hint_x: None
            width: 25
""")
