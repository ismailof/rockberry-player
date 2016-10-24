from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import DictProperty, BooleanProperty
from kivy.clock import Clock


DefaultErrorDict = {'title': 'Error',
                    'type': 'UnknownError',
                    'error': '<No Description>',
                    'traceback': ''}


class ErrorContent(BoxLayout):
    show_tb = BooleanProperty(False)


class ErrorPopup(Popup):
    error = DictProperty(DefaultErrorDict)

    def __init__(self, **kwargs):
        super(ErrorPopup, self).__init__(**kwargs)
        self.content = ErrorContent()
        self.content.bind(show_tb=self.update_height)
        self.content.ids['string'].bind(texture_size=self.update_height)
        self.content.ids['btn_close'].bind(on_press=self.dismiss)
        Clock.schedule_once(self.on_error, 0.1)

    def on_error(self, *args):
        self.title = self.error.get('title', DefaultErrorDict['title'])
        if self.content:
            self.content.ids['string'].text = '%s: %s' % \
                (self.error.get('type', DefaultErrorDict['type']),
                 self.error.get('error', DefaultErrorDict['error']))
            self.content.ids['traceback'].text = \
                self.error.get('traceback', DefaultErrorDict['traceback'])
            self.update_height()

    def update_height(self, *args):
        self.height = self.content.height + 100
        self.center_y = 240


Builder.load_string("""

<ErrorContent>
    orientation: 'vertical'
    padding: 10
    spacing: 15
    size_hint_y: None
    height: string.height + scroll_tb.height + buttons.height + self.spacing * 2
    show_tb: btn_show_tb.state == 'down'

    Label:
        id: string
        font_size: 21
        valign: 'top'
        size_hint_y: None
        height: self.texture_size[1]
        text_size: (self.width, None)

    ScrollView:
        id: scroll_tb
        size_hint: (0.95, None)
        height: min(200, traceback.texture_size[1]) if root.show_tb else 0
        opacity: 1 if root.show_tb else 0
        Label:
            id: traceback
            font_size: 15
            valign: 'bottom'
            pos_hint: {'right': 1}
            text_size: (self.width, None)
            size_hint: (0.95, None)
            height: self.texture_size[1]

    BoxLayout:
        id: buttons
        size_hint: (1, None)
        height: 50
        spacing: 5

        ToggleButton:
            id: btn_show_tb
            text: 'Details'

        Button:
            id: btn_close
            text: 'Close'


<ErrorPopup>
    title_size: 25
    title_color: (1, 0.1, 0.1, 1)
    separator_color: (1, 0.1, 0.1, 1)
    size_hint: (0.7, None)
    auto_dismiss: False

""")
