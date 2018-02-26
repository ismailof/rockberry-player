#!/usr/bin/python
if __name__ == '__main__':
    import kivy
    kivy.require('1.9.2')

from kivy.base import runTouchApp
from kivy.lang import Builder
from kivy.properties import NumericProperty, BooleanProperty

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.layout import RecycleLayoutManagerBehavior

from rockberry_player.widgets.dialrecycleview import DialRecycleView


class TestWidget(BoxLayout):
    pass

class TestRecycleView(DialRecycleView):
    pass

class TestItem(BoxLayout):
    number = NumericProperty(0)


Builder.load_string("""

<TestItem>:
    Label:
        text: 'Item #%02d' % root.number


<TestWidget>:
    orientation: 'horizontal'
    list_size: 500

    BoxLayout:
        orientation: 'vertical'
        Label:
            text: 'Num_Items: %d' % len(testview.data)
        Label:
            text: 'Navigation ID: %s' % testview.nav_id
        Label:
            text: 'Reference: %0.2f' % testview.reftop_id


    TestRecycleView:
        id: testview
        dial_axis: 'y'
        viewclass: 'TestItem'
        data: [{'number': i} for i in range(0, root.list_size)]

""")




if __name__ == '__main__':
   runTouchApp(widget=TestWidget())
