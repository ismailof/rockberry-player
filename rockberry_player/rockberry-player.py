#!/usr/bin/python
import kivy
import logging
kivy.require('1.9.2')

from kivy.app import App
from kivy.loader import Loader

from main import RockberryMain
from music import MediaManager


logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler)
logger.setLevel(logging.DEBUG)


class RockberryPlayerApp(App):

    #def __init__(self, **kwargs):
        #super(RockberryPlayerApp, self).__init__(**kwargs)
        #self.IMG_FOLDER = self.directory + '/images/'
        #self.mm = MediaManager()
        #self.main = RockberryMain()                

    def build(self):
        self.IMG_FOLDER = self.directory + '/images/'
        self.MOPIDY_SERVER = 'localhost:6680'

        self.mm = MediaManager()
        self.main = RockberryMain()
        self.main.switch_to(screen='playback')

        return self.main


if __name__ == '__main__':
    RockberryPlayerApp().run()
