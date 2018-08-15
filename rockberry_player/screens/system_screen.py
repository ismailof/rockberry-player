import subprocess

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

from ..widgets.imageactionbutton import ImageActionButton


class SystemScreen(Screen):

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
            Button:
                text: 'Reset WiFi'
                on_release: root.system_command('rst-wifi')
            Button:
                text: 'Reset Mopidy'
                on_release: root.system_command('rst-mopidy')
            ImageActionButton:
                scope: 'system'
                call: root.system_command
                color_released: [0.0, 0.0, 0.8, 1]
                action: 'reboot'
            ImageActionButton:
                scope: 'system'
                color_released: [0.8, 0.0, 0.0, 1]
                call: root.system_command
                action: 'poweroff'

""")
