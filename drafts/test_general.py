#!/usr/bin/python
if __name__ == '__main__':
    import kivy
    kivy.require('1.9.1')

from kivy import base
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.gridlayout import GridLayout
from kivy.uix.spinner import Spinner

from kivy.properties import NumericProperty

from widgets.iconimage import IconImage
from widgets.playback_slider import PlaybackSlider
from widgets.simpleclock import AnalogClock

from widgets.error_popup import ErrorPopup

#from widgets.pa_levels import PeakMonitor
#from widgets.audiobar import AudioBar
#import thread

from widgets.seekslider import SeekSlider
from widgets.playback_slider import PlaybackSlider


Builder.load_string("""

<TestSlider@BoxLayout>:
    orientation: 'horizontal'

    Slider:
        id: sld_in
        on_value: sld_out.value = sld_pb.position = args[1]
        min: 0
        max: 100

    SeekSlider:
        id: sld_out
        min: 0
        max: 100
        constrain: True
        on_seek: sld_in.value = args[1]

    PlaybackSlider:
        id: sld_pb
        resolution: 1
        duration: 100
        playing: True
        on_seek: sld_in.value = args[1]


<TestAudioLevels@FloatLayout>:
    AudioBar:
        id: audiobar
        value: root.audiolevel
        text_size: self.size


<TestWidget>:
    cols: 2
    rows: 5

    Spinner:
        text: 'turntable'
        values: ('NONE', 'turntable', 'radio', 'microphone', 'bluetooth', 'tv')
        on_text: root.manager.get_screen('playback').ids['device_image'].device = self.text

    Image:
        source: 'atlas://images/flags_32x16/ES'

    BoxLayout:
        id: option_buttons
        #size_hint: (0.6, 0.1)
        #pos_hint: {'right': 1}
        spacing: 5
        padding_x: 10

        CheckBox:
            id: chk_random
            background_checkbox_down: 'atlas://images/options/random_on'
            background_checkbox_normal: 'atlas://images/options/random_off'

        CheckBox:
            id: chk_single
            background_checkbox_down: 'atlas://images/options/single_on'
            background_checkbox_normal: 'atlas://images/options/single_off'

        CheckBox:
            id: chk_repeat
            background_checkbox_down: 'atlas://images/options/repeat_on'
            background_checkbox_normal: 'atlas://images/options/repeat_off'

    AnalogClock:
    
    Widget:
    
    Widget:

    Button:
        text: 'EXIT'
        on_press: app.stop()

""")


#SINK_NAME = 'alsa_output.usb-C-Media_Electronics_Inc._USB_PnP_Sound_Device-00-Device.analog-stereo'
#METER_RATE = 344


class TestWidget(GridLayout):

    #audiolevel = NumericProperty(0)

    def __init__(self, **kwargs):
        super(TestWidget, self).__init__(**kwargs)
        #self.monitor = PeakMonitor(SINK_NAME, METER_RATE)
        #thread.start_new_thread(self.update_levels, ())

    def move_slider(self, *args):
        self.ids['sld_out'].value = self.ids['sld_out'].value + 1

    #def update_levels(self, *args):
        #for sample in self.monitor:
            #self.audiolevel = sample

    def generate_error(self):
        mi_error={'title': 'MockError',
                  'type': 'MockingJayError',
                  'error': 'Vete a dormir',
                  'traceback': 'Vete a cenar, anda que ya te vale tronco n se de que cjnes vas, aunque molen las cncines son las putas doce ya, joder. Me devuelveees de nuevooo a la viddaaaaa\n RESURRECCIOOOOON',
                  }

        ErrorPopup(error=mi_error).open()


if __name__ == '__main__':
    base.runTouchApp(widget=TestWidget())
