#!/usr/bin/python

import kivy
kivy.require('1.9.1')

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.properties import NumericProperty, ReferenceListProperty
#from kivy.lang import Builder

class Target(Widget):
    pass

class TSCalibrate(FloatLayout):
    
    toque_x = NumericProperty(0)
    toque_y = NumericProperty(0)
    toque_pos = ReferenceListProperty (toque_x,toque_y)
    
    def __init__(self, **kwargs):        
        super(TSCalibrate, self).__init__(**kwargs)        
        
        for x in range(100, 800, 100):
            for y in range(100, 480, 100):
                self.add_widget(Target(x=x, y=y))
    
    def on_touch_down (self, touch):
        self.toque_pos = touch.pos
    
    def on_touch_move (self, touch):
        self.toque_pos = touch.pos
    

class TS_CalibrateApp(App):
    pass
    
    
if __name__ == '__main__':
    TS_CalibrateApp().run()