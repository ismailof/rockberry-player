import subprocess

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

from ..widgets.imageholdbutton import ImageActionButton


class SystemScreen(Screen):

    def system_command(self, command):

        commands = {
            'poweroff': 'shutdown -P now',
            'reboot': 'reboot',
            'rst-mopidy': 'systemctl restart mopidy',
            'rst-wifi': 'ifdown wlan0; sudo ifup wlan0'
        }

        try:
            subprocess.call(['sudo', command[action]], shell=True, stderr=subprocess.STDOUT)
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
                action: 'reboot'
                call: root.system_command
            ImageActionButton:
                scope: 'system'
                action: 'poweroff'
                call: root.system_command

""")
