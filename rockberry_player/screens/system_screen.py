import subprocess

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen


class SystemScreen(Screen):

    def system_command(self, command):
        subprocess.call(command, shell=True, stderr=subprocess.STDOUT)


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
                on_release: root.system_command('sudo ifdown wlan0; sudo ifup wlan0')
            Button:
                text: 'Reset Mopidy'
                on_release: root.system_command('sudo systemctl restart mopidy')
            Button:
                text: 'Reset'
                on_release: root.system_command('sudo reboot')
            Button:
                text: 'Apagar'
                on_release: root.system_command('sudo shutdown -P now')

""")
