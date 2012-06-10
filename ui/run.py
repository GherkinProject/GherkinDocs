# -*- coding: utf-8 -*-
 
from PyQt4 import QtCore, QtGui
from display import Ui_ProjetGherkin
from dbbrowser import Browser_Window
from server_window import server_window
from playlistwidget import playlist_window


import sys

#local lib : loading db
from load_db import *

#configuration constant
from configUi import *

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
        self.Ui = Ui_ProjetGherkin()
        self.Ui.setupUi(self)
        self.Browser = Browser_Window()
        self.Dialog = QtGui.QDialog()
        self.Server_Window= server_window()
        self.Server_Window.setup_server_window(self.Dialog)
        self.Widget = QtGui.QWidget()
        self.Playlist_Window = playlist_window()
        self.Playlist_Window.setup_playlist_window(self.Widget)

        #self.Ui.AudioTrack.mousePressEvent = mousePressEvent        
        
        #initializing server
        self.start_ui()
        
        #signal received, functions called

        # Shortcuts
        self.shortPlay = QtGui.QShortcut(QtGui.QKeySequence("Ctrl+J"), self)
        self.shortPrev = QtGui.QShortcut(QtGui.QKeySequence("Ctrl+H"), self)
        self.shortNext = QtGui.QShortcut(QtGui.QKeySequence("Ctrl+K"), self)
        QtCore.QObject.connect(self.shortPlay, QtCore.SIGNAL('activated()'), self.call_play_pause )
        QtCore.QObject.connect(self.shortPrev, QtCore.SIGNAL('activated()'), self.call_prev )
        QtCore.QObject.connect(self.shortNext, QtCore.SIGNAL('activated()'), self.call_next )
        
        # Menu
        QtCore.QObject.connect(self.Ui.actionImporter_Dossier, QtCore.SIGNAL("triggered()"), self.open_browser)
        QtCore.QObject.connect(self.Ui.actionChercher_Serveur, QtCore.SIGNAL("triggered()"), self.open_server_window)
        
        # By song
        QtCore.QObject.connect(self.Ui.AudioTrack, QtCore.SIGNAL("itemClicked(QTreeWidgetItem*,int)"), self.call_track_before )
        QtCore.QObject.connect(self.Ui.AudioTrack, QtCore.SIGNAL("itemActivated(QTreeWidgetItem*,int)"), self.call_play_track )
        QtCore.QObject.connect(self.Ui.AudioTrack, QtCore.SIGNAL("customContextMenuRequested (const QPoint&)"), self.call_right )
        # By album
        QtCore.QObject.connect(self.Ui.Album, QtCore.SIGNAL("itemClicked(QTreeWidgetItem*,int)"), self.call_album_before )
        QtCore.QObject.connect(self.Ui.Album, QtCore.SIGNAL("itemActivated(QTreeWidgetItem*,int)"), self.call_play_album)
        QtCore.QObject.connect(self.Ui.Album, QtCore.SIGNAL("customContextMenuRequested (const QPoint&)"), self.call_right )
        QtCore.QObject.connect(self.Ui.Album.header(), QtCore.SIGNAL("sectionClicked(int)"), self.call_add_all_albums )
        # By artist
        QtCore.QObject.connect(self.Ui.Artist, QtCore.SIGNAL("itemClicked(QTreeWidgetItem*,int)"), self.call_artist_before )
        QtCore.QObject.connect(self.Ui.Artist, QtCore.SIGNAL("itemActivated(QTreeWidgetItem*,int)"), self.call_play_artist )
        QtCore.QObject.connect(self.Ui.Artist, QtCore.SIGNAL("customContextMenuRequested (const QPoint&)"), self.call_right )
        QtCore.QObject.connect(self.Ui.Artist.header(), QtCore.SIGNAL("sectionClicked(int)"), self.call_add_all )
         
        # Buttons
        QtCore.QObject.connect(self.Ui.PlayButton, QtCore.SIGNAL("clicked()"), self.call_play_pause )
        QtCore.QObject.connect(self.Ui.NextButton, QtCore.SIGNAL("clicked()"), self.call_next)
        QtCore.QObject.connect(self.Ui.PreviousButton, QtCore.SIGNAL("clicked()"), self.call_prev)
        QtCore.QObject.connect(self.Ui.RandomButton, QtCore.SIGNAL("clicked()"), self.call_random)
        QtCore.QObject.connect(self.Ui.RepeatButton,QtCore.SIGNAL("clicked()"), self.call_repeat)
    	QtCore.QObject.connect(self.Ui.PlaylistButton,QtCore.SIGNAL("clicked()"), self.call_playlist_button)
        
        # LookingFor
        QtCore.QObject.connect(self.Ui.LookingFor, QtCore.SIGNAL("textEdited(QString)"), self.call_search)
        
        #./! fetch mode
        QtCore.QObject.connect(self.Ui.LookingForNoTouch, QtCore.SIGNAL("clicked()"), self.call_fetch)  
        QtCore.QObject.connect(self.Ui.verticalSlider, QtCore.SIGNAL("valueChanged(int)"), self.call_volume )

        # Playlist Window
        QtCore.QObject.connect(self.Playlist_Window.Playlist, QtCore.SIGNAL("itemActivated(QTreeWidgetItem*,int)"), self.call_play_playlist )
        QtCore.QObject.connect(self.Playlist_Window.Playlist, QtCore.SIGNAL("itemClicked(QTreeWidgetItem*,int)"), self.call_playlist_before)  
        QtCore.QObject.connect(self.Playlist_Window.Playlist, QtCore.SIGNAL("customContextMenuRequested (const QPoint&)"), self.call_right)  

        # Browser Window
        QtCore.QObject.connect(self.Browser.select_path, QtCore.SIGNAL("clicked()"), self.send_path)

        # Server Window
        QtCore.QObject.connect(self.Dialog, QtCore.SIGNAL("accepted()"), self.change_server)
        QtCore.QObject.connect(self.Server_Window.radioButton, QtCore.SIGNAL("toggled(bool)"), self.lf_server)

    def start_ui(self): 
        #connection with the server
        self.server = xmlrpclib.ServerProxy("http://" + config.serverName + ":" + str(config.defaultPort))

        #launching not in fetchmode
        self.fetch = True
        self.right = False 

        #var linked with the server
        self.point = -1
        self.playlist = []

        #sync with the server at the beginning
        self.sync_server()
        self.iconChange()
        self.update_volume()
        
        #get self.songsBase, self.artistsBase, self.albumsBase
        self.get_lib()
        
        #self.artists,albums,songs can possibly change because of 'looking for'
        self.artists = dict(self.artistsBase)
        self.albums = dict(self.albumsBase)
        self.songs = dict(self.songsBase)


        #display artists and albums at launch, if server is playing, display current infos
        self.date_display_name = -1
        if self.playlist != []:
            #displaying playlist
            self.call_fetch()
            self.selectedSongs = self.playlist
            self.call_add_all()
            if self.point != -1:
                self.display_name()
                if self.server.is_playing():
                    self.run_stream()
        else:
            #fetching tracks
            self.fetch = True
            self.call_add_all()
           
        #update buttons state
        self.button_fetch() 
        self.button_repeat()
        self.button_playlist()
        
        if self.server.is_playing():
            self.run_stream()
    
    def call_right(self):
        self.right = True

#-------------------------------------------------------------------
#-------------------------------------------------------------------
#Sincing with server
#-------------------------------------------------------------------
#-------------------------------------------------------------------
    def get_lib(self):
        """Getting the lib from the xml file"""
        if config.serverName == "localhost":
            (self.artistsBase, self.albumsBase, self.songsBase) = get_lib(dbLocation = config.defaultDbLocation, dbFile = config.defaultDbFile)
        else:
            #downloading db from server
            with open(config.defaultDbLocation + config.defaultDbFileImported, 'wb') as handle:
                handle.write(self.server.get_db().data)
            
            (self.artistsBase, self.albumsBase, self.songsBase) = get_lib(dbFile = config.defaultDbFileImported)


    def send_path(self):
        """Send db path to server"""
        self.server.update_db(str(self.Browser.dest_path_edit.text())) 
        self.Browser.close()   

    def change_server(self):
        """Change the server to the one indicated in the Dialog box"""
        address = str(self.Server_Window.lineEdit.text())
        address = address.split(":")
        config.set('server', 'name', address[0])
        config.set('server', 'port', address[1])
        self.start_ui()

    def lf_server(self):
        """Look for new server"""
        if bool:
            for i in range (256):
                for j in range(2):
                    for k in range(6):
                        for l in range(256):
                            Z = str(l)+"."+str(k)+"."+str(j)+"."+str(i)
                            # Compute Z which represents the server adress
