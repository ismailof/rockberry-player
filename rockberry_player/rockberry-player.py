#!/usr/bin/python
import kivy
import logging
kivy.require('1.9.2')

from kivy.app import App

from screens import RockberryMainScreen
from music import MediaManager


logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler)
logger.setLevel(logging.DEBUG)


class RockberryPlayerApp(App):

    def build(self):
        self.IMG_FOLDER = self.directory + '/images/'
        self.MOPIDY_SERVER = 'localhost:6680'

        self.mm = MediaManager()
        self.main = RockberryMainScreen()

        self.main.switch_to('playback' if self.mm.current else 'browse')

        return self.main


if __name__ == '__main__':
    RockberryPlayerApp().run()
