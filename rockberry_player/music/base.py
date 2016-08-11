from kivy.app import App
from kivy.event import EventDispatcher


class MediaController(EventDispatcher):

    app = None
    interface = None
    mopidy = None

    #def __init__(self, **kwargs):
        #super(MediaController, self).__init__(**kwargs)
        #self.app = App.get_running_app()
        #print self, self.app

    def refresh(self, *args):
        pass