from kivy.lang import Builder
from kivy.properties import StringProperty, BooleanProperty, \
    AliasProperty, OptionProperty
from kivy.uix.image import Image
from utils import scheduled


class DeviceImage(Image):

    media = StringProperty(None, allownone=True)
    playing = BooleanProperty(None)

    dev_images = {None: 'transparent.png',
                  'turntable': 'turntable.zip',
                  'radio': 'dev_radio.png',
                  'microphone': 'dev_mic.png',
                  'bluetooth': 'dev_bt.png',
                  'tv': 'dev_film.png',
                  }

    device = OptionProperty(None,
                            options=dev_images.keys(),
                            allownone=True,
                            errorvalue=None)

    dev_types = {'spotify': 'turntable',
                 'local': 'turntable',
                 'dleyna': 'turntable',
                 'soundcloud': 'turntable',
                 'tunein': 'radio',
                 'podcast': 'microphone',
                 'bt': 'bluetooth',
                 'youtube': 'tv'}

    def get_dev_image(self):
        return self.dev_images.get(self.device, self.dev_images[None])

    device_image = AliasProperty(get_dev_image, None, bind=['device'])

    def on_media(self, *args):
        self.device = self.dev_types.get(self.media)

    def on_device(self, *args):
        self.set_anim_delay()

    def on_playing(self, *args):
        self.set_anim_delay()

    def set_anim_delay(self, *args):
        # Required to avoid Clock.max_iteration
        self.anim_delay = 1
        # Set to vinyl speed 33rev/min if playing and turntable
        self.anim_delay = 60.0 / (28 * 33) \
            if self.playing and self.device == 'turntable' else -1


Builder.load_string("""

<DeviceImage>:
    allow_stretch: True
    source: app.IMG_FOLDER + root.device_image

""")
