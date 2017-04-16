from kivy.lang import Builder
from kivy.properties import NumericProperty, ListProperty, AliasProperty
from kivy.uix.widget import Widget


class ProgressRectangle(Widget):
    color = ListProperty([0.8, 0.0, 0.0, 0.25])
    value = NumericProperty(0)
    max = NumericProperty(1)

    def _get_progress(self):
        if not self.max:
            return 0
        return self.value / float(self.max)

    def _set_progress(self, progress):
        self.value = progress * self.max

    progress = AliasProperty(_get_progress, _set_progress, bind=['value', 'max'])


Builder.load_string('''

<ProgressRectangle>:
    canvas.before:
        Color:
            rgba: self.color
        Rectangle:
            pos: self.pos
            size: self.width * self.progress, self.height

''')
