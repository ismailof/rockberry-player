from kivy.lang import Builder
from kivy.properties import NumericProperty, ListProperty, AliasProperty
from kivy.uix.widget import Widget


class ProgressRectangle(Widget):
    progress_color = ListProperty([0.8, 0.0, 0.0, 0.25])
    progress_value = NumericProperty(0)
    progress_min = NumericProperty(0)
    progress_max = NumericProperty(1)

    def _get_progress(self):
        if not self.progress_max:
            return 0
        return ((self.progress_value - self.progress_min)
                    / float(self.progress_max))

    progress = AliasProperty(_get_progress, None,
                             bind=['progress_value', 'progress_min', 'progress_max'])


Builder.load_string('''

<ProgressRectangle>:
    canvas.before:
        Color:
            rgba: self.progress_color
        Rectangle:
            pos: self.pos
            size: self.width * self.progress, self.height

''')