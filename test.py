#!/usr/bin/python
# if __name__ == '__main__':
    # import kivy
    # kivy.require('1.9.2')

# import json
    
# from kivy.base import runTouchApp
# from kivy.lang import Builder
# from kivy.properties import ListProperty
# from kivy.uix.boxlayout import BoxLayout

import time
import json
from rockberry_player.widgets.historyview import format_time_diff

    
# class TestWidget(BoxLayout):

def get_historylist():
    hl = None
    with open('results/result_history1.json') as history_file:
        hl = json.load(history_file)
    return hl


#now = time.time()
now = 1523204380
print 'NOW [%d] %s' % (now, time.strftime('%d-%b %H:%M', time.localtime(now)))
    
for milisec, ref in get_historylist():
    ts = milisec / 1000
    print '[({0}) {1}] {2} {3}'.format(ts,
        time.strftime('%d-%b %H:%M', time.localtime(ts)),
        format_time_diff(ts, now),
        ref['name'])
    
# if __name__ == '__main__':
   # runTouchApp(widget=TestWidget())

   
# Builder.load_string("""

# <TestWidget>:
    # HistoryView:
        # historylist: root.get_historylist()

# """)