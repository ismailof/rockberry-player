from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty


class InputBar(BoxLayout):
    title = StringProperty('')
    text = StringProperty('')

    def set_text(self, text):
        self.ids['input'].text = text


Builder.load_string("""

<InputBar>:
    size_hint_y: None
    height: 45
    spacing: 4
    text: input.text

    Label:
        size_hint_x: None
        width: 100
        font_size: 23
        bold: True
        text: root.title + ' '
        halign: 'right'
        valign: 'middle'
        text_size: self.size
    TextInput:
        id: input
        valign: 'middle'
        font_size: 23
    Button:
        size_hint_x: None
        width: 60
        text: 'del'
        # u'\u232b'
        on_press: input.text = ''
""")
