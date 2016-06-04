#!/usr/bin/python
import kivy
import logging
kivy.require('1.9.2')

from kivy.app import App
from kivy.loader import Loader

from main import RockberryMain
from music.manager import MediaManager


logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler)
logger.setLevel(logging.DEBUG)


class RockberryPlayerApp(App):

    def __init__(self, **kwargs):
        super(RockberryPlayerApp, self).__init__(**kwargs)
        self.IMG_FOLDER = self.directory + '/images/'
        self.mm = MediaManager()

    def build(self):
        main_widget = RockberryMain()
        main_widget.switch_to(screen='playback')

        return main_widget


if __name__ == '__main__':
    RockberryPlayerApp().run()
