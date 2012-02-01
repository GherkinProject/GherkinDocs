# -*- coding: utf-8 -*-
#!/usr/bin/python -d
 
from PyQt4 import QtCore, QtGui
from testIG import Ui_ProjetGherkin
import sys

#local lib : loading db
from load_db import *

#configuration constant
import config

#config file
import time
from random import randint

#client lib for calling server
import xmlrpclib

normal = 0
random = 1
playlist = 2

class MyForm(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_ProjetGherkin()
        self.ui.setupUi(self)
        self.pointeur = 0
        self.playlist = []
        self.mode = normal
        self.repeat = False

        #connection with the server
        self.server = xmlrpclib.ServerProxy("http://localhost:" + str(config.defaultPort))

        (self.artists, self.albums, self.songs) = get_lib()
        #print self.artists
        #print self.albums
        
        self.display_all()
        #l'except est present pour les fichiers n'ayant pas de titre.

        #loading song into the server
        self.server.load(self.songs[self.pointeur]['location'])
        
        #signal received, functions called
        QtCore.QObject.connect(self.ui.PlayButton, QtCore.SIGNAL("clicked()"), self.call_play_pause )
        QtCore.QObject.connect(self.ui.AudioTrack, QtCore.SIGNAL("itemActivated(QTreeWidgetItem*,int)"), self.call_load )
        QtCore.QObject.connect(self.ui.Artist, QtCore.SIGNAL("itemClicked(QTreeWidgetItem*,int)"), self.call_albums )
        QtCore.QObject.connect(self.ui.Album, QtCore.SIGNAL("itemClicked(QTreeWidgetItem*,int)"), self.call_tracks )
        QtCore.QObject.connect(self.ui.NextButton, QtCore.SIGNAL("clicked()"), self.call_next)
        QtCore.QObject.connect(self.ui.PreviousButton, QtCore.SIGNAL("clicked()"), self.call_prev)
        QtCore.QObject.connect(self.ui.RandomButton, QtCore.SIGNAL("clicked()"), self.call_random)
        QtCore.QObject.connect(self.ui.RepeatButton,QtCore.SIGNAL("clicked()"), self.call_repeat)
#        QtCore.QObject.connect(self.ui.verticalSlider, QtCore.SIGNAL("valueChanged(int)"), self.call_volume )	

    def add_entry(self):
        self.ui.lineEdit.selectAll()
        self.ui.lineEdit.cut()
        self.ui.textEdit.append("")
        self.ui.textEdit.paste()

    def call_play_pause(self):
        self.server.play_pause()
     	self.runSong()
        self.iconChange()
        self.ui.AudioTrack.topLevelItem(self.pointeur).setSelected(True)

    def call_load(self, QtWidget, val = 0):
        idSong = int(QtWidget.text(4))
        
        #arret de la lecture
        self.server.stop()

        #déselection graphique de la chanson
        self.ui.AudioTrack.topLevelItem(self.pointeur).setSelected(False)
        
        #on trouve la chanson choisie dans la playlist
        while self.playlist[self.pointeur] != idSong:
            self.pointeur += 1

        #chargement puis lancement de la musique
        self.server.load(self.songs[idSong]["location"])
        self.server.play_pause()
        
        #affichage graphique
    	self.iconChange()
        self.runSong()
        self.ui.AudioTrack.topLevelItem(self.pointeur).setSelected(True)
    
    def display_all(self):
        self.ui.Artist.clear()
        self.ui.Album.clear()
        self.ui.AudioTrack.clear()
        artists = self.artists.keys()
        artists.sort()
        for artist in artists:
            self.ui.addArtist(artist)
            albums = list(self.artists[artist])
            albums.sort()
            for album in albums:
                self.ui.addAlbum(album)
 

    def call_albums(self, QtWidget, val = 0):
        self.selectedArtist = str(QtWidget.text(0))
        self.selectedSongs = set()
        
        for album in self.artists[self.selectedArtist]:
            for idTrack in self.albums[album]:
                self.selectedSongs.add(idTrack)
        
        self.playlist = make_neighbors(self.songs, self.selectedSongs)
        self.pointeur = 0

        self.update_albums()
    
    def update_albums(self):
        #removing elements from the album tree
        self.ui.Album.clear()
        self.ui.AudioTrack.clear()

        self.displayedAlbums = set()
        for idTrack in self.playlist:
            if self.songs[idTrack]["album"] not in self.displayedAlbums:
                self.displayedAlbums.add(self.songs[idTrack]["album"])
                self.ui.addAlbum(self.songs[idTrack]["album"])
            self.ui.addTrack(self.songs[idTrack])
    
    def call_tracks(self, QtWidget, val = 0):
        self.selectedAlbum = str(QtWidget.text(0))
        self.selectedSongs = self.albums[self.selectedAlbum] 
        
        self.playlist = make_neighbors(self.songs, self.selectedSongs)
        self.pointeur = 0
    
        self.update_tracks()

    def update_tracks(self):
        #removing elements from the album tree
        self.ui.AudioTrack.clear()

        for idTrack in self.playlist:
            self.ui.addTrack(self.songs[idTrack])
    
 

    def call_next(self):
        """The function return True if it has found a new song to play, False either"""
        
        self.server.stop()
        self.ui.AudioTrack.topLevelItem(self.pointeur).setSelected(False)
        if self.mode == normal:
            if self.pointeur < len(self.playlist) - 1:
                self.pointeur+=1
                self.server.load(self.songs[self.playlist[self.pointeur]]['location'])
            else:
                self.pointeur = 0
                self.server.stop()

                return False
        else:
            if self.mode == random:
                #choosing a random number in the list of possible song
                posSong = randint(0, len(self.songs))
                idSong = self.songs.keys()[posSong] 
            elif self.mode == playlist:
                idSong = Markovienne(self.proba[self.playlist[self.pointeur]])
            #adding the song to the playlist
            self.playlist.append(idSong)
            
            #pointing on the new song
            self.pointeur += 1

            #displaying the track to the playlist
            self.ui.addTrack(self.songs[self.playlist[-1]])
            self.server.load(self.songs[self.playlist[self.pointeur]]['location'])

        self.server.play_pause()
        self.iconChange()
        self.runSong()
        self.ui.AudioTrack.topLevelItem(self.pointeur).setSelected(True)

        return True

    def call_prev(self):
        self.server.stop()
        self.ui.AudioTrack.topLevelItem(self.pointeur).setSelected(False)
        
        if self.pointeur > 0:
            self.pointeur-=1
            self.server.load(self.songs[self.playlist[self.pointeur]]['location'])
        else:
            self.pointeur = len(self.playlist)-1
            self.server.load(self.songs[self.playlist[self.pointeur]]['location'])

        if self.mode == playlist or self.mode == random:
            self.playlist.pop(-1)
            self.update_tracks()
        
        self.server.play_pause()
        self.iconChange()
        self.runSong()
        self.ui.AudioTrack.topLevelItem(self.pointeur).setSelected(True)

    def call_random(self):
        if self.mode == random:
            self.mode = random
            icon2 = QtGui.QIcon()
            icon2.addPixmap(QtGui.QPixmap((config.randomOffIcon)), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.ui.RandomButton.setIcon(icon2)
            self.ui.RandomButton.setIconSize(QtCore.QSize(30,30))
        else:
            self.mode = random
            self.playlist = self.playlist[0:self.pointeur+1]
            self.update_tracks()
            icon2 = QtGui.QIcon()
            icon2.addPixmap(QtGui.QPixmap((config.randomOnIcon)), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.ui.RandomButton.setIcon(icon2)
            self.ui.RandomButton.setIconSize(QtCore.QSize(30,30))
    
    def call_repeat(self):
        if self.repeat:
            self.repeat = False
            icon2 = QtGui.QIcon()
            icon2.addPixmap(QtGui.QPixmap((config.repeatOffIcon)), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.ui.RepeatButton.setIcon(icon2)
            self.ui.RepeatButton.setIconSize(QtCore.QSize(30,30))
        else:
            self.repeat = True
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
            self.ui.SongBar.setMaximum(self.server.get_duration())
            self.ui.SongBar.setValue(self.server.get_position())
        except:
            pass
        self.ui.SongBar.repaint()
        try:
            if (self.server.get_position() == self.server.get_duration() and self.server.get_position() > 0):
                self.call_next()
                if self.repeat:
                    self.call_prev()
                if not self.server.is_playing():
                    self.server.play_pause()
                    self.iconChange()
                else:
                    self.iconChange()
            else:
                pass
        except:
            pass



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
