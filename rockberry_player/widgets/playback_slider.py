from kivy.lang import Builder
from kivy.properties import StringProperty, NumericProperty, \
    BooleanProperty, AliasProperty, VariableListProperty
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.label import Label

from widgets.seekslider import SeekSlider


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

    def format_time(self, time):
        if time is None:
            return self.default_text

        time_secs = round(time * self.resolution)
        time_st = {'s': time_secs % 60,
                   'm': (time_secs // 60) % 60,
                   'h': time_secs // 3600}

        time_format = '%(h)d:%(m)02d:%(s)02d' if time_st['h'] \
            else '%(m)d:%(s)02d'

        return time_format % time_st

    def on_seek(self, value):
        pass


class SecondsLabel(Label):
    secs = NumericProperty(10)
    show = BooleanProperty(True)


Builder.load_string("""

<SecondsLabel>:
    markup: True
    text: '[ref=%d]%+ds[/ref]' % (self.secs, self.secs)
    size_hint: (None, None)
    size: (60, 25)
    disabled: False if self.secs and self.show else True
    opacity: 0 if self.disabled else 1


<PlaybackSlider>:

    SecondsLabel:
        secs: -root.shortcut_secs[0]
        show: root.seekable and root.available
        halign: 'right'
        pos: (slider.x, slider.top)
        on_ref_press: root.dispatch('on_seek', int(root.position + int(args[1])/root.resolution))

    SecondsLabel:
        secs: root.shortcut_secs[1]
        show: root.seekable and root.available
        halign: 'left'
        pos: (slider.right - self.width, slider.top)
        on_ref_press: root.dispatch('on_seek', int(root.position + int(args[1])/root.resolution))

    BoxLayout:
        orientation: 'horizontal'
        user_touch: slider.user_touch

        Label:
            text: root.format_time(slider.value if root.available else root.position)
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
            on_seek: root.dispatch('on_seek', int(args[1]))

        Label:
            text: root.format_time(root.duration)
            halign: 'left'
            size_hint_x: None
            width: 25
""")
