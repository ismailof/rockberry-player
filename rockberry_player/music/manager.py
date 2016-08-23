from __future__ import unicode_literals

from kivy.app import App
from kivy.event import EventDispatcher
from kivy.clock import Clock
from kivy.properties import ObjectProperty, BooleanProperty
from kivy.logger import Logger

from mopidy_json_client import MopidyClient

from utils import scheduled, assign_property

from base import MediaController
from refs import RefUtils
from tracks import TrackItem, TrackControl
from images import ImageCache
from playback import PlaybackControl
from options import OptionsControl
from mixer import MixerControl
from queue import QueueControl
from browser import BrowserControl

from debug import debug_function



class MediaManager(EventDispatcher):

    connected = BooleanProperty(False)

    current = ObjectProperty(TrackControl(), rebind=True)
    prev = ObjectProperty(TrackControl(), rebind=True)
    next = ObjectProperty(TrackControl(), rebind=True)
    eot = ObjectProperty(TrackControl(), rebind=True)

    state = ObjectProperty(PlaybackControl(resolution=0.001,
                                           update_interval=0.25),
                           rebind=True)

    mixer = ObjectProperty(MixerControl(), rebind=True)
    options = ObjectProperty(OptionsControl(), rebind=True)

    queue = ObjectProperty(QueueControl(), rebind=True)

    browser = ObjectProperty(BrowserControl(), rebind=True)


    def bind_method(self, method, events):
        if type(events) != list:
            events = [events]

        for event in events:
            self.mopidy.bind_event(event, method)

    def bind_property(self, instance, prop_name, events, **kwargs):
        self.bind_method(assign_property(instance, prop_name, **kwargs), events)

    def __init__(self, **kwargs):
        super(MediaManager, self).__init__(**kwargs)

        self.app = App.get_running_app()
        MediaController.app = self.app

        self.mopidy = MopidyClient(
            ws_url = 'ws://' + self.app.MOPIDY_SERVER + '/mopidy/ws',
            error_handler=self.on_mopidy_error,
            connection_handler=self.on_connection
        )

        self.bind_events()

    @scheduled
    def on_connection(self, connection_state, *args):
        self.connected = connection_state

        if self.connected:
            self.set_interfaces()
            self.init_player_state()

        self.choose_window()

    def choose_window(self, *args):
        if not self.connected:
            screen = 'server'
        #elif self.state.playing:
            #screen = 'playback'
        #elif self.queue.tracklist:
            #screen = 'tracklist'
        #else:
            #screen = 'browse'
        else:
            screen = 'playback'

        self.app.main.switch_to(screen=screen)

    def set_interfaces(self):

        MediaController.mopidy = self.mopidy

        PlaybackControl.set_interface(self.mopidy.playback)
        MixerControl.set_interface(self.mopidy.mixer)
        OptionsControl.set_interface(self.mopidy.tracklist)
        ImageCache.set_interface(self.mopidy.library.get_images)
        QueueControl.set_interface(self.mopidy.tracklist)
        BrowserControl.set_interface(self.mopidy.library)

        self.current.set_refresh_method(self.mopidy.playback.get_current_tl_track)
        self.next.set_refresh_method(self.mopidy.tracklist.next_track)
        self.prev.set_refresh_method(self.mopidy.tracklist.previous_track)
        self.eot.set_refresh_method(self.mopidy.tracklist.eot_track)

    def bind_events(self, *args):

        self.bind_method(self.mixer.update_volume, 'volume_changed')
        self.bind_method(self.mixer.update_mute, 'mute_changed')

        self.bind_property(self.state, 'playback_state', 'playback_state_changed',
                           field='new_state')

        self.bind_method(self.state.update_time_position, ['seeked',
                                                           'track_playback_paused',
                                                           'track_playback_resumed'])

        self.bind_method(self.state.reset_time_position, ['track_playback_started',
                                                          'track_playback_ended'])

        self.bind_method(self.current.set_tl_track, ['track_playback_started',
                                                     'track_playback_paused',
                                                     'track_playback_resumed',
                                                     'track_playback_ended'])

        self.bind_method(self.current.refresh_stream_title, 'track_playback_started')
        self.bind_method(self.current.set_stream_title, 'stream_title_changed')
        self.bind_method(self.current.reset_stream_title, 'track_playback_ended')

        self.current.bind(item=self.refresh_context_info)
        self.state.bind(on_next=self.current.refresh,
                        on_prev=self.current.refresh)

        self.bind_method(self.refresh_context_info, ['options_changed',
                                                     'tracklist_changed'])

        self.bind_method(self.queue.refresh, 'tracklist_changed')
        self.bind_method(self.options.refresh, 'options_changed')

    def init_player_state(self):
        for controller in [self.state,
                           self.mixer,
                           self.current,
                           self.next,
                           self.prev,
                           self.options,
                           self.queue,
                           self.browser]:
            controller.refresh()

    def on_mopidy_error(self, error):
        self.app.main.show_error(error=error)

    def refresh_context_info(self, *args):
        self.next.refresh()
        self.prev.refresh()
        self.eot.refresh()


    # ACTIONS FUNCTIONS. TODO: Move to a proper place

    @scheduled
    def play_uris(self, uris):
        try:
            tl_index = self.mopidy.tracklist.index(timeout=5)
            tltracks = self.mopidy.tracklist.add(
                uris=uris,
                at_position=tl_index + 1,
                timeout=20
            )
            tlid_first = tltracks[0]['tlid']
            self.mopidy.playback.play(tlid=tlid_first)
            self.app.main.switch_to(screen='playback')
        except:
            pass

    @scheduled
    def add_to_tracklist(self, refs=None, uris=None, tunning=False, mixing=False):
        if refs:
            uris = [RefUtils.get_uri(ref) for ref in refs]
        if not uris:
            return

        if tunning:
            self.mopidy.tracklist.clear()

        self.mopidy.tracklist.add(uris=uris)

        if mixing:
            self.mopidy.tracklist.shuffle()

        if tunning:
            self.app.mm.mopidy.playback.play()
            self.app.main.switch_to(screen='playback')
