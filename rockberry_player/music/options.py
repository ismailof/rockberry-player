from kivy.clock import mainthread
from kivy.properties import BooleanProperty
from base import MediaController


class OptionsControl(MediaController):

    random = BooleanProperty(False)
    single = BooleanProperty(False)
    repeat = BooleanProperty(False)
    consume = BooleanProperty(False)

    @mainthread
    def update_tl_options(self, *args, **kwargs):
        self.random = self.interface.get_random(timeout=5) or False
        self.single = self.interface.get_single(timeout=5) or False
        self.repeat = self.interface.get_repeat(timeout=5) or False
        self.consume = self.interface.get_consume(timeout=5) or False

    def refresh(self, *args, **kwargs):
        self.update_tl_options()

    def reset(self, *args, **kwargs):
        self.random = False
        self.single = False
        self.repeat = False
        self.consume = False

    def set_random(self, value):
        self.interface.set_random(value)

    def set_single(self, value):
        self.interface.set_single(value)

    def set_repeat(self, value):
        self.interface.set_repeat(value)

    def set_consume(self, value):
        self.interface.set_consume(value)
