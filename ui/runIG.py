# -*- coding: utf-8 -*-
#!/usr/bin/python -d
 
from PyQt4 import QtCore, QtGui
from testIG import Ui_ProjetGherkin
import sys

#local lib : loading db
from load_db import *

#configuration constant
import config

#time for progress bar
import time

#client lib for calling server
import xmlrpclib

def give_time(u):
    if u % 60 < 10:
        return str(u // 60) + " : " + "0" + str(u % 60)
    else:
        return str(u // 60) + " : " + str(u % 60)


class MyForm(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_ProjetGherkin()
        self.ui.setupUi(self)
                
        #connection with the server
        self.server = xmlrpclib.ServerProxy("http://" + config.serverName + ":" + str(config.defaultPort))

        self.point = -1
        self.playlist = []
        #sync with the server at the beginning
        self.sync_server()
        self.iconChange()

        #saving artists and songs displayed
        #getting the lib from the xml file
        if config.serverName == "localhost":
            (self.artists, self.albums, self.songs) = get_lib()
	
        #display artists and albums at launch, if server is playing, display current infos
        
        self.date_display_name = -1
        if self.playlist != []:
            self.update_all()
            self.update_tracks()
            if self.point != -1:
                self.display_name()
                if self.server.is_playing():
                    self.runSong()
        else:
            self.call_all()
            

        #update buttons state
        self.update_repeat()
        self.update_playlist()


        action = QtGui.QAction(self.ui.PlayButton)
        action.setShortcut("Ctrl+P")
#        action.setStatusTip(command.name)
        QtCore.QObject.connect(action, QtCore.SIGNAL('triggered()'), self.call_play_pause )
                            
    
    #signal received, functions called
        QtCore.QObject.connect(self.ui.PlayButton, QtCore.SIGNAL("clicked()"), self.call_play_pause )
        QtCore.QObject.connect(self.ui.AudioTrack, QtCore.SIGNAL("itemActivated(QTreeWidgetItem*,int)"), self.call_change )
        QtCore.QObject.connect(self.ui.Artist, QtCore.SIGNAL("itemClicked(QTreeWidgetItem*,int)"), self.call_albums )
        QtCore.QObject.connect(self.ui.Artist, QtCore.SIGNAL("itemActivated(QTreeWidgetItem*,int)"), self.call_play_albums )
        QtCore.QObject.connect(self.ui.Album, QtCore.SIGNAL("itemClicked(QTreeWidgetItem*,int)"), self.call_tracks )
        QtCore.QObject.connect(self.ui.Album, QtCore.SIGNAL("itemActivated(QTreeWidgetItem*,int)"), self.call_play_tracks)
        QtCore.QObject.connect(self.ui.NextButton, QtCore.SIGNAL("clicked()"), self.call_next)
        QtCore.QObject.connect(self.ui.PreviousButton, QtCore.SIGNAL("clicked()"), self.call_prev)
        QtCore.QObject.connect(self.ui.RandomButton, QtCore.SIGNAL("clicked()"), self.call_random)
        QtCore.QObject.connect(self.ui.RepeatButton,QtCore.SIGNAL("clicked()"), self.call_repeat)
    	QtCore.QObject.connect(self.ui.PlaylistButton,QtCore.SIGNAL("clicked()"), self.call_playlist)
        QtCore.QObject.connect(self.ui.LookingFor, QtCore.SIGNAL("textEdited(QString)"), self.call_search)
#        QtCore.QObject.connect(self.ui.verticalSlider, QtCore.SIGNAL("valueChanged(int)"), self.call_volume )	

#-------------------------------------------------------------------
#-------------------------------------------------------------------
#Sincing with server
#-------------------------------------------------------------------
#-------------------------------------------------------------------

    def sync_server(self):
        """Sincing common variables with the server"""
        self.point = self.server.get_point()
        self.playlist = self.server.get_playlist()
        if self.server.is_loaded():
            self.position = self.server.get_position()
            self.duration = self.server.get_duration()
        self.date_sync = time.time()

    def apply_changes(self):
        """Called after every action that changes the song played (next, prev, change)"""
        try:
            self.song_play.terminate()
        except:
            pass
        self.sync_server()
        self.runSong()
        self.iconChange()
        self.display_name()

#-------------------------------------------------------------------
#-------------------------------------------------------------------
#Interface with signals (clicks)
#-------------------------------------------------------------------
#-------------------------------------------------------------------

    def call_play_pause(self):
        self.server.play_pause()
        self.sync_server()

        #do not forget to work with the other thread
     	if self.server.is_playing():
            self.runSong()
        else:
            self.song_play.terminate()

        #displaying the changes
        self.iconChange()
        self.select()

    def call_change(self, QtWidget, val = 0):
        """When a song is doubleclicked on in the playlist"""
        #we have the id of the song clicked on
        idSong = QtWidget.text(4)
        self.point = 0
        #looking for the selected track in the playlist
        while self.playlist[self.point] != idSong:
            self.point += 1
        
        self.deselect()
        self.server.change(self.point)
        self.apply_changes()
        self.select()

    def call_next(self):
        """The function return True if it has found a new song to play, False either""" 
        self.deselect()
        self.server.next()
        self.apply_changes()
        #perhaps it would be better to update all tracks shown..
        if self.server.get_mode() != config.normal:
            self.ui.addTrack(self.songs[self.playlist[self.point]])
        self.select()

    def call_prev(self):
        """When previous button clicked on, convention : go to the end if at the first"""
        self.deselect()
        self.server.prev()
        self.apply_changes()
        self.select()

    def call_play_albums(self, QtWidget):
        self.deselect()
        self.call_albums(QtWidget)
        self.server.set_point(0)
        self.server.load()
        self.server.play_pause()
        self.apply_changes()
        self.select()

    def call_play_tracks(self, QtWidget):
        self.deselect()
        self.call_tracks(QtWidget)
        self.server.set_point(0)
        self.server.load()
        self.server.play_pause()
        self.apply_changes()
        self.select()
   
    def call_random(self):
        self.server.random()
        self.sync_server()
        self.update_playlist()
        self.update_tracks()

    def call_playlist(self):
        self.server.mode_playlist()
        self.sync_server()
        self.update_playlist()
        self.update_tracks()

    def call_repeat(self):
        self.server.mode_repeat()
        self.update_repeat()

    def call_volume(self, int):
        self.server.set_volume(int * 10 / (self.ui.verticalSlider.maximum()-self.ui.verticalSlider.minimum()))

#-------------------------------------------------------------------
#-------------------------------------------------------------------
#UI methods
#-------------------------------------------------------------------
#-------------------------------------------------------------------

#----------------------------
#modifying constants
#----------------------------

    def set_playlist(self, playlist):
        """update playlist of ui and server"""
        self.server.set_playlist(playlist)
        self.playlist = playlist

    def set_point(self, point):
        """update point of ui and server"""
        self.server.set_point(point)
        self.point = point

#----------------------------
#only display methods
#----------------------------

    def deselect(self):
        """DEselect element in the tree"""
        if self.point != -1 and self.point < len(self.playlist):
            self.ui.AudioTrack.topLevelItem(self.point).setSelected(False)
   
    def select(self):
        """select element in the tree"""    
        if self.point != -1:
            self.ui.AudioTrack.topLevelItem(self.point).setSelected(True)
 
    def display_name(self):
        """display name of song currently playing"""
        if self.date_display_name < self.date_sync:
            try:
                self.ui.LookingForNoTouch.setText(self.songs[self.playlist[self.point]]["title"]+" - "+ self.songs[self.playlist[self.point]]['artist'])
            except:
                self.ui.LookingForNoTouch.setText("Unknown")
            self.date_display_name = time.time()
    
    def call_all(self):
        self.update_all()
         
        #then create a playlist from this set
        self.set_playlist(make_neighbors(self.songs, self.selectedSongs))
        self.set_point(-1)
        self.update_tracks()  

    def update_all(self):
        """display all albums and artists and set point at the beginning"""
        #cleaning the lists
        self.ui.Artist.clear()
        self.ui.Album.clear()
        self.ui.AudioTrack.clear()
         
        #sorting the artists and albums by name for it to be smarter, and display
        artists = self.artists.keys()
        artists.sort()
        self.selectedSongs = set()
        for artist in artists:
            self.ui.addArtist(artist)
            albums = list(self.artists[artist])
            albums.sort()
            for album in albums:
                self.ui.addAlbum(album)
                for idTrack in self.albums[album]:
                    self.selectedSongs.add(idTrack)
        #and update the ui then
        #self.update_albums()
 
    def update_albums(self):
        """display elements of the playlist"""
        self.ui.Album.clear()
        self.ui.AudioTrack.clear()
        
        #add them in the order of the playlist, that is to say, alphabetical order for albums
        self.displayedAlbums = set()
        for idTrack in self.playlist:
            #adding an album if he hasn't already been displayed
            if self.songs[idTrack]["album"] not in self.displayedAlbums:
                self.displayedAlbums.add(self.songs[idTrack]["album"])
                self.ui.addAlbum(self.songs[idTrack]["album"])
            self.ui.addTrack(self.songs[idTrack])

    def update_tracks(self):
        """display elements of the playlist"""
        #removing elements from the album tree
        self.ui.AudioTrack.clear()

        for idTrack in self.playlist:
            self.ui.addTrack(self.songs[idTrack])
   
    def call_albums(self, QtWidget):
        """When an artist is clicked on..."""
        self.selectedArtist = str(QtWidget.text(0))
        self.selectedSongs = set()
        
        #adding all the songs to the set
        for album in self.artists[self.selectedArtist]:
            for idTrack in self.albums[album]:
                self.selectedSongs.add(idTrack)
        
        #then create a playlist from this set
        self.set_playlist(make_neighbors(self.songs, self.selectedSongs))
        self.set_point(-1)
        
        #and update the ui then
        self.update_albums()
  
    def call_tracks(self, QtWidget):
        """When an album is doubleclicked on"""
        self.selectedAlbum = str(QtWidget.text(0))
        self.selectedSongs = self.albums[self.selectedAlbum] 
        
        #making the playlist from the set of songs
        self.set_playlist(make_neighbors(self.songs, self.selectedSongs))
        self.set_point(-1)
    
        self.update_tracks()
   
    def iconChange(self):
        if self.server.is_playing():
            icon2 = QtGui.QIcon()
            icon2.addPixmap(QtGui.QPixmap((config.pauseIcon)), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.ui.PlayButton.setIcon(icon2)
            self.ui.PlayButton.setIconSize(QtCore.QSize(30, 30))
    	else:
            icon2 = QtGui.QIcon()
            icon2.addPixmap(QtGui.QPixmap((config.playIcon)), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    	    self.ui.PlayButton.setIcon(icon2)
            self.ui.PlayButton.setIconSize(QtCore.QSize(30, 30))

    def update_playlist(self):
        if self.server.get_mode() == config.random:
            icon2 = QtGui.QIcon()
            icon2.addPixmap(QtGui.QPixmap((config.randomOnIcon)), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.ui.RandomButton.setIcon(icon2)
            self.ui.RandomButton.setIconSize(QtCore.QSize(30,30))
        else:
            icon2 = QtGui.QIcon()
            icon2.addPixmap(QtGui.QPixmap((config.randomOffIcon)), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.ui.RandomButton.setIcon(icon2)
            self.ui.RandomButton.setIconSize(QtCore.QSize(30,30))
        if self.server.get_mode() == config.playlist:
            icon2 = QtGui.QIcon()
            icon2.addPixmap(QtGui.QPixmap((config.playlistOnIcon)), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.ui.PlaylistButton.setIcon(icon2)
            self.ui.PlaylistButton.setIconSize(QtCore.QSize(30,30))
    	else:
            icon2 = QtGui.QIcon()
            icon2.addPixmap(QtGui.QPixmap((config.playlistOffIcon)), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.ui.PlaylistButton.setIcon(icon2)
            self.ui.PlaylistButton.setIconSize(QtCore.QSize(30,30))

    def update_repeat(self):
        if not self.server.get_repeat():
            icon2 = QtGui.QIcon()
            icon2.addPixmap(QtGui.QPixmap((config.repeatOffIcon)), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.ui.RepeatButton.setIcon(icon2)
            self.ui.RepeatButton.setIconSize(QtCore.QSize(30,30))
        else:
            icon2 = QtGui.QIcon()
            icon2.addPixmap(QtGui.QPixmap((config.repeatOnIcon)), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.ui.RepeatButton.setIcon(icon2)
            self.ui.RepeatButton.setIconSize(QtCore.QSize(30,30))
 
    def runSong(self):
        try:    
            self.song_play.terminate()
        except:
            pass

        self.sync_server()
        self.display_name()
        self.song_play = Song()
        self.ui.SongBar.setMaximum(int(self.duration*100))
        self.ui.SongBar.setMinimum(0)
        self.connect(self.song_play, QtCore.SIGNAL("progressUpdated"), self.updateSongProgress)
        self.song_play.start()
    
    def updateSongProgress(self):
        #we sync to server only at the end and the begining
        if self.position > self.duration - config.anticipateDisplay or self.position < config.anticipateDisplay:
            #sync before the end or at the beginning
            self.deselect()
            self.sync_server()
            self.ui.SongBar.setMaximum(int(self.duration*100))
            self.select()
            self.display_name()
        try:
            self.position += config.dtDisplay 
            self.ui.SongBar.setValue(int(self.position*100))
            self.ui.SongBar.setFormat(give_time(int(self.position)) + " / " + give_time(int(self.duration)))
            if self.server.get_position() == self.server.get_duration() and self.server.get_position() > 0:
                if self.repeat:
                    self.load()
                    self.server.play_pause()
                else:
                    try:
                        self.markovienne.vote_Markov(self.playlist[self.pointeur -1], self.playlist[self.pointeur])
                    except:
                        pass
                    self.call_next()
        except:
            pass
        
        self.ui.SongBar.repaint()

    def call_search(self, QString):
        self.selectSongs = set()
        for artist in self.artists:
            for album in self.artists[artist]:
                for idTrack in self.albums[album]:
                    try:
                        b=self.songs[idTrack]['title'].__contains__(str(QString)) or  self.songs[idTrack]['album'].__contains__(str(QString)) or self.songs[idTrack]['artist'].__contains__(str(QString))
                        if b:
                            self.selectSongs.add(idTrack)
                    except:
                        pass
        #then create a playlist from this set
        self.set_playlist(make_neighbors(self.songs, self.selectSongs))
        self.set_point(0)
        
        #and update the ui then
        self.update_albums()

class Song(QtCore.QThread):
    __pyqtSignals__ = ("progressUpdated")
    def __init__(self):
        QtCore.QThread.__init__(self)
    def run(self):
        while True:
            self.emit(QtCore.SIGNAL("progressUpdated"))
            time.sleep(config.dtDisplay)
     
        

app = QtGui.QApplication(sys.argv)
myapp = MyForm()
myapp.show()
sys.exit(app.exec_())
