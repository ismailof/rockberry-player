from __future__ import unicode_literals
import random

from kivy.app import App
from kivy.event import EventDispatcher
from kivy.clock import Clock
from kivy.properties import ObjectProperty, BooleanProperty
from kivy.logger import Logger

from mopidy_json_client import MopidyClient

from utils import scheduled, delayed, assign_property

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

    current = ObjectProperty(
        TrackControl(refresh_method='playback.get_current_tl_track',
                     refresh_args={}),
        rebind=True)

    prev = ObjectProperty(
        TrackControl(refresh_method='tracklist.previous_track',
                     refresh_args={'tl_track':None}),
        rebind=True)
    next = ObjectProperty(
        TrackControl(refresh_method='tracklist.next_track',
                     refresh_args={'tl_track':None}),
        rebind=True)
    eot = ObjectProperty(
        TrackControl(refresh_method='tracklist.eot_track',
                     refresh_args={'tl_track':None}),
        rebind=True)

    state = ObjectProperty(
        PlaybackControl(resolution=0.001, update_interval=0.25),
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
            version='2.0.1',
            error_handler=self.on_mopidy_error,
            connection_handler=self.on_connection,
        )

        # self.mopidy.debug_client(True)
        self.bind_events()

    @scheduled
    def on_connection(self, connection_state, *args):
        self.connected = connection_state

        if self.connected:
            self.set_interfaces()
            self.init_player_state()
        else:
            self.reset_player_state()

        Clock.schedule_once(self.choose_window, 5)

    def choose_window(self, *args, **kwargs):
        if not self.connected:
            screen = 'server'
        elif self.state.playback_state == 'playing':
            screen = 'playback'
        elif self.queue.tracklist:
            screen = 'tracklist'
        else:
            screen = 'browse'

        self.app.main.switch_to(screen=screen)

    def set_interfaces(self):
        # Set mopidy accesible to every MediaController subclass
        MediaController.set_server(self.mopidy)

        PlaybackControl.set_interface(self.mopidy.playback)
        MixerControl.set_interface(self.mopidy.mixer)
        OptionsControl.set_interface(self.mopidy.tracklist)
        ImageCache.set_interface(self.mopidy.library.get_images)
        QueueControl.set_interface(self.mopidy.tracklist)
        BrowserControl.set_interface(self.mopidy.library)

    def bind_events(self, *args):

        self.bind_method(self.mixer.update_volume, 'volume_changed')
        self.bind_method(self.mixer.update_mute, 'mute_changed')

        self.bind_property(self.state, 'playback_state', 'playback_state_changed',
                           field='new_state')

        self.bind_method(self.state.set_time_position, 'seeked')

        self.bind_method(self.track_playback_started, 'track_playback_started')
        self.bind_method(self.track_playback_ended, 'track_playback_ended')
        self.bind_method(self.track_playback_paused_or_resumed, ['track_playback_paused',
                                                                 'track_playback_resumed'])

        self.current.bind(item=self.refresh_context_info)
        self.state.bind(on_next=self.current.refresh,
                        on_prev=self.current.refresh)

        self.bind_method(self.state.set_stream_title, 'stream_title_changed')

        self.bind_method(self.refresh_context_info, ['options_changed',
                                                     'tracklist_changed'])

        self.bind_method(self.queue.refresh, 'tracklist_changed')
        self.bind_method(self.options.refresh, 'options_changed')

        self.check_playback_end = Clock.create_trigger(self.refresh_main_info, 1)

    def init_player_state(self):
        for controller in (self.state,
                           self.mixer,
                           self.current,
                           self.next,
                           self.prev,
                           self.options,
                           self.queue,
                           self.browser):
            controller.refresh()

    def reset_player_state(self):
        for controller in (self.state,
                           self.mixer,
                           self.current,
                           self.next,
                           self.prev,
                           self.options,
                           self.queue,
                           self.browser):
            controller.reset()

    def on_mopidy_error(self, error):
        self.app.main.show_error(error=error)

    def refresh_main_info(self, *args):
        for controller in (self.state,
                           self.current):
            controller.refresh()

    def refresh_context_info(self, *args):
        for trackitem in (self.next,
                          self.prev,
                          self.eot):
            trackitem.refresh()

    # Track playback events

    @scheduled
    def track_playback_started(self, tl_track):
        self.check_playback_end.cancel()
        self.state.set_time_position(0)
        self.current.set_tl_track(tl_track)

    @scheduled
    def track_playback_ended(self, time_position, tl_track):
        self.state.set_time_position(0)
        self.state.set_stream_title(None)
        self.check_playback_end()

    @scheduled
    def track_playback_paused_or_resumed(self, time_position, tl_track):
        self.state.set_time_position(time_position)
        self.current.set_tl_track(tl_track)


    # TODO: Move to a proper place (queue)
    # TODO: The two actions are quite the same. Join.

    @scheduled
    def play_uris(self, uris=None, refs=None):

        if refs:
            uris = [RefUtils.get_uri(ref) for ref in refs
                    if RefUtils.get_type(ref)=='track']
        if not uris:
            return

        try:
            tl_index = self.mopidy.tracklist.index(timeout=5) or 0
            tltracks = self.mopidy.tracklist.add(
                uris=uris,
                at_position=tl_index,  # play just before current track
                timeout=20
            )
            tlid_first = tltracks[0]['tlid']
            self.mopidy.playback.play(tlid=tlid_first)
            self.app.main.switch_to(screen='playback')
        except:
            pass

    @scheduled
    def add_to_tracklist(self,
                         refs=None, uris=None,
                         tune_id=None,
                         ):
        if refs:
            uris = [RefUtils.get_uri(ref) for ref in refs
                    if RefUtils.get_type(ref)=='track']
        if not uris:
            return

        # Select tune_id as first and shuffle if aplicable
        first_uri = [uris.pop(tune_id)] if tune_id is not None else []
        if self.queue.shuffle_mode:
            random.shuffle(uris)
        uris = first_uri + uris

        if tune_id is not None:
            self.mopidy.tracklist.clear()

        self.mopidy.tracklist.add(uris=uris)

        if tune_id is not None:
            self.app.mm.mopidy.playback.play()
            self.app.main.switch_to(screen='playback')