#                            if self.server.exists(Z):
                            if l == 40 and i == 21:
                                self.Server_Window.add_server(Z)

    def sync_server(self):
        """Sincing common variables with the server"""
        self.point = self.server.get_point()
        self.playlist = self.server.get_playlist()
        if not self.fetch:
            self.display_playlist()
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

    def call_fetch(self):
        if self.fetch:
        # Was in fetch mode... not anymore. Display window
            self.Playlist_Window.Playlist.clear()
            self.Widget.show()
        else:
            self.Widget.hide()
        
        self.fetch = not self.fetch
        self.button_fetch()
        self.call_add_all()
        self.select()
 
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

    def call_next(self):
        """The function return True if it has found a new song to play, False either""" 
        self.deselect()
        self.server.next()
        self.apply_changes()
        self.position = 0
        #perhaps it would be better to update all tracks shown..
        if self.server.get_mode() != config.normal:
            self.Ui.addTrack(self.songs[self.playlist[self.point]])
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
        self.button_playlist()
        self.display_album()

    def call_playlist_button(self):
        self.server.mode_playlist()
        self.sync_server()
        self.button_playlist()
        self.display_album()

    def call_repeat(self):
        self.server.mode_repeat()
        self.button_repeat()

    def call_volume(self, val):
        self.server.set_volume(float(val)/100)

    def update_volume(self):
        self.Ui.verticalSlider.setValue(self.server.get_volume() * (self.Ui.verticalSlider.maximum()-self.Ui.verticalSlider.minimum()) + self.Ui.verticalSlider.minimum())

    def open_browser(self):
        self.Browser.setWindowModality(QtCore.Qt.ApplicationModal)
        # appel de la deuxième fenêtre
        self.Browser.set_path()
        self.Browser.show()

    def open_server_window(self):
        self.Dialog.show()

        
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
    
    def add_playlist(self, newSongs):
        """update playlist adding newSongs, and prun the rest if fetch mode"""
        if self.fetch:
            try:
                jump = max(0, self.point - config.keepPlaylist)
                prev = self.playlist[jump:self.point+1]
            except:
                self.point, jump = 0, 0
                prev = []
                
            self.set_playlist(prev + newSongs)
            self.set_point(self.point - jump)
        else:
            if self.right:
                self.set_playlist(self.playlist + newSongs)
            else:
                self.set_playlist(self.playlist[0:self.point] + newSongs + self.playlist[self.point:])

    def set_point(self, point):
        """update point of ui and server"""
        self.server.set_point(point)
        self.point = point

#----------------------------
#Small graphical changes methods
#----------------------------

    def deselect(self):
        """DEselect element in the Ui and Playlist tree"""
        if self.point in range(len(self.playlist)):
            if self.playlist[self.point] in self.selectedSongs: 
                try:    
                    self.Ui.AudioTrack.topLevelItem(self.selected).setSelected(False)
                except:
                    pass
            if not self.fetch:
                try:
                    self.Playlist_Window.Playlist.topLevelItem(self.selected).setSelected(False)
                except:
                    pass

    def select(self):
        """select element in the tree"""    
        if self.point in range(len(self.playlist)):
            if self.playlist[self.point] in self.selectedSongs: 
                try:
                    self.selected = self.selectedSongs.index(self.playlist[self.point])
                    self.Ui.AudioTrack.topLevelItem(self.selected).setSelected(True)
                except:
                    self.selected = None
            if not self.fetch:
                try:
                    self.Playlist_Window.Playlist.topLevelItem(self.point).setSelected(True)
                except:
                    pass
 
    def display_name(self):
        """display name of song currently playing"""
        if self.date_display_name < self.date_sync:
            try:
                self.Ui.LookingForNoTouch.setText(self.songsBase[self.playlist[self.point]]["title"]+" - "+ self.songsBase[self.playlist[self.point]]['artist'])
            except:
                self.Ui.LookingForNoTouch.setText("Unknown")
            self.date_display_name = time.time()

