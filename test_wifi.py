#!/usr/bin/python
import kivy
kivy.require('1.9.2')

from time import sleep
import wifi

from kivy.base import runTouchApp
from kivy.lang import Builder

from kivy.clock import Clock
from kivy.event import EventDispatcher

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView

from kivy.properties import ListProperty, ObjectProperty, NumericProperty, \
    StringProperty


WIFI_INTERFACE = 'wlan1'


class WifiService(object):

    def __init__(self, interface='wlan0', file='/home/pi/rockberry-player/wifi-networks.txt'):
        self._interface = interface
        self._cells = self.scan()
        self._ip = ''
        self.Scheme = wifi.Scheme.for_file(file)

    def scan(self):
        # Scan wifi cells
        cells = wifi.Cell.all(self._interface, sudo=True)
        current = wifi.Cell.active(self._interface)
        # Order by quality
        cells.sort(key=lambda x: self.abs_quality(x.quality),
                   reverse=True)
        # Move active cell first
        for id, cell in enumerate(cells):
            if cell.active:
                cells.insert(0, cells.pop(id))
                break

        return cells

    def new_scheme_for_cell(self, cell):
        password = 'asensio1'

        sch = self.Scheme.for_cell(self._interface,
                                   cell.ssid,
                                   cell,
                                   password)
        return sch

    def connect(self, cell):
        sch = self.Scheme.find(self._interface, name=cell.ssid) \
            or new_scheme_for_cell(cell)

        try:
            conn = sch.activate()
            self._ip = conn.ip_address
        except:
            print 'ERROR AL CONECTARSE'

    @property
    def cells(self):
        return self._cells

    @staticmethod
    def abs_quality(quality, max=100):
        value, top = map(int, quality.split('/'))
        return int(round(value*max/top))

class WifiCellItem(BoxLayout):
    cell = ObjectProperty(wifi.Cell(), rebind=True)
    level = NumericProperty(0)

    def on_cell(self, *args):
        self.level = WifiService.abs_quality(self.cell.quality, 4.49)

class WifiSelector(RecycleView):
    pass

class TestWidget(BoxLayout):

    wlan = WifiService(WIFI_INTERFACE)
    cells = ListProperty([], rebind=True)
    ip = StringProperty('')

    def __init__(self, *args, **kwargs):
        super(TestWidget, self).__init__(*args, **kwargs)
        Clock.schedule_interval(self.do_scan, 5)
        Clock.schedule_once(self.do_scan)

    def do_scan(self, dt=None):
        self.cells = self.wlan.scan()

    def do_connect(self, cell):
        self.wlan.connect(cell)


Builder.load_string("""

<TestWidget>:
    orientation: 'vertical'
    padding: 20

    Label:
        size_hint_y: 0.1
        text: root.ip

    WifiSelector:
        id: wifisel
        data: [{'cell': cell} for cell in root.cells]

    Button:
        size_hint_y: 0.2
        text: 'Scan WiFi Networks'
        on_press: root.do_scan()

<WifiCellItem>:
    Label:
        size_hint_x: 0.3
        fontsize: 25
        text: ('#' * root.level) + ('-' * (4 - root.level))
    Label:
        text: root.cell.encryption_type or '-'
        size_hint_x: 0.3
    Label:
        text_size: self.size
        shorten: True
        shorten_from: 'right'
        valign: 'middle'
        font_size: 22
        text: root.cell.ssid or ''
        bold: root.cell.active
    Label:
        size_hint_x: 0.5
        text: 'Conectado' if root.cell.active else ''
    Button:
        size_hint_x: 0.3
        text: 'Conectar'
        on_press: root.do_connect()

<WifiSelector>:
    viewclass: 'WifiCellItem'
    bar_width: 20
    bar_margin: 2
    scroll_type: ['bars', 'content']
    RecycleBoxLayout:
        orientation: 'vertical'
        size_hint: (None, None)
        width: root.width - root.bar_width - root.bar_margin
        height: self.minimum_height
        default_size_hint: (None, None)
        default_size: (600, 50)

""")


if __name__ == '__main__':
   runTouchApp(widget=TestWidget())
