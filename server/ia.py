#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

#playing audio
import audio

#http server
from SimpleXMLRPCServer import SimpleXMLRPCServer


class ai:
    def __init__(self):
        self.audio = audio_server()
        self.playlist = []
        self.songs = dict()
        self.point = 0
    
#-------------------------------   
#interface with ui
#-------------------------------
    def next():

    def prev():

    def play_pause():

    def stop(self):
        self.audio.stop()

    def get_position(self):
        """return (int) the current position in the song ( in second )"""
        return self.audio.get_position()

    def get_duration(self):
        """return (int) the total duration of the song ( in second )"""
        return self.audio.get_duration()
   
    def is_playing(self):
        """Return the state of the audio player"""
        return self.audio.is_playing()

#-------------------------------
#internal function and methods
#-------------------------------



# Create server
server = SimpleXMLRPCServer(("localhost", config.defaultPort), logRequests = False, allow_none=True)
server.register_introspection_functions()
server.register_instance(ai())

# Run the server's main loop
server.serve_forever()
