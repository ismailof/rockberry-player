from __future__ import unicode_literals
import logging

from kivy.event import EventDispatcher
from kivy.clock import Clock
from kivy.properties import ListProperty, ObjectProperty, StringProperty,\
    DictProperty

from kivy.app import App

from mopidy_json_client import MopidyClient

from utils import scheduled, assign_property

from base import MediaController
from refs import RefUtils
from tracks import TrackItem, TrackControl
from images import AlbumCoverRetriever
from playback import PlaybackControl
from options import OptionsControl
from mixer import MixerControl
from queue import QueueControl
from browser import BrowserControl

from debug import debug_function

logger = logging.getLogger(__name__)


class MediaManager(EventDispatcher):

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
            self.mopidy.listener.bind(event, method)

    def bind_property(self, instance, prop_name, events, **kwargs):
        self.bind_method(assign_property(instance, prop_name, **kwargs), events)

    def __init__(self, **kwargs):
        super(MediaManager, self).__init__(**kwargs)

        self.app = App.get_running_app()
        MediaController.app = self.app

        self.mopidy = MopidyClient(server_addr=self.app.MOPIDY_SERVER,
                                   error_handler=self.on_mopidy_error)

        self.bind_events()
        self.on_connect(connection_state=True)

    def on_connect(self, connection_state, *args):
        if connection_state:
            self.set_interfaces()
            self.init_player_state()

    def set_interfaces(self):
        PlaybackControl.interface = self.mopidy.playback
        MixerControl.interface = self.mopidy.mixer
        OptionsControl.interface = self.mopidy.tracklist
        AlbumCoverRetriever.interface = self.mopidy.library
        QueueControl.interface = self.mopidy.tracklist
        BrowserControl.interface = self.mopidy.library

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

        self.bind_method(self.current.set_stream_title, 'stream_title_changed')
        self.bind_method(self.current.reset_stream_title, ['track_playback_started',
                                                           'track_playback_ended'])

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


    # BROWSE FUNCTIONS. TODO: Move to a proper place

    @scheduled
    def play_uris(self, uris):
        tltracks = self.mopidy.tracklist.add(uris=uris, timeout=20)
        try:
            tlid_first = tltracks[0]['tlid']
            self.mopidy.playback.play(tlid=tlid_first)
            self.app.main.switch_to(screen='playback')
        except:
            pass

    @scheduled
    def add_to_tracklist(self, refs=None, uris=None, tunning=False):
        if refs:
            uris = [RefUtils.get_uri(ref) for ref in refs]
        if not uris:
            return

        if tunning:
            self.mopidy.tracklist.clear()

        self.mopidy.tracklist.add(uris=uris)

        if tunning:
            self.app.mm.mopidy.playback.play()
            self.app.main.switch_to(screen='playback')
