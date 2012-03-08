#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

#playing audio
import audio

#local lib : loading db
from load_db import *

#config file
import config

#config file
import time
from random import randint

#Markov Process
from Markov import Markovienne

#http server
from SimpleXMLRPCServer import SimpleXMLRPCServer

class ai:
    def __init__(self):
        #connection with audio
        self.audio = audio.server()

        #variable
        self.hist = []
        self.playlist = []
        self.songs = dict()
        self.point = 0
        self.mode = config.normal
        self.repeat = False

        #getting library
        (a, b, self.songs) = get_lib()
        
        #markov chain
        self.markovienne = Markovienne(config.dbMarkov)

        try:
            self.markovienne.load_Markov(config.dbMarkov)
        except:
            self.markovienne.create_Markov(self.songs.keys())

#-------------------------------------------------------------------
#-------------------------------------------------------------------
#interface with ui
#-------------------------------------------------------------------
#-------------------------------------------------------------------

#----------------------------
#getters
#----------------------------

    def get_playlist(self):
        return self.playlist

    def get_point(self):
        if len(self.playlist) > 0:
            return self.point
        else:
            return -1
    
    def get_mode(self):
        return self.mode

    def get_repeat(self):
        return self.repeat

    def get_position(self):
        """return (int) the current position in the song ( in second )"""
        return self.audio.get_position()

    def get_duration(self):
        """return (int) the total duration of the song ( in second )"""
        return self.audio.get_duration()
   
    def is_playing(self):
        """Return the state of the audio player"""
        return self.audio.is_playing()
 
#----------------------------
#setters
#----------------------------

    def set_playlist(self, playlist):
        self.playlist = playlist

    def set_point(self, point):
        """Change pointeur of playlist position"""
        assert len(self.playlist) > 0 and point in range(0, len(self.playlist)), "pointeur incorrect"
        
        #update hist and point
        self.point = point
        self.hist.append((self.playlist[self.point], time.time()))
    
#----------------------------
#audio actions
#----------------------------

    def change(self, point):
        """Lauch song pointed"""
        #change pointeur
        self.set_point(point)
       
        #we increase the probabily to go from idSongNow to idSong and decrease the other
        #we do a pruning of the successors of idSongNow
        
        #>>>>>>>>>>>>>>> why try: ? if no previous song played ? ok but 'if' works too...
        #we have to test if the
        try:
            self.markovienne.vote_Markov(self.hist[-2][0], self.hist[-1][0])
            self.markovienne.elagage(self.hist[-2][0], config.epsilon)
        except:
            pass

        self.load()

    def next(self):
        #few things to do if we are in normal mode... just incrementing the pointeur
        if self.mode == config.normal:
            if self.point < len(self.playlist) - 1:
                self.set_point(self.point+1)
                self.load()
                return True
            else:
                self.point = 0
                self.server.stop()
                return False
        else:
            if self.mode == config.random:
                #choosing a random number in the list of possible song
                posSong = randint(0, len(self.songs))
                idSong = self.songs.keys()[posSong] 
            elif self.mode == config.playlist:
                idSong = self.markovienne.choix_Markov(self.playlist[self.point])
            
            #adding the song to the playlist
            self.playlist.append(idSong)
            
            #pointing on the new song
            self.set_point(self.point+1)
            
            #loading
            self.load()

    def prev(self):
        #if we are not at the first element, no problem
        if self.point > 0:
            self.point -= 1
        else:
            self.point = len(self.playlist)-1
            
        self.load()
        
        #erasing the lasts elements in those mode taking into account the user didn't like the music proposed
        if self.mode == config.playlist or self.mode == config.random:
            self.playlist.pop(-1)
            self.update_tracks()
        
    def play_pause(self):
        self.audio.play_pause()

    def stop(self):
        self.audio.stop()

    def random(self):
        if self.mode == config.random:
            self.mode = config.normal
        
        elif self.mode == config.playlist:
            self.mode = random
            self.Markovienne.save_Markov()
        
        else:
            self.mode = random

   
#-------------------------------------------------------------------
#-------------------------------------------------------------------
#internal function and methods
#-------------------------------------------------------------------
#-------------------------------------------------------------------

    def load(self):
        self.stop()
        self.audio.load(self.songs[self.playlist[self.point]]["location"])


# Create server
server = SimpleXMLRPCServer((config.serverName, config.defaultPort), logRequests = False, allow_none=True)
server.register_introspection_functions()
server.register_instance(ai())

# Run the server's main loop
server.serve_forever()
