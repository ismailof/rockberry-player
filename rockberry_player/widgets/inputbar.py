from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty


class InputBar(BoxLayout):
    title = StringProperty('')
    text = StringProperty('')


Builder.load_string("""

<InputBar>:
    size_hint_y: None
    height: 45
    spacing: 30
    text: input.text

    Label:
        size_hint_x: 0.2
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
        multiline: False
        write_tab: False
        hint_text: root.title
    ImageButton:
        size_hint_x: 0.1
        source: 'button_x.png'
        on_press: input.text = ''
""")
