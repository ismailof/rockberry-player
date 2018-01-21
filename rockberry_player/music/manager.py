from __future__ import unicode_literals, absolute_import, print_function
import random

from kivy.app import App
from kivy.event import EventDispatcher
from kivy.clock import Clock, mainthread
from kivy.properties import ObjectProperty, BooleanProperty
from kivy.logger import Logger

from mopidy_json_client import MopidyClient

from ..utils import delayed

from .base import MediaController
from .refs import RefUtils
from .tracks import TrackControl
from .playback import PlaybackControl
from .options import OptionsControl
from .mixer import MixerControl
from .queue import QueueControl
from .browser import BrowserControl


class MediaManager(EventDispatcher):

    connected = BooleanProperty(False)

    current = ObjectProperty(
        TrackControl(refresh_method='playback.get_current_tl_track',
                     refresh_args={}),
        rebind=True)

    prev = ObjectProperty(
        TrackControl(refresh_method='tracklist.previous_track',
                     refresh_args={'tl_track': None}),
        rebind=True)
    next = ObjectProperty(
        TrackControl(refresh_method='tracklist.next_track',
                     refresh_args={'tl_track': None}),
        rebind=True)
    eot = ObjectProperty(
        TrackControl(refresh_method='tracklist.eot_track',
                     refresh_args={'tl_track': None}),
        rebind=True)

    state = ObjectProperty(PlaybackControl(), rebind=True)

    mixer = ObjectProperty(MixerControl(), rebind=True)
    options = ObjectProperty(OptionsControl(), rebind=True)

    queue = ObjectProperty(QueueControl(), rebind=True)

    browser = ObjectProperty(BrowserControl(), rebind=True)

    def __init__(self, **kwargs):
        super(MediaManager, self).__init__(**kwargs)

        self.app = App.get_running_app()
        MediaController.app = self.app

        self.mopidy = MopidyClient(
            ws_url='ws://' + self.app.MOPIDY_SERVER + '/mopidy/ws',
            version='2.0.1',
            error_handler=self.on_mopidy_error,
            connection_handler=self.on_connection,
        )
#        self.mopidy.debug_client(True)

        self.controllers = (
            self.state, self.mixer,
            self.current, self.next, self.prev,
            self.options, self.queue, self.browser)

        self.bind_events()

    @mainthread
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
        elif self.state.playback_state != 'stopped':
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
        QueueControl.set_interface(self.mopidy.tracklist)
        BrowserControl.set_interface(self.mopidy.library)

    def bind_events(self, *args):

        # Clear previous events to avoid duplicity
        self.mopidy.listener.clear()

        # Mixer events
        self.mopidy.bind_event('volume_changed', self.mixer.update_volume)
        self.mopidy.bind_event('mute_changed', self.mixer.update_mute)

        # State events
        self.mopidy.bind_event('playback_state_changed', self.state.set_playback_state)
        self.mopidy.bind_event('seeked', self.state.set_time_position)
        self.mopidy.bind_event('stream_title_changed', self.state.set_stream_title)

        # Playback events
        self.mopidy.bind_event('track_playback_started', self.track_playback_started)
        self.mopidy.bind_event('track_playback_ended', self.track_playback_ended)
        self.mopidy.bind_event('track_playback_paused', self.track_playback_paused_or_resumed)
        self.mopidy.bind_event('track_playback_resumed', self.track_playback_paused_or_resumed)

        # Current track updates
        self.current.bind(item=self.refresh_context_info)
        self.state.bind(on_next=self.current.refresh,
                        on_prev=self.current.refresh)

        # Context update: Options and Tracklist
        self.mopidy.bind_event('options_changed', self.options.refresh)
        self.mopidy.bind_event('tracklist_changed', self.queue.refresh)
        self.mopidy.bind_event('options_changed', self.refresh_context_info)
        self.mopidy.bind_event('tracklist_changed', self.refresh_context_info)

        # Trigger to update status on playback end
        self.check_playback_end = Clock.create_trigger(self.refresh_main_info, 1)

    def init_player_state(self):
        for controller in self.controllers:
            controller.refresh()

    def reset_player_state(self):
        for controller in self.controllers:
            controller.reset()

    def on_mopidy_error(self, error):
        self.app.main.show_error(error=error)

    def refresh_main_info(self, *args):
        for controller in (self.state,
                           self.current):
            controller.refresh()

    @delayed(1)
    def refresh_context_info(self, *args):
        for trackitem in (self.next,
                          self.prev,
                          self.eot):
            trackitem.refresh()

    # Track playback events

    @mainthread
    def track_playback_started(self, tl_track):
        self.check_playback_end.cancel()
        self.state.set_time_position(0)
        self.current.set_tl_track(tl_track)

    @mainthread
    def track_playback_ended(self, time_position, tl_track):
        self.state.set_time_position(0)
        self.state.set_stream_title(None)
        self.check_playback_end()

    @mainthread
    def track_playback_paused_or_resumed(self, time_position, tl_track):
        self.state.set_time_position(time_position)
        self.current.set_tl_track(tl_track)

    # TODO: Move to a proper place (queue)
    # TODO: The two actions are quite the same. Join.

    def play_uris(self, uris=None, refs=None):

        if refs:
            uris = [RefUtils.get_uri(ref) for ref in refs
                    if RefUtils.get_type(ref) == 'track']
        if not uris:
            return

        try:
            tl_index = self.mopidy.tracklist.index(timeout=5) or 0
            tltracks = self.mopidy.tracklist.add(
                uris=uris,
                at_position=tl_index + 1,  # play just before current track
                timeout=20
            )
            tlid_first = tltracks[0]['tlid']
            self.mopidy.playback.play(tlid=tlid_first)
            self.app.main.switch_to(screen='playback')
        except Exception:
            pass

    def add_to_tracklist(self,
                         refs=None, uris=None,
                         tune_id=None,
                         ):
        if refs:
            uris = [RefUtils.get_uri(ref) for ref in refs
                    if RefUtils.get_type(ref) == 'track']
        if not uris:
            return

        # Select tune_id as first and shuffle if aplicable

        if tune_id is not None:
            tune_uri = uris.pop(tune_id)
            self.mopidy.tracklist.clear()
            self.mopidy.tracklist.add(uris=[tune_uri])
            self.mopidy.playback.play()
            self.app.main.switch_to(screen='playback')
        else:
            tune_id = 0

        if self.queue.shuffle_mode:
            random.shuffle(uris)
            tune_id = 0

        self.mopidy.tracklist.add(uris=uris[tune_id:])
        if tune_id:
            self.mopidy.tracklist.add(uris=uris[:tune_id], at_position=0)
