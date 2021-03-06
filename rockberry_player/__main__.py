#!/usr/bin/python
from __future__ import absolute_import, print_function
__package__ = 'rockberry_player'

import os
import kivy
kivy.require('1.10.0')
from kivy.app import App

from .screens import RockberryMainScreen
from .music import MediaManager

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

    kivy.resources.resource_add_path(os.path.join(BASE_FOLDER, 'images'))

    def build(self):
        self.mm = MediaManager()
        self.main = RockberryMainScreen()

        self.main.switch_to(screen='system')

        return self.main

def main():
    RockberryPlayerApp().run()


if __name__ == '__main__':
    main()