#----------------------------
#only display in TREE methods => order : (albums, tracks) doubleclicked -> clicked -> update
#----------------------------    

# CALL_PLAY : CALL_ADD then PLAY

    def call_play_track(self, QtWidget):
        """When a song is doubleclicked on in the playlist"""
        #we have the id of the song clicked on
        idSong = str(QtWidget.text(4))

        self.deselect()
        
        #if it is in playlist : moving point
        if idSong in self.playlist:
            self.point = 0
            for i in range(len(self.playlist)):
                if self.playlist[i] == idSong:
                    self.point = i
        else: #we are in playlist mode   
            self.add_playlist([idSong])
        
        self.server.change(self.point)
        self.apply_changes()
        self.position = 0
        self.select()

    def call_play_playlist(self, QtWidget):
        """play a given element from the playlist"""
        idPlay = self.Playlist_Window.Playlist.indexOfTopLevelItem(QtWidget)
        self.deselect()
        self.server.change(idPlay)
        self.apply_changes()
        self.position = 0
        self.select() 

    def call_play_artist(self, QtWidget):
        """When an artist is doubleclicked on"""
        self.deselect()
        #select songs and display them
        self.call_artist(QtWidget)
        #then create a playlist from this set
        self.set_playlist(self.selectedSongs)
        self.server.set_point(0)
        self.server.load()
        self.server.play_pause()
        self.apply_changes()
        self.position = 0
        self.select()

    def call_play_album(self, QtWidget):
        """When an album is doubleclicked on"""
        self.deselect()
        #select songs and display them
        self.call_album(QtWidget)
        #making the playlist from the set of songs
        self.set_playlist(self.selectedSongs)
        self.server.set_point(0)
        self.server.load()
        self.server.play_pause()
        self.apply_changes()
        self.position = 0
        self.select()

# CALL_BEFORE : click management then CALL_ADD

    def call_artist_before(self, QtWidget):
        if self.right:
            self.call_add_artist(QtWidget)
            self.right = False
        else:
            self.call_add_artist(QtWidget)

    def call_album_before(self, QtWidget):
        if self.right:
            self.call_add_album(QtWidget)
            self.right = False
        else:
            self.call_add_album(QtWidget)

    def call_track_before(self, QtWidget):
        if self.right:
            self.call_add_track(QtWidget)
            self.right = False

    def call_playlist_before(self, QtWidget):
        if self.right:
            self.call_remove_track(QtWidget)
            self.right = False


# CALL_ADD : first CALL_ADD then playlist_management according to self.fetch

    def call_add_all(self):
        """display all the songs (for clicks)"""
        self.call_all()
         
        #then create a playlist from this set
        if self.fetch:
            self.add_playlist(self.selectedSongs)
        else:
            self.display_playlist()

    def call_add_artist(self, QtWidget = None):
        """Adding self.selectedSongs in playlist after interaction with an artist"""
        self.deselect()

        #select songs and display them
        #if fetching we add at the end of the playlist
        self.call_artist(QtWidget)
        
        if self.fetch:
            #could have done it cleverer (updating the playlist if some selected songs are already in the playlist)
            if self.point >= 0:
                self.add_playlist(self.selectedSongs)
            else:
                self.set_point(0)
                self.set_playlist(self.selectedSongs)
        else:
            if self.right:
                self.add_playlist(self.selectedSongs)
            self.display_playlist()

        self.select()

    def call_add_all_albums(self):
        try:
            self.call_add_artist()
        except:
            pass

    def call_add_album(self, QtWidget):
        """Adding self.selectedSongs in playlist after interaction with an album"""
        self.deselect()
        #select songs and display them
        #if fetching we add at the end of the playlist
        self.call_album(QtWidget)
        
        if self.fetch:
            #could have done it cleverer (updating the playlist if some selected songs are already in the playlist)
            if self.point >= 0:
                self.add_playlist(self.selectedSongs)
            else:
                self.set_point(0)
                self.set_playlist(self.selectedSongs)
        else:
            if self.right:
                self.add_playlist(self.selectedSongs)
            self.display_playlist()

        self.select()

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
            if self.right:
                self.add_playlist(self.selectedSongs)
            self.display_playlist()

    def call_remove_track(self, QtWidget):
        """When wanting to remove a song from the playlist"""
        idPlay = self.Playlist_Window.Playlist.indexOfTopLevelItem(QtWidget) 
        self.set_playlist(self.playlist[0:idPlay] + self.playlist[idPlay+1:])
        self.Playlist_Window.Playlist.takeTopLevelItem(idPlay)
        #self.display_playlist()
  
# CALL : make selectedSongs and call DISPLAY

    def call_all(self):
        """display all albums and artists and set point at the beginning"""
        self.selectedSongs = make_neighbors(self.songs, set(self.songs.keys()))
        self.display_all_artists()

    def call_artist(self, QtWidget = None, displayed = True):
        """When an artist is clicked on..."""
        #if we just want to see all available albums
        if QtWidget != None:
            self.selectedArtist = str(QtWidget.text(0))
        self.selectedSongs = set()
        
        #adding all the songs to the set
        for album in self.artists[self.selectedArtist]:
            for idSong in self.albums[album]:
                self.selectedSongs.add(idSong)
       
        if displayed:
            #sorting them
            self.selectedSongs = make_neighbors(self.songs, self.selectedSongs) 
            #and update the ui then
            self.display_artist()

  
    def call_album(self, QtWidget, displayed = True):
        """When an album is doubleclicked on"""
        self.selectedAlbum = str(QtWidget.text(0))
        self.selectedSongs = self.albums[self.selectedAlbum] 
        
        if displayed:
            #sorting them
            self.selectedSongs = make_neighbors(self.songs, self.selectedSongs) 
            #updating the ui then
            self.display_album()

# DISPLAY songs
    
    def display_all_artists(self):
        #cleaning the lists
        self.Ui.Artist.clear()
        self.Ui.Album.clear()
        self.Ui.AudioTrack.clear()
 
        self.displayedArtists = set()
        self.displayedAlbums = set()         
        for idSong in self.selectedSongs:
            if idSong in self.songs.keys():
                if self.songs[idSong]['artist'] not in self.displayedArtists:
                    self.displayedArtists.add(self.songs[idSong]['artist'])
                    self.Ui.addArtist(self.songs[idSong]['artist'])
                if self.songs[idSong]['album'] not in self.displayedAlbums:
                    self.displayedAlbums.add(self.songs[idSong]['album'])
                    self.Ui.addAlbum(self.songs[idSong]['album'])
                self.Ui.addTrack(self.songs[idSong])
            else:
                pass	

    def display_artist(self):
        """update albuml list and tracklist"""
        self.Ui.Album.clear()
        self.Ui.AudioTrack.clear()
        
        #add them in the order of the playlist, that is to say, alphabetical order for albums
        self.displayedAlbums = set()
        for idSong in self.selectedSongs:
            if idSong in self.songs.keys():
                #adding an album if he hasn't already been displayed
                if self.songs[idSong]["album"] not in self.displayedAlbums:
                    self.displayedAlbums.add(self.songs[idSong]["album"])
                    self.Ui.addAlbum(self.songs[idSong]["album"])
                self.Ui.addTrack(self.songs[idSong])
            else:
                pass

    def display_album(self):
        """display elements of the album"""
        #removing elements from the album tree
        self.Ui.AudioTrack.clear()
        for idSong in self.selectedSongs:
            if idSong in self.songs.keys():
                self.Ui.addTrack(self.songs[idSong])
            else:
                pass

    def display_playlist(self):
        """display elements of the playlist"""
        #removing elements from the playlist tree
        self.Playlist_Window.Playlist.clear()
        for idSong in self.playlist:
            self.Playlist_Window.addTrack(self.songsBase[idSong])
        self.select()

    def clean_button_playlist(self): 
        """for playlist mode, if we want to remove songs from playlist"""    
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

        self.call_add_all()

#----------------------------
#button states
#----------------------------
   
    def button_fetch(self):
        if self.fetch == True:
            self.Ui.LookingForNoTouch.setChecked(False)
        else:
            self.Ui.LookingForNoTouch.setChecked(True)

    def iconChange(self):
        if self.server.is_playing():
            icon2 = QtGui.QIcon()
            icon2.addPixmap(QtGui.QPixmap((config.pauseIcon)), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.Ui.PlayButton.setIcon(icon2)
            self.Ui.PlayButton.setIconSize(QtCore.QSize(30, 30))
    	else:
            icon2 = QtGui.QIcon()
            icon2.addPixmap(QtGui.QPixmap((config.playIcon)), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    	    self.Ui.PlayButton.setIcon(icon2)
            self.Ui.PlayButton.setIconSize(QtCore.QSize(30, 30))

    def button_playlist(self):
        if self.server.get_mode() == config.random:
            icon2 = QtGui.QIcon()
            icon2.addPixmap(QtGui.QPixmap((config.randomOnIcon)), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.Ui.RandomButton.setIcon(icon2)
            self.Ui.RandomButton.setIconSize(QtCore.QSize(30,30))
        else:
            icon2 = QtGui.QIcon()
            icon2.addPixmap(QtGui.QPixmap((config.randomOffIcon)), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.Ui.RandomButton.setIcon(icon2)
            self.Ui.RandomButton.setIconSize(QtCore.QSize(30,30))
        if self.server.get_mode() == config.playlist:
            icon2 = QtGui.QIcon()
            icon2.addPixmap(QtGui.QPixmap((config.playlistOnIcon)), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.Ui.PlaylistButton.setIcon(icon2)
            self.Ui.PlaylistButton.setIconSize(QtCore.QSize(30,30))
    	else:
            icon2 = QtGui.QIcon()
            icon2.addPixmap(QtGui.QPixmap((config.playlistOffIcon)), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.Ui.PlaylistButton.setIcon(icon2)
            self.Ui.PlaylistButton.setIconSize(QtCore.QSize(30,30))

    def button_repeat(self):
        if not self.server.get_repeat():
            icon2 = QtGui.QIcon()
            icon2.addPixmap(QtGui.QPixmap((config.repeatOffIcon)), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.Ui.RepeatButton.setIcon(icon2)
            self.Ui.RepeatButton.setIconSize(QtCore.QSize(30,30))
        else:
            icon2 = QtGui.QIcon()
            icon2.addPixmap(QtGui.QPixmap((config.repeatOnIcon)), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.Ui.RepeatButton.setIcon(icon2)
            self.Ui.RepeatButton.setIconSize(QtCore.QSize(30,30))

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
        self.Ui.SongBar.reset()
        if self.sync_stream():
            self.Ui.SongBar.setMaximum(int(self.duration*100))
            self.Ui.SongBar.setMinimum(0)
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

            self.Ui.SongBar.setMaximum(int(self.duration*100))
            self.select()
            self.display_name()
        
        self.position += config.dtDisplay 
        self.Ui.SongBar.setValue(int(self.position*100))
        self.Ui.SongBar.setFormat(give_time(int(self.position)) + " / " + give_time(int(self.duration)))
        self.Ui.SongBar.repaint()

    def call_search(self, QString):
        search = str(QString)
        
        if search == "":
            self.artists = dict(self.artistsBase)
            self.albums = dict(self.albumsBase)
            self.songs = dict(self.songsBase)
        else:
            self.artists = dict()
            self.albums = dict()
            self.songs = dict()
            
            for artist in self.artistsBase.keys():
                if search in artist:
                    self.artists[artist] = set(self.artistsBase[artist])
                
                for album in self.artistsBase[artist]:
                    if search in artist or search in album:
                        self.albums[album] = set(self.albumsBase[album])
                    
                    if search in album:
                        if self.artists.has_key(artist):
                            self.artists[artist].add(album)
                        else:
                            self.artists[artist] = set([album])

                    for idSong in self.albumsBase[album]:
                        if search in artist or search in album or search in self.songsBase[idSong]['title']:
                            self.songs[idSong] = self.songsBase[idSong]

                        if search in self.songsBase[idSong]['title']:
                            if self.artists.has_key(artist):
                                self.artists[artist].add(album)
                            else:
                                self.artists[artist] = set([album])
                            
                            if self.albums.has_key(album):
                                self.albums[album].add(idSong)
                            else:
                                self.albums[album] = set([idSong])
             
        self.call_add_all()
        

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
