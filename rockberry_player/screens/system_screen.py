import subprocess

from kivy.lang import Builder
from kivy.clock import mainthread
from kivy.uix.screenmanager import Screen

from ..widgets.imageactionbutton import ImageActionButton


class SystemScreen(Screen):
    pass


class SystemButton(ImageActionButton):

    @mainthread
    def system_command(self, action=None):

        commands = {
            'poweroff': 'shutdown -P now',
            'reboot': 'reboot',
            'rst-mopidy': 'systemctl restart mopidy',
            'rst-wifi': 'ifdown wlan0; sudo ifup wlan0'
        }

        try:
            subprocess.call(['sudo'] + commands[action].split(),
                            stderr=subprocess.STDOUT)
        except KeyError:
            pass


Builder.load_string("""

<SystemButton>
    holdtime: 2
    on_hold: self.system_command(action=self.action)
    color_pressed: [1, 1, 1, 1]

<SystemScreen>
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: 'Mopidy Server is [b]%s[/b]' % ('Connected' if app.mm.connected else 'Disconnected')
            markup: True
            halign: 'center'
            valign: 'middle'
            text_size: self.size
            font_size: 40
        BoxLayout:
            size_hint_y: 0.3
            SystemButton:
                scope: 'system'
                color_released: [0.0, 0.8, 0.0, 1]
                action: 'rst-mopidy'
            SystemButton:
                scope: 'system'
                color_released: [0.0, 0.0, 0.8, 1]
                action: 'reboot'
            SystemButton:
                scope: 'system'
                color_released: [0.8, 0.0, 0.0, 1]
                action: 'poweroff'

""")
