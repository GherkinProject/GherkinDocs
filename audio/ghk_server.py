#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

#standards libraries
#audio
import gst

#os
import os

#http server
from SimpleXMLRPCServer import SimpleXMLRPCServer

#config file
import config

class audio_server:
    def __init__(self):
        self.playing = False
        #self.player = gst.Pipeline("player")
        self.player = gst.element_factory_make("playbin2", "player")
        fakesink = gst.element_factory_make("fakesink", "fakesink")
        self.player.set_property("video-sink", fakesink)
        
        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.connect("message", self.on_message)
    
    def load(self, path):
        """Load a song from the absolution or relative path "path" to the gstreamer audio server"""
        print path
        if os.path.isfile(path):
            self.player.set_property("uri", "file://" + path)
        else:
            print "bad file path"

    def play_pause(self):
        """Play or pause the file if loaded, if not, do nothing"""
        if not self.playing:
            self.player.set_state(gst.STATE_PLAYING)
            self.playing = True
        else:
            self.player.set_state(gst.STATE_PAUSED)
            self.playing = False
    
    def stop(self):
        """De-load the file if loaded, compulsory if wanted to load a new file"""
        self.playing = False
        self.player.set_state(gst.STATE_NULL)

    def get_position(self):
        """return (int) the current position in the song ( in second )"""
        return int(self.player.query_position(gst.FORMAT_TIME, None)[0] // 1000000000)

    def get_duration(self):
        """return (int) the total duration of the song ( in second )"""
        return int(self.player.query_duration(gst.FORMAT_TIME, None)[0] // 1000000000)
    
    def on_message(self, bus, message):
        """Print message sent by gstreamer"""
        t = message.type
        if t == gst.MESSAGE_EOS:
            self.player.set_state(gst.STATE_NULL)
        elif t == gst.MESSAGE_ERROR:
            self.player.set_state(gst.STATE_NULL)
            err, debug = message.parse_error()
            print "Error: %s" % err, debug
    
    def is_playing(self):
        """Return the state of the audio player"""
        return self.playing

# Create server
server = SimpleXMLRPCServer(("localhost", config.defaultPort), allow_none=True)
server.register_introspection_functions()
server.register_instance(audio_server())

# Run the server's main loop
server.serve_forever()