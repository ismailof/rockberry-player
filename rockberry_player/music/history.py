from kivy.clock import mainthread
from kivy.properties import ListProperty

from base import MediaController

from ..utils import triggered


class HistoryControl(MediaController):

    historylist = ListProperty([], errorvalue=[])

    @mainthread
    def update_history(self, history, *args):
        self.historylist = history

    @triggered(0.7)
    def refresh(self, *args):
        if self.interface:
            self.interface.get_history(on_result=self.update_history)

    def reset(self, *args):
        self.historylist = []