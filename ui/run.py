# -*- coding: utf-8 -*-
 
from PyQt4 import QtCore, QtGui
from display import Ui_ProjetGherkin
from dbbrowser import Browser_Window

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
        self.Browser = Browser_Window()
        #self.ui.AudioTrack.mousePressEvent = mousePressEvent        
 
        #connection with the server
        self.server = xmlrpclib.ServerProxy("http://" + config.serverName + ":" + str(config.defaultPort))

        #launching not in fetchmode
        self.fetch = False
        self.right = False 

        #var linked with the server
        self.point = -1
        self.playlist = []

        #sync with the server at the beginning
        self.sync_server()
        self.iconChange()
        
        #saving artists and songs displayed
        #getting the lib from the xml file
        if config.serverName == "localhost":
            (self.artists, self.albums, self.songs) = get_lib()
        else:
            #downloading db from server
            self.get_db()
            (self.artists, self.albums, self.songs) = get_lib(dbFile = config.defaultDbFileImported)


        #display artists and albums at launch, if server is playing, display current infos
        self.date_display_name = -1
        if self.playlist != []:
            #displaying playlist
            self.fetch = False
            self.selectedSongs = self.playlist
            self.display_all()
            if self.point != -1:
                self.display_name()
                if self.server.is_playing():
                    self.run_stream()
        else:
            #fetching tracks
            self.fetch = True
            self.display_all()
           
        #update buttons state
        self.display_fetch() 
        self.display_repeat()
        self.display_playlist()
        
        if self.server.is_playing():
            self.run_stream()

        #TODO : Shortcuts
        action = QtGui.QAction(self.ui.PlayButton)
        action.setShortcut("Ctrl+P")
        #action.setStatusTip(command.name)
        QtCore.QObject.connect(action, QtCore.SIGNAL('triggered()'), self.call_play_pause )
        
        #signal received, functions called

        # Menu

        QtCore.QObject.connect(self.ui.actionImporter_Dossier, QtCore.SIGNAL("triggered()"), self.open_browser)
        
        #By song
        QtCore.QObject.connect(self.ui.AudioTrack, QtCore.SIGNAL("itemClicked(QTreeWidgetItem*,int)"), self.call_track )
        QtCore.QObject.connect(self.ui.AudioTrack, QtCore.SIGNAL("itemActivated(QTreeWidgetItem*,int)"), self.call_change )
        QtCore.QObject.connect(self.ui.AudioTrack, QtCore.SIGNAL("customContextMenuRequested (const QPoint&)"), self.call_right )
        #By album
        QtCore.QObject.connect(self.ui.Album, QtCore.SIGNAL("itemClicked(QTreeWidgetItem*,int)"), self.call_tracks_before )
        QtCore.QObject.connect(self.ui.Album, QtCore.SIGNAL("itemActivated(QTreeWidgetItem*,int)"), self.call_play_tracks)
        QtCore.QObject.connect(self.ui.Album, QtCore.SIGNAL("customContextMenuRequested (const QPoint&)"), self.call_right )
        QtCore.QObject.connect(self.ui.Album.header(), QtCore.SIGNAL("sectionClicked(int)"), self.call_all_albums )
        #By artist
        QtCore.QObject.connect(self.ui.Artist, QtCore.SIGNAL("itemClicked(QTreeWidgetItem*,int)"), self.call_albums_before )
        QtCore.QObject.connect(self.ui.Artist, QtCore.SIGNAL("itemActivated(QTreeWidgetItem*,int)"), self.call_play_albums )
        QtCore.QObject.connect(self.ui.Artist, QtCore.SIGNAL("customContextMenuRequested (const QPoint&)"), self.call_right )
        QtCore.QObject.connect(self.ui.Artist.header(), QtCore.SIGNAL("sectionClicked(int)"), self.display_all )
         
        #Buttons
        QtCore.QObject.connect(self.ui.PlayButton, QtCore.SIGNAL("clicked()"), self.call_play_pause )
        QtCore.QObject.connect(self.ui.NextButton, QtCore.SIGNAL("clicked()"), self.call_next)
        QtCore.QObject.connect(self.ui.PreviousButton, QtCore.SIGNAL("clicked()"), self.call_prev)
        QtCore.QObject.connect(self.ui.RandomButton, QtCore.SIGNAL("clicked()"), self.call_random)
        QtCore.QObject.connect(self.ui.RepeatButton,QtCore.SIGNAL("clicked()"), self.call_repeat)
    	QtCore.QObject.connect(self.ui.PlaylistButton,QtCore.SIGNAL("clicked()"), self.call_playlist)
        
        #LookingFor
        QtCore.QObject.connect(self.ui.LookingFor, QtCore.SIGNAL("textEdited(QString)"), self.call_search)
        
        #./! fetch mode
        QtCore.QObject.connect(self.ui.LookingForNoTouch, QtCore.SIGNAL("clicked()"), self.call_fetch)
        #QtCore.QObject.connect(self.ui.verticalSlider, QtCore.SIGNAL("valueChanged(int)"), self.call_volume )

        # Browser Window

        QtCore.QObject.connect(self.Browser.select_path, QtCore.SIGNAL("clicked()"), self.send_path)	
    
    def call_right(self):
        self.right = True

#-------------------------------------------------------------------
#-------------------------------------------------------------------
#Sincing with server
#-------------------------------------------------------------------
#-------------------------------------------------------------------
    def send_path(self):
#        self.server.update_db(str(self.Browser.dest_path_edit.text()))   
        print str(self.Browser.dest_path_edit.text())
        self.Browser.close()    
    
    def get_db(self):
        """Import DB from server"""
        with open(config.defaultDbLocation + config.defaultDbFileImported, 'wb') as handle:
            handle.write(self.server.get_db().data)

    def sync_server(self):
        """Sincing common variables with the server"""
        self.point = self.server.get_point()
        self.playlist = self.server.get_playlist()
        self.date_sync = time.time()

    def sync_stream(self, reset = False):
        if self.server.is_loaded():
            self.position = self.server.get_position()
            self.duration = self.server.get_duration()
            return True
        else:
            return False

    def apply_changes(self):
        """Called after every action that changes the song played (next, prev, change)"""
        self.sync_server()
        self.run_stream()
        self.iconChange()
        self.display_name()

#-------------------------------------------------------------------
#-------------------------------------------------------------------
#Interface with signals (clicks)
#-------------------------------------------------------------------
#-------------------------------------------------------------------

    def call_play_pause(self):
        self.server.play_pause()
        #do not forget to work with the other thread
     	if self.server.is_playing():
            self.run_stream()
        else:
            self.songStream.terminate()

        #displaying the changes
        self.iconChange()
        self.select()

    def call_change(self, QtWidget):
        """When a song is doubleclicked on in the playlist"""
        #we have the id of the song clicked on
        idSong = str(QtWidget.text(4))

        self.deselect()
        #if in playlist view, index == point
        if not self.fetch:
            self.point = self.ui.AudioTrack.indexOfTopLevelItem(QtWidget)
        #if not, have to check if it is in playlist
        else:
            #if it is in playlist : moving point
            if idSong in self.playlist:
                self.point = 0
                for i in range(len(self.playlist)):
                    if self.playlist[i] == idSong:
                        self.point = i
            #if not, adding at the end
            else:
                self.point = len(self.playlist)
                self.set_playlist(self.playlist + [str(idSong)])

        self.server.change(self.point)
        self.apply_changes()
        self.position = 0
        self.select()

    def call_next(self):
        """The function return True if it has found a new song to play, False either""" 
        self.deselect()
        self.server.next()
        self.apply_changes()
        self.position = 0
        #perhaps it would be better to update all tracks shown..
        if self.server.get_mode() != config.normal:
            self.ui.addTrack(self.songs[self.playlist[self.point]])
        self.select()

    def call_prev(self):
        """When previous button clicked on, convention : go to the end if at the first"""
        self.deselect()
        self.server.prev()
        self.apply_changes()
        self.position = 0
        self.select()

    def call_random(self):
        self.server.random()
        self.sync_server()
        self.display_playlist()
        self.display_tracks()

    def call_playlist(self):
        self.server.mode_playlist()
        self.sync_server()
        self.display_playlist()
        self.display_tracks()

    def call_repeat(self):
        self.server.mode_repeat()
        self.display_repeat()

    def call_volume(self, int):
        self.server.set_volume(int * 10 / (self.ui.verticalSlider.maximum()-self.ui.verticalSlider.minimum()))


    def open_browser(self):
        self.Browser.setWindowModality(QtCore.Qt.ApplicationModal)
        # appel de la deuxième fenêtre
        self.Browser.set_path()
        self.Browser.show()
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
#Small graphical changes methods
#----------------------------


    def deselect(self):
        """DEselect element in the tree"""
        if self.point in range(len(self.playlist)) and self.playlist[self.point] in self.selectedSongs:
            try:
                self.ui.AudioTrack.topLevelItem(self.selected).setSelected(False)
            except:
                pass

    def select(self):
        """select element in the tree"""    
        if self.point in range(len(self.playlist)) and self.playlist[self.point] in self.selectedSongs:
            if not self.fetch:
                self.selected = self.point
            else:
                self.selected = self.selectedSongs.index(self.playlist[self.point])

            try:
                self.ui.AudioTrack.topLevelItem(self.selected).setSelected(True)
            except:
                pass
 
    def display_name(self):
        """display name of song currently playing"""
        if self.date_display_name < self.date_sync:
            try:
                self.ui.LookingForNoTouch.setText(self.songs[self.playlist[self.point]]["title"]+" - "+ self.songs[self.playlist[self.point]]['artist'])
            except:
                self.ui.LookingForNoTouch.setText("Unknown")
            self.date_display_name = time.time()

