from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout


class GlassBoxLayout(BoxLayout):
    pass


Builder.load_string("""

<GlassBoxLayout>:

    orientation: 'vertical'
    padding: 15
    spacing: 10

    canvas.before:
        Color:
            rgba: (0.4, 0.4, 0.4, 0.2)
        Rectangle:
            pos: self.pos
            size: self.size

""")
