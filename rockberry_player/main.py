from kivy.lang import Builder
from kivy.core.window import Window
from kivy.clock import Clock

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.togglebutton import ToggleButton

from functools import partial

from playback_screen import PlaybackScreen
from tracklist_screen import TrackListScreen
from widgets.backgroundimage import BackgroundImage
from widgets.simpleclock import DigitalClock


from widgets.playbackarea import PlaybackArea


class RockberryMain(FloatLayout):

    def __init__(self, **kwargs):
        super(RockberryMain, self).__init__(**kwargs)

        for screen in self.ids['screenmanager'].screen_names:
            sc_button = ToggleButton(text=screen,
                                     group='sm',
                                     on_press=partial(self.switch_to, screen=screen),
                                     )

            self.ids['buttonbar'].add_widget(sc_button)

    def switch_to(self, instance=None, screen=None):
        if self.ids['screenmanager'].has_screen(screen):
            self.ids['screenmanager'].current = screen

    def do_screenshot(self, *args):
        Window.screenshot(name='rockberry_%(counter)04d.png')


Builder.load_string("""
#:import sm kivy.uix.screenmanager

#<Label>
    #font_name: 'DroidSans'

<RockberryMain>

    BackgroundImage:
        id: background
        default: app.IMG_FOLDER + 'bg2.jpg'
        uri: app.mm.current.uri
        tint: (0.6, 0.6, 0.6, 1)
        outbounds: 0.1

    BoxLayout:
        orientation: 'vertical'
        padding: 10
        spacing: 10

        BoxLayout
            id: titlebar
            size_hint_y: 0.12

            BoxLayout:
                id: buttonbar
                opacity: 0.6

            Button:
                size_hint_x: 0.2
                opacity: 0.6
                text: 'shot'
                on_press: root.do_screenshot()

            DigitalClock:
                size_hint_x: 0.3
                font_size: 28
                style: 'cool'
                halign: 'right'
                valign: 'middle'

        ScreenManager:
            id: screenmanager
            transition: sm.NoTransition()

            PlaybackScreen:
                name: 'playback'
                #id: playback
                size_hint: (0.95, 0.95)
                pos_hint: {'center': (0.5, 0.5)}

            TrackListScreen:
                name: 'tracklist'
                tracklist: app.mm.tracklist
                tlid: app.mm.current.tlid

            #Screen:
                #name: 'test'
                #TestWidget:
                    #manager: screenmanager

            Screen:
                name: 'browse'
                PlaybackArea:
                    size_hint_x: 0.3

            #Screen:
                #name: 'settings'
                #Settings:
                    #opacity: 0.8

""")