#----------------------------
#only display in TREE methods => order : (albums, tracks) doubleclicked -> clicked -> update
#----------------------------    

    def call_play_albums(self, QtWidget):
        """When an artist is doubleclicked on"""
        self.deselect()
        #select songs and display them
        self.call_albums(QtWidget)
        #then create a playlist from this set
        self.set_playlist(self.selectedSongs)
        self.server.set_point(0)
        self.server.load()
        self.server.play_pause()
        self.apply_changes()
        self.position = 0
        self.select()

    def call_play_tracks(self, QtWidget):
        """When an album is doubleclicked on"""
        self.deselect()
        #select songs and display them
        self.call_tracks(QtWidget)
        #making the playlist from the set of songs
        self.set_playlist(self.selectedSongs)
        self.server.set_point(0)
        self.server.load()
        self.server.play_pause()
        self.apply_changes()
        self.position = 0
        self.select()

    def call_albums_before(self, QtWidget):
        if not self.fetch and self.right:
            self.call_add_albums(QtWidget)
            self.right = False
        elif self.fetch:
            self.call_add_albums(QtWidget)

    def call_tracks_before(self, QtWidget):
        if not self.fetch and self.right:
            self.call_add_tracks(QtWidget)
            self.right = False
        elif self.fetch:
            self.call_add_tracks(QtWidget)

    def call_track(self, QtWidget):
        if self.right:
            self.call_add_track(QtWidget)
            self.right = False

    def call_all_albums(self):
        try:
            self.call_add_albums()
        except:
            #selectArtist == None : do nothing
            pass

    def call_add_albums(self, QtWidget = None):
        """Adding self.selectedSongs in playlist after interaction with an artist"""
        self.deselect()
        #select songs and display them
        #making the playlist from the set of songs
        #if fetching we add at the end of the playlist
        if self.fetch:
            self.call_albums(QtWidget)
            #could have done it cleverer (updating the playlist if some selected songs are already in the playlist)
            if self.point >= 0:
                self.set_playlist(self.playlist[:self.point+1] + self.selectedSongs)
            else:
                self.set_point(0)
                self.set_playlist(self.selectedSongs)
        else:
            #else doing the inverse
            self.call_albums(QtWidget, displayed = False)
            self.clean_display_playlist()

        self.select()

    def call_add_tracks(self, QtWidget):
        """Adding self.selectedSongs in playlist after interaction with an album"""
        self.deselect()
        #select songs and display them
        #making the playlist from the set of songs
        #if fetching we add at the end of the playlist
        if self.fetch:
            self.call_tracks(QtWidget)
            #could have done it cleverer (updating the playlist if some selected songs are already in the playlist)
            if self.point >= 0:
                self.set_playlist(self.playlist[:self.point+1] + self.selectedSongs)
            else:
                self.set_point(0)
                self.set_playlist(self.selectedSongs)
        else:
            #else doing the inverse
            self.call_tracks(QtWidget, displayed = False)
            self.clean_display_playlist()

        self.select()

    def clean_display_playlist(self): 
            #stopping if song is playing and removing selected ones            
            loaded = False
            stopped = False
            if self.server.is_loaded():
                loaded = True
                idLoaded = self.playlist[self.point] 
                if idLoaded in self.selectedSongs:
                    self.server.stop()
                    stopped = True
     
            for song in self.selectedSongs:
               #possibly several occurences
                while song in self.playlist:                 
                    self.playlist.remove(song)
            
            #updating server playlist and point
            self.set_playlist(self.playlist)            
            if loaded and not stopped:
                self.set_point(self.playlist.index(idLoaded))
                            
            if stopped:
                self.apply_changes()

            self.display_all()

    def call_add_track(self, QtWidget):
        """When an album is rightclicked on"""
        song = str(QtWidget.text(4)) 
        #making the playlist from the set of songs
        #if fetching we add at the end of the playlist
        if self.fetch:
            #could have done it cleverer (updating the playlist if some selected songs are already in the playlist)
            self.playlist.append(song)
            self.set_playlist(self.playlist)
        else:
            #else doing the inverse
            self.selectedSongs = [song]
            self.clean_display_playlist()            
 
    def call_albums(self, QtWidget = None, displayed = True):
        """When an artist is clicked on..."""
        #if we just want to see all available albums
        if QtWidget != None:
            self.selectedArtist = str(QtWidget.text(0))
        self.selectedSongs = set()
        
        #adding all the songs to the set
        for album in self.artists[self.selectedArtist]:
            for idTrack in self.albums[album]:
                if self.fetch or (idTrack in self.playlist):
                    self.selectedSongs.add(idTrack)
       
        if displayed:
            #sorting them
            self.selectedSongs = make_neighbors(self.songs, self.selectedSongs) 
            #and update the ui then
            self.display_albums()
  
    def call_tracks(self, QtWidget, displayed = True):
        """When an album is doubleclicked on"""
        self.selectedAlbum = str(QtWidget.text(0))
        
        if self.fetch:
            self.selectedSongs = self.albums[self.selectedAlbum] 
        else:
            self.selectedSongs = set(self.albums[self.selectedAlbum]).intersection(set(self.playlist))       
        
        if displayed:
            #sorting them
            self.selectedSongs = make_neighbors(self.songs, self.selectedSongs) 
            #updating the ui then
            self.display_tracks()

    def display_albums(self):
        """update albuml list and tracklist"""
        self.ui.Album.clear()
        self.ui.AudioTrack.clear()
        
        #add them in the order of the playlist, that is to say, alphabetical order for albums
        self.displayedAlbums = set()
        for idTrack in self.selectedSongs:
            #adding an album if he hasn't already been displayed
            if self.songs[idTrack]["album"] not in self.displayedAlbums:
                self.displayedAlbums.add(self.songs[idTrack]["album"])
                self.ui.addAlbum(self.songs[idTrack]["album"])
            self.ui.addTrack(self.songs[idTrack])

    def display_tracks(self):
        """display elements of the playlist"""
        #removing elements from the album tree
        self.ui.AudioTrack.clear()

        for idTrack in self.selectedSongs:
            self.ui.addTrack(self.songs[idTrack])

    def call_all(self):
        """display all the songs (for clicks)"""
        self.display_all()
         
        #then create a playlist from this set
        self.set_playlist(self.selectedSongs)
        self.set_point(0)
        self.display_tracks()  

   
    def display_all(self):
        """display all albums and artists and set point at the beginning"""
        #cleaning the lists
        self.ui.Artist.clear()
        self.ui.Album.clear()
        self.ui.AudioTrack.clear()

        #sorting the artists and albums by name for it to be smarter, and display
        if not self.fetch:
            self.selectedSongs = self.playlist
            #Only display what is in the playlist in the order of the playlist for album and artist
        else:
            self.selectedSongs = make_neighbors(self.songs, self.songs.keys())
            #display all

        self.displayedArtists = set()
        self.displayedAlbums = set()         
        for idSong in self.selectedSongs:
            if self.songs[idSong]['artist'] not in self.displayedArtists:
                self.displayedArtists.add(self.songs[idSong]['artist'])
                self.ui.addArtist(self.songs[idSong]['artist'])
            if self.songs[idSong]['album'] not in self.displayedAlbums:
                self.displayedAlbums.add(self.songs[idSong]['album'])
                self.ui.addAlbum(self.songs[idSong]['album'])
            self.ui.addTrack(self.songs[idSong])

