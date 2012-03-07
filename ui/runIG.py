# -*- coding: utf-8 -*-
#!/usr/bin/python -d
 
from PyQt4 import QtCore, QtGui
from testIG import Ui_ProjetGherkin
import sys

#local lib : loading db
from load_db import *

#configuration constant
import config

#client lib for calling server
import xmlrpclib

class MyForm(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_ProjetGherkin()
        self.ui.setupUi(self)
        
        #connection with the server
        self.server = xmlrpclib.ServerProxy("http://" + config.serverName + ":" + str(config.defaultPort))
          
        #they come together
        self.playlist = self.server.get_playlist()
        
        #saving artists and songs displayed
        #getting the lib from the xml file
        if config.serverName == "localhost":
            (self.artists, self.albums, self.songs) = get_lib()
	
        #display artists and albums at launch
        self.display_all()

        #self.server.load()

        #loading song into the server
        #TO BE CHANGE ! id = 0 may not exist !
        #self.playlist.append(self.songs.keys()[0])
        #self.server.load(self.songs[self.playlist[self.pointeur]]['location'])
        
        self.update_tracks()

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

    def add_entry(self):
        self.ui.lineEdit.selectAll()
        self.ui.lineEdit.cut()
        self.ui.textEdit.append("")
        self.ui.textEdit.paste()
    
    def load(self):
        #terminate process, if existing
        try:
            self.song_play.terminate()
        except:
            pass
        try:
            self.ui.LookingForNoTouch.setText(self.songs[self.playlist[self.pointeur]]["title"]+" - "+ self.songs[self.playlist[self.pointeur]]['artist'])
        except:
            self.ui.LookingForNoTouch.setText("Unknown")

        self.server.load()
        
    def call_play_pause(self):
        self.server.play_pause()

        #do not forget to work with the other thread
     	if self.server.is_playing():
            self.runSong()
        else:
            self.song_play.quit()

        #displaying the changes
        self.iconChange()
        self.ui.AudioTrack.topLevelItem(self.pointeur).setSelected(True)

    def call_change(self, QtWidget, val = 0):
        """When a song is doubleclicked on in the playlist"""
        #we have the id of the song clicked on
        idSong = int(QtWidget.text(4))

        #deselect the track in the ui
        self.ui.AudioTrack.topLevelItem(self.pointeur).setSelected(False)
        
        self.pointeur = 0
        #looking for the selected track in the playlist
        while self.playlist[self.pointeur] != idSong:
            self.pointeur += 1

        #loading and playing
        self.server.change(self.pointeur)
        
        #needs graphical changes
        self.load()
        self.call_play_pause()
    
    def display_all(self):
        """display all albums and artists"""
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
        
        #then create a playlist from this set
        self.playlist = make_neighbors(self.songs, self.selectedSongs)
        self.server.set_playlist(self.playlist)
        self.pointeur = 0
        
        #and update the ui then
        self.update_albums()
 
    def call_play_albums(self, QtWidget):
        self.call_albums(QtWidget)
        self.load()
        self.call_play_pause()

    def call_play_tracks(self, QtWidget):
        self.call_tracks(QtWidget)
        self.load()
        self.call_play_pause()
    
    def call_albums(self, QtWidget, val = 0):
        """When an artist is clicked on..."""
        self.selectedArtist = str(QtWidget.text(0))
        self.selectedSongs = set()
        
        #adding all the songs to the set
        for album in self.artists[self.selectedArtist]:
            for idTrack in self.albums[album]:
                self.selectedSongs.add(idTrack)
        
        #then create a playlist from this set
        self.playlist = make_neighbors(self.songs, self.selectedSongs)
        self.server.set_playlist(self.playlist)
        self.pointeur = 0
        
        #and update the ui then
        self.update_albums()
    
    def update_albums(self):
        #removing elements from the album tree
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
    
    def update_artists(self):
        #removing elements from the artist tree
        self.ui.Artist.clear()
        self.ui.Album.clear()
        self.ui.AudioTrack.clear()
        
        #add them in the ordre of the playlist => alphabetical order for artists
        self.displayedArtists = set()
        self.displayedAlbums = set()
        for idTrack in self.playlist:
            #one should be added if not yet displayed
            if self.songs[idTrack]["artist"] not in self.displayedArtists:
                self.displayedArtists.add(self.songs[idTrack]["artist"])
                self.ui.addArtist(self.songs[idTrack]["artist"])
            if self.songs[idTrack]["album"] not in self.displayedAlbums:
                self.displayedAlbums.add(self.songs[idTrack]["album"])
                self.ui.addAlbum(self.songs[idTrack]["album"])
            self.ui.addTrack(self.songs[idTrack])

    def call_tracks(self, QtWidget, val = 0):
        """When an album is doubleclicked on"""
        self.selectedAlbum = str(QtWidget.text(0))
        self.selectedSongs = self.albums[self.selectedAlbum] 
        
        #making the playlist from the set of songs
        self.playlist = make_neighbors(self.songs, self.selectedSongs)
        self.server.set_playlist(self.playlist)
        self.pointeur = 0
    
        self.update_tracks()

    def update_tracks(self):
        #removing elements from the album tree
        self.ui.AudioTrack.clear()

        for idTrack in self.playlist:
		self.ui.addTrack(self.songs[idTrack])
    
 

    def call_next(self):
        """The function return True if it has found a new song to play, False either"""
        self.server.set_next()
        self.ui.AudioTrack.topLevelItem(self.pointeur).setSelected(False)
        self.server.play_pause()

    def call_prev(self):
        """When previous button clicked on, convention : go to the end if at the first"""
        self.ui.AudioTrack.topLevelItem(self.pointeur).setSelected(False)
        
        #if we are not at the first element, no problem
        if self.pointeur > 0:
            self.pointeur-=1
            self.load()
        else:
            self.pointeur = len(self.playlist)-1
            self.load()
        
        #erasing the lasts elements in those mode taking into account the user didn't like the music proposed
        if self.mode == playlist or self.mode == random:
            self.playlist.pop(-1)
            self.update_tracks()
        
        self.call_play_pause()

    def call_random(self):
        if self.mode == random:
            self.mode = normal 

            #updating ui
            icon2 = QtGui.QIcon()
            icon2.addPixmap(QtGui.QPixmap((config.randomOffIcon)), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.ui.RandomButton.setIcon(icon2)
            self.ui.RandomButton.setIconSize(QtCore.QSize(30,30))
        else:
            if self.mode == playlist:
                self.call_playlist()

            self.mode = random

            #removing last elements from the playlist for it to be ready for next
            self.playlist = self.playlist[0:self.pointeur+1]

            #updating ui
            self.update_tracks()
            icon2 = QtGui.QIcon()
            icon2.addPixmap(QtGui.QPixmap((config.randomOnIcon)), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.ui.RandomButton.setIcon(icon2)
            self.ui.RandomButton.setIconSize(QtCore.QSize(30,30))

    def call_playlist(self):
        if self.mode == playlist:
       	    self.mode = normal
            self.markovienne.save_Markov()

	    #updating ui
            icon2 = QtGui.QIcon()
            icon2.addPixmap(QtGui.QPixmap((config.playlistOffIcon)), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.ui.PlaylistButton.setIcon(icon2)
            self.ui.PlaylistButton.setIconSize(QtCore.QSize(30,30))
    	else:
            if self.mode == random:
                self.call_random()
            
            self.mode = playlist
            #removing last elements from the playlist for it to be ready for next
            self.playlist = self.playlist[0:self.pointeur+1]
	    
            #save the data of the markovienne into the file 
    	    self.markovienne.save_Markov()

	    #updating ui
            self.update_tracks()
            icon2 = QtGui.QIcon()
            icon2.addPixmap(QtGui.QPixmap((config.playlistOnIcon)), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.ui.PlaylistButton.setIcon(icon2)
            self.ui.PlaylistButton.setIconSize(QtCore.QSize(30,30))
  
    def call_repeat(self):
        if self.repeat:
            self.repeat = False
            
            #updating ui
            icon2 = QtGui.QIcon()
            icon2.addPixmap(QtGui.QPixmap((config.repeatOffIcon)), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.ui.RepeatButton.setIcon(icon2)
            self.ui.RepeatButton.setIconSize(QtCore.QSize(30,30))
        else:
            self.repeat = True

            #updating ui
            icon2 = QtGui.QIcon()
            icon2.addPixmap(QtGui.QPixmap((config.repeatOnIcon)), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.ui.RepeatButton.setIcon(icon2)
            self.ui.RepeatButton.setIconSize(QtCore.QSize(30,30))

    def call_volume(self, int):
        self.server.set_volume(int * 10 / (self.ui.verticalSlider.maximum()-self.ui.verticalSlider.minimum()))

   

    def iconChange(self):
        u = self.server.is_playing()
        if u:
            icon2 = QtGui.QIcon()
            icon2.addPixmap(QtGui.QPixmap((config.pauseIcon)), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.ui.PlayButton.setIcon(icon2)
            self.ui.PlayButton.setIconSize(QtCore.QSize(30, 30))
    	else:
            icon2 = QtGui.QIcon()
            icon2.addPixmap(QtGui.QPixmap((config.playIcon)), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    	    self.ui.PlayButton.setIcon(icon2)
            self.ui.PlayButton.setIconSize(QtCore.QSize(30, 30))
  
    def runSong(self):
        self.song_play = Song()
        self.connect(self.song_play, QtCore.SIGNAL("progressUpdated"),
        self.updateSongProgress2)
        self.song_play.start()

    def updateSongProgress(self, min, max, progress):
        self.ui.SongBar.setMinimum(min)
        self.ui.SongBar.setMaximum(max)
        self.ui.SongBar.setValue(progress)
        self.ui.SongBar.repaint()

    def updateSongProgress2(self):
        self.ui.SongBar.setMinimum(0)
        try:
	    u = self.server.get_position()
	    v = self.server.get_duration()
            self.ui.SongBar.setMaximum(v)
            self.ui.SongBar.setValue(u)
	    
	    time = ""
	    if u % 60 < 10 and v % 60 < 10:
		time = str(u // 60) + " : " + "0"+str(u % 60) + " / " + str(v // 60) + " : " + "0" + str(v % 60)
	    elif u % 60 >= 10 and v % 60 < 10:
		time = str(u // 60) + " : " + str(u % 60) + " / " + str(v // 60) + " : " + "0" + str(v % 60)
	    elif u % 60 < 10 and v % 60 >= 10:
		time = str(u // 60) + " : " + "0"+str(u % 60) + " / " + str(v // 60) + " : "  + str(v % 60)
	    else:
		time = str(u // 60) + " : " + str(u % 60) + " / " + str(v // 60) + " : " +  str(v % 60)
	           
	    self.ui.SongBar.setFormat(time)
        except:
            pass
        self.ui.SongBar.repaint()
        
        try:
            if self.server.get_position() == self.server.get_duration() and self.server.get_position() > 0:
                if self.repeat:
                    self.load()
                    self.server.play_pause()
                else:
                    self.call_next()
        except:
            pass
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
        self.playlist = make_neighbors(self.songs, self.selectSongs)
        self.server.set_playlist(self.playlist)
        self.pointeur = 0
        
        #and update the ui then
        self.update_artists()


class Song(QtCore.QThread):
    __pyqtSignals__ = ("progressUpdated")
    def __init__(self):
        QtCore.QThread.__init__(self)
        self.min = 0
        self.max = 100000
        self.progress = 0
    def run(self):
	for self.progress in range(self.min, self.max):
            self.emit(QtCore.SIGNAL("progressUpdated"))
            time.sleep(0.2)  
     
        

app = QtGui.QApplication(sys.argv)
myapp = MyForm()
myapp.show()
sys.exit(app.exec_())
