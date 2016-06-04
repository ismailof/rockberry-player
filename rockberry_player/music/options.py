from kivy.event import EventDispatcher
from kivy.properties import BooleanProperty
from utils import scheduled


class OptionsControl(EventDispatcher):

    interface = None

    random = BooleanProperty(False)
    single = BooleanProperty(False)
    repeat = BooleanProperty(False)
    consume = BooleanProperty(False)

    @scheduled
    def update_tl_options(self, *args, **kwargs):
        self.random = self.interface.get_random(timeout=10) or False
        self.single = self.interface.get_single(timeout=10) or False
        self.repeat = self.interface.get_repeat(timeout=10) or False
        self.consume = self.interface.get_consume(timeout=10) or False

    def refresh(self, *args, **kwargs):
        self.update_tl_options()

    def set_random(self, value):
        self.interface.set_random(value)

    def set_single(self, value):
        self.interface.set_single(value)

    def set_repeat(self, value):
        self.interface.set_repeat(value)

    def set_consume(self, value):
        self.interface.set_consume(value)