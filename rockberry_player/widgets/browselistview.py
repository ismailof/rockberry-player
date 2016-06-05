from kivy.uix.listview import ListView
from kivy.adapters.simplelistadapter import SimpleListAdapter
from kivy.properties import ListProperty

from widgets.browselistitem import BrowseListItem


class BrowseListView(ListView):

    reflist = ListProperty()

    def __init__(self, **kwargs):
        super(BrowseListView, self).__init__(**kwargs)
        self.adapter = SimpleListAdapter(data=[],
                                         args_converter=self.my_args_converter,
                                         cls=BrowseListItem)

    def on_reflist(self, *args):
        self.adapter.data = self.reflist

    def my_args_converter(self, row_index, item):
        return {'ref': item}
