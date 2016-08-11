import time

from kivy.lang import Builder
from kivy.clock import Clock

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.togglebutton import ToggleButton

from functools import partial

from playback_screen import PlaybackScreen
from tracklist_screen import TracklistScreen
from browse_screen import BrowseScreen

from widgets.backgroundimage import BackgroundImage
from widgets.simpleclock import DigitalClock
from widgets.error_popup import ErrorPopup


class RockberryMainScreen(FloatLayout):

    def __init__(self, **kwargs):
        super(RockberryMainScreen, self).__init__(**kwargs)
        self.init_screenbar()

    # Sets the task bar to toggle between screens
    # To be removed in a more polished interface
    def init_screenbar(self, *args):
        for screen in self.ids['screenmanager'].screen_names:
            sc_button = ToggleButton(text=screen,
                                     group='sm',
                                     on_press=partial(self.switch_to, screen=screen),
                                     )

            self.ids['buttonbar'].add_widget(sc_button)

    # Switch the view to the given screen
    def switch_to(self, instance=None, screen=None):
        if self.ids['screenmanager'].has_screen(screen):
            self.ids['screenmanager'].current = screen

    # Makes a new screenshot of the current view
    def do_screenshot(self, *args):
        shotname = '/home/pi/rockberry-player/screenshots/rockberry_%y%m%d_%H%M%S.png'
        self.export_to_png(time.strftime(shotname))

    # Shows a suitable popup when an error occures
    def show_error(self, error, *args):
        popup = ErrorPopup(error=error)
        Clock.schedule_once(popup.open)


Builder.load_string("""
#:import sm kivy.uix.screenmanager

#<Label>
    #font_name: 'DroidSans'

<RockberryMainScreen>

    BackgroundImage:
        id: background
        default: app.IMG_FOLDER + 'bg1.jpg'
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
                
            CheckBox:                
                size_hint_x: None
                width: 40
                active: app.mm.connected

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

            TracklistScreen:
                name: 'tracklist'
                tracklist: app.mm.queue.tracklist
                tlid: app.mm.current.tlid

            #Screen:
                #name: 'test'
                #TestWidget:
                    #manager: screenmanager

            BrowseScreen:
                name: 'browse'

            #Screen:
                #name: 'settings'
                #Settings:
                    #opacity: 0.8

""")
