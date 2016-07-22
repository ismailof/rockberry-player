from kivy.app import App
from kivy.event import EventDispatcher
from kivy.properties import ObjectProperty


class MediaController(EventDispatcher):

    app = None
    interface = ObjectProperty(basetype=callable)

    def __init__(self, **kwargs):
        super(MediaController, self).__init__(**kwargs)
        self.app = App.get_running_app()

    def refresh(self, *args):
        pass