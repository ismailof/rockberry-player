#!/usr/bin/python
import os
import kivy
kivy.require('1.9.2')
from kivy.app import App

from screens import RockberryMainScreen
from music import MediaManager

#import logging
#logger = logging.getLogger(__name__)
#logger.addHandler(logging.StreamHandler)
#logger.setLevel(logging.DEBUG)
#LOGFILE = os.path.abspath(fullpath + '/../rockberry-player.log')
#logger.addHandler(logging.FileHandler(self.LOGFILE))

class RockberryPlayerApp(App):

    # TODO: Store this into config fie
    MOPIDY_SERVER = 'localhost:6680'
    BASE_FOLDER = os.path.abspath(os.path.dirname(__file__))

    def build(self):
        self.mm = MediaManager()
        self.main = RockberryMainScreen()

        self.main.switch_to(screen='server')

        return self.main


if __name__ == '__main__':
    RockberryPlayerApp().run()