#----------------------------
#button states
#----------------------------

    def call_fetch(self):
        self.deselect()
        self.fetch = not self.fetch
        self.display_fetch()
        self.display_all()
        self.select()
    
    def display_fetch(self):
        if self.fetch == True:
            self.ui.LookingForNoTouch.setChecked(False)
        else:
            self.ui.LookingForNoTouch.setChecked(True)

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

    def display_playlist(self):
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

    def display_repeat(self):
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

#----------------------------
#All relevant to song stream
#----------------------------

    def run_stream(self):
        try:    
            self.songStream.terminate()
        except:
            pass
       
        #do not launch songbar if not synchronised
        self.display_name()
        self.ui.SongBar.reset()
        if self.sync_stream():
            self.ui.SongBar.setMaximum(int(self.duration*100))
            self.ui.SongBar.setMinimum(0)
            self.songStream = Song()
            self.connect(self.songStream, QtCore.SIGNAL("progressUpdated"), self.updateSongProgress)
            self.songStream.start()
    
    def updateSongProgress(self):
        #we sync to server only at the end and the begining
        if int(self.position) % 10 == 0 or self.position > self.duration - config.anticipateDisplay or self.position < config.anticipateDisplay:
            #sync before the end or at the beginning
            self.deselect()
            self.sync_server()
            
            if not self.sync_stream() and self.position > self.duration + config.anticipateDisplay:
                self.songStream.terminate()

            self.ui.SongBar.setMaximum(int(self.duration*100))
            self.select()
            self.display_name()
        
        self.position += config.dtDisplay 
        self.ui.SongBar.setValue(int(self.position*100))
        self.ui.SongBar.setFormat(give_time(int(self.position)) + " / " + give_time(int(self.duration)))
        self.ui.SongBar.repaint()

    def call_search(self, QString):
        self.selectedSongs = set()
        for artist in self.artists:
            for album in self.artists[artist]:
                for idTrack in self.albums[album]:
                    try:
                        b=self.songs[idTrack]['title'].__contains__(str(QString)) or  self.songs[idTrack]['album'].__contains__(str(QString)) or self.songs[idTrack]['artist'].__contains__(str(QString))
                        if b:
                            self.selectedSongs.add(idTrack)
                    except:
                        pass
        #then create a playlist from this set
        self.set_playlist(make_neighbors(self.songs, self.selectedSongs))
        self.set_point(0)
        
        #and update the ui then
        self.display_albums()

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
