from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.properties import NumericProperty, ListProperty
from kivy.graphics import *


#class AudioBar (Widget):
class AudioBar (Label):
    value = NumericProperty(0.0)
    max = NumericProperty(127)
    num_bars = NumericProperty(10)
    spacing = NumericProperty(10)
    color = ListProperty([1, 0, 0, 1])
    
    def __init__(self, **kwargs):
        super(AudioBar, self).__init__(**kwargs)        
        self.bind(value=self.update_bar)
        self.halign = 'left'

    def update_bar(self, *args):
        self.text = '%3d %s' % (self.value, '>' * (self.value/3))
        #with self.canvas:
            #Color(self.color)
            #Rectangle(self.x, self.y, self.width * self.value / self.max, self.height)