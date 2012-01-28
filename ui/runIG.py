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
import random

#client lib for calling server
import xmlrpclib


class MyForm(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_ProjetGherkin()
        self.ui.setupUi(self)
        self.pointeur = 0
        self.random =False
        self.repeat = False 
    #getting in touch with server
        self.server = xmlrpclib.ServerProxy("http://localhost:" + str(config.defaultPort))

    #just to show what commands are available

    #print self.server.system.listMethods()

        self.songs = get_lib()

        for u in self.songs:
            self.ui.addTrack(u)
# l'except est present pour les fichiers n'ayant pas de titre.

    #loading song into the server
        self.server.load(self.songs[self.pointeur]['location'])
        
    
        QtCore.QObject.connect(self.ui.PlayButton, QtCore.SIGNAL("clicked()"), self.call_play_pause )
        QtCore.QObject.connect(self.ui.AudioTrack, QtCore.SIGNAL("itemDoubleClicked(QTreeWidgetItem*,int)"), self.call_load )
        QtCore.QObject.connect(self.ui.NextButton, QtCore.SIGNAL("clicked()"), self.call_next)
        QtCore.QObject.connect(self.ui.PreviousButton, QtCore.SIGNAL("clicked()"), self.call_prev)
        QtCore.QObject.connect(self.ui.RandomButton, QtCore.SIGNAL("clicked()"), self.call_random)
        QtCore.QObject.connect(self.ui.RepeatButton,QtCore.SIGNAL("clicked()"), self.call_repeat)
    #playing song
    #s.play_pause()

    def add_entry(self):
        self.ui.lineEdit.selectAll()
        self.ui.lineEdit.cut()
        self.ui.textEdit.append("")
        self.ui.textEdit.paste()

    def call_play_pause(self):
        self.server.play_pause()
        self.iconChange()
        self.pushProgressBar()

    def call_load(self, QtWidget, val = 0):
        self.server.stop()
        self.iconChange()
        s = str(QtWidget.text(3))
        self.pointeur = int(QtWidget.text(4))
        self.server.load(s)
        self.server.play_pause()

    def call_next(self):
        self.server.stop()
        self.iconChange()
        if self.random == False:
            self.pointeur+=1
            self.server.load(self.songs[self.pointeur]['location'])
            print self.songs[self.pointeur]['title']
        else:
# On est en mode random, donc on fait n'importe quoi.
            self.pointeur = random.randint(0, self.songs[-1]['id'])
            self.server.load(self.songs[self.pointeur]['location'])
            print self.songs[self.pointeur]['title']

        self.server.play_pause()


    def call_prev(self):
        self.server.stop()
        self.iconChange()
        if not self.random:
            self.pointeur-=1
            self.server.load(self.songs[self.pointeur]['location'])
        else:
            self.pointeur = random.randint(0,self.songs[-1]['id'])
            self.server.load(self.songs[self.pointeur]['location'])

        self.server.play_pause()

    def call_random(self):
        if self.random:
            self.random = False
        else:
            self.random = True
    
    def call_repeat(self):
        if self.repeat:
            self.repeat = False
        else:
            self.repeat = True

    def pushBar(self, dt):
        u = self.ui.SongBar.value()
        self.ui.SongBar.setValue(u + 100*dt/180)#self.server.get_duration())
        self.ui.SongBar.repaint()
      
 #   def pushProgressBar(self):
 #       u = self.server.is_playing()
 #       print u
 #       if u:
 #           time.sleep(config.dt)
 #           self.pushBar(config.dt)
 #           self.pushProgressBar()
 #       else:
 #           pass

    def iconChange(self):
        u = self.server.is_playing()
        print u
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
  
        
        

app = QtGui.QApplication(sys.argv)
myapp = MyForm()
myapp.show()
sys.exit(app.exec_())
