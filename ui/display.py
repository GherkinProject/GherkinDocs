# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Gherkin.ui'
#
# Created: Wed Jan 11 11:53:46 2012
#      by: PyQt4 UI code generator 4.8.5
#

from PyQt4 import QtCore, QtGui
from time import *

#configuration constant
from configUi import *

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

tracknumber = 0
title = 1
album = 2
artist = 3
id = 4
location = 5

class Ui_ProjetGherkin(object):
    def setupUi(self, ProjetGherkin):
    	self.iteratorPlaylist = 0
        self.iteratorArtist = 0
        self.iteratorAlbum = 0
        self.iteratorAudioTrack = 0
    	self.isPlaying = False   

        ProjetGherkin.setObjectName(_fromUtf8("ProjetGherkin"))
        ProjetGherkin.resize(640, 480)
        ProjetGherkin.setWindowTitle(QtGui.QApplication.translate("ProjetGherkin", "Projet Gherkin", None, QtGui.QApplication.UnicodeUTF8))
        ProjetGherkin.setWindowOpacity(1.0)
        ProjetGherkin.setWindowIcon(QtGui.QIcon(config.gherkinIcon))
        self.centralwidget = QtGui.QWidget(ProjetGherkin)
        self.centralwidget.setAcceptDrops(False)
        self.centralwidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.centralwidget.setAutoFillBackground(True)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setSizeConstraint(QtGui.QLayout.SetNoConstraint)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        
        # Album        

        self.Album = QtGui.QTreeWidget(self.centralwidget)
        self.Album.setObjectName(_fromUtf8("Albums"))
        self.Album.headerItem().setText(0, QtGui.QApplication.translate("ProjetGherkin", "Albums", None, QtGui.QApplication.UnicodeUTF8))
        self.Album.headerItem().setTextAlignment(0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.gridLayout.addWidget(self.Album, 4, 2, 5 , 1)
        self.Album.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.Album.header().setClickable(True)
        
        #Artist        

        self.Artist = QtGui.QTreeWidget(self.centralwidget)
        self.Artist.setObjectName(_fromUtf8("Artists"))
        self.Artist.headerItem().setText(0, QtGui.QApplication.translate("ProjetGherkin", "Artistes", None, QtGui.QApplication.UnicodeUTF8))
        self.Artist.headerItem().setTextAlignment(0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.gridLayout.addWidget(self.Artist, 4, 1, 5, 1)
        self.Artist.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.Artist.header().setClickable(True)

        #AudioTrack        

        self.AudioTrack = QtGui.QTreeWidget(self.centralwidget)
        self.AudioTrack.setObjectName(_fromUtf8("AudioTrack"))
        self.AudioTrack.headerItem().setText(tracknumber, QtGui.QApplication.translate("ProjetGherkin", "Piste", None, QtGui.QApplication.UnicodeUTF8))
        self.AudioTrack.headerItem().setTextAlignment(tracknumber, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.AudioTrack.headerItem().setText(title, QtGui.QApplication.translate("ProjetGherkin", "Titre", None, QtGui.QApplication.UnicodeUTF8))
        self.AudioTrack.headerItem().setTextAlignment(title, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.AudioTrack.headerItem().setText(artist, QtGui.QApplication.translate("ProjetGherkin", "Artiste", None, QtGui.QApplication.UnicodeUTF8))
        self.AudioTrack.headerItem().setTextAlignment(artist, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.AudioTrack.headerItem().setText(album, QtGui.QApplication.translate("ProjetGherkin", "Album", None, QtGui.QApplication.UnicodeUTF8))
        self.AudioTrack.headerItem().setTextAlignment(album, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.AudioTrack.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)


        self.RandomButton = QtGui.QPushButton(self.centralwidget)
        self.RandomButton.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(config.randomOffIcon)), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.RandomButton.setIcon(icon)
        self.RandomButton.setIconSize(QtCore.QSize(30, 30))
        self.RandomButton.setFlat(True)
        self.RandomButton.setObjectName(_fromUtf8("RandomButton"))
        self.RandomRepeat = QtGui.QButtonGroup(ProjetGherkin)
        self.RandomRepeat.setObjectName(_fromUtf8("RandomRepeat"))
        self.RandomRepeat.addButton(self.RandomButton)
        self.gridLayout.addWidget(self.RandomButton, 4, 3, 1, 1)
        

        self.gridLayout.addWidget(self.AudioTrack, 9, 1, 5, 2)
        self.verticalSlider = QtGui.QSlider(self.centralwidget)
        self.verticalSlider.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider.setTickPosition(QtGui.QSlider.TicksBelow)
        self.verticalSlider.setObjectName(_fromUtf8("verticalSlider"))
        self.gridLayout.addWidget(self.verticalSlider, 13, 3, 1, 1 )




        self.LookingFor = QtGui.QLineEdit(self.centralwidget)
        self.LookingFor.setText(_fromUtf8(""))
        self.LookingFor.setReadOnly(False)
        self.LookingFor.setObjectName(_fromUtf8("LookingFor"))
        self.LookingFor.setPlaceholderText("Recherche")
        self.gridLayout.addWidget(self.LookingFor, 3, 2, 1, 1)


        #self.LookingForNoTouch = QtGui.QLineEdit(self.centralwidget)
        #self.LookingForNoTouch.setText(QtGui.QApplication.translate("ProjetGherkin", "Nom de la chanson", None, QtGui.QApplication.UnicodeUTF8))
        #self.LookingForNoTouch.setAlignment(QtCore.Qt.AlignCenter)
        #self.LookingForNoTouch.setReadOnly(True)
        #self.LookingForNoTouch.setObjectName(_fromUtf8("LookingForNoTouch"))

        self.LookingForNoTouch = QtGui.QCommandLinkButton(self.centralwidget)
        self.LookingForNoTouch.setCheckable(True)
        self.LookingForNoTouch.setText(QtGui.QApplication.translate("ProjetGherkin", "Pas de titre en cours", None, QtGui.QApplication.UnicodeUTF8))
        self.LookingForNoTouch.setObjectName(_fromUtf8("SongName"))
        self.gridLayout.addWidget(self.LookingForNoTouch, 3, 1, 1, 1)


        self.NextButton = QtGui.QPushButton(self.centralwidget)
        self.NextButton.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(config.nextIcon)), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.NextButton.setIcon(icon1)
        self.NextButton.setIconSize(QtCore.QSize(30, 30))
        self.NextButton.setAutoDefault(False)
        self.NextButton.setDefault(False)
        self.NextButton.setFlat(True)
        self.NextButton.setObjectName(_fromUtf8("NextButton"))


        self.PlayPN = QtGui.QButtonGroup(ProjetGherkin)
        self.PlayPN.setObjectName(_fromUtf8("PlayPN"))
        self.PlayPN.addButton(self.NextButton)
        self.gridLayout.addWidget(self.NextButton, 10, 3, 1, 1)

        self.PlayButton = QtGui.QPushButton(self.centralwidget)
        self.PlayButton.setText(_fromUtf8(""))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(config.playIcon)), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.PlayButton.setIcon(icon2)
        self.PlayButton.setIconSize(QtCore.QSize(30, 30))
        self.PlayButton.setFlat(True)
        self.PlayButton.setObjectName(_fromUtf8("PlayButton"))
        self.PlayPN.addButton(self.PlayButton)
        self.gridLayout.addWidget(self.PlayButton, 9, 3, 1, 1)

        self.PreviousButton = QtGui.QPushButton(self.centralwidget)
        self.PreviousButton.setText(_fromUtf8(""))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(config.prevIcon)), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.PreviousButton.setIcon(icon3)
        self.PreviousButton.setIconSize(QtCore.QSize(30, 30))
        self.PreviousButton.setFlat(True)
        self.PreviousButton.setObjectName(_fromUtf8("PreviousButton"))
        self.PlayPN.addButton(self.PreviousButton)
        self.gridLayout.addWidget(self.PreviousButton, 7, 3, 1, 1)

        self.RepeatButton = QtGui.QPushButton(self.centralwidget)
        self.RepeatButton.setText(_fromUtf8(""))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8(config.repeatOffIcon)), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.RepeatButton.setIcon(icon4)
        self.RepeatButton.setIconSize(QtCore.QSize(30, 30))
        self.RepeatButton.setFlat(True)
        self.RepeatButton.setObjectName(_fromUtf8("RepeatButton"))
        self.RandomRepeat.addButton(self.RepeatButton)

	self.PlaylistButton = QtGui.QPushButton(self.centralwidget)
	self.PlaylistButton.setText(_fromUtf8(""))
	icon5 = QtGui.QIcon()
	icon5.addPixmap(QtGui.QPixmap(_fromUtf8(config.playlistOffIcon)), QtGui.QIcon.Normal, QtGui.QIcon.Off)
	self.PlaylistButton.setIcon(icon5)
	self.PlaylistButton.setIconSize(QtCore.QSize(30, 30))
	self.PlaylistButton.setFlat(True)
	self.PlaylistButton.setObjectName(_fromUtf8("PlaylistButton"))
	self.RandomRepeat.addButton(self.PlaylistButton)

        self.gridLayout.addWidget(self.RepeatButton, 3, 3, 1, 1)
	self.gridLayout.addWidget(self.PlaylistButton, 5,3,1,1)

        self.SongBar = QtGui.QProgressBar(self.centralwidget)
        self.SongBar.setObjectName(_fromUtf8("SongBar"))
	self.SongBar.setFormat('%v')
        self.gridLayout.addWidget(self.SongBar, 2, 1, 1, 2)
	


        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 12, 3, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 6, 3, 1, 1)

        ProjetGherkin.setCentralWidget(self.centralwidget)
        self.MenuBarPG = QtGui.QMenuBar(ProjetGherkin)
        self.MenuBarPG.setGeometry(QtCore.QRect(0, 0, 640, 25))
        self.MenuBarPG.setFocusPolicy(QtCore.Qt.NoFocus)
        self.MenuBarPG.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.MenuBarPG.setAutoFillBackground(False)
        self.MenuBarPG.setDefaultUp(False)
        self.MenuBarPG.setNativeMenuBar(False)
        self.MenuBarPG.setObjectName(_fromUtf8("MenuBarPG"))
        self.menuMedia = QtGui.QMenu(self.MenuBarPG)
        self.menuMedia.setTitle(QtGui.QApplication.translate("ProjetGherkin", "Media", None, QtGui.QApplication.UnicodeUTF8))
        self.menuMedia.setObjectName(_fromUtf8("menuMedia"))
        self.menuAffichage = QtGui.QMenu(self.MenuBarPG)
        self.menuAffichage.setTitle(QtGui.QApplication.translate("ProjetGherkin", "Affichage", None, QtGui.QApplication.UnicodeUTF8))
        self.menuAffichage.setObjectName(_fromUtf8("menuAffichage"))
        self.menuEdition = QtGui.QMenu(self.MenuBarPG)
        self.menuEdition.setTitle(QtGui.QApplication.translate("ProjetGherkin", "Edition", None, QtGui.QApplication.UnicodeUTF8))
        self.menuEdition.setObjectName(_fromUtf8("menuEdition"))
        ProjetGherkin.setMenuBar(self.MenuBarPG)
        self.statusbar = QtGui.QStatusBar(ProjetGherkin)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        ProjetGherkin.setStatusBar(self.statusbar)
        self.actionImporter_Dossier = QtGui.QAction(ProjetGherkin)
        self.actionImporter_Dossier.setText(QtGui.QApplication.translate("ProjetGherkin", "Importer Dossier", None, QtGui.QApplication.UnicodeUTF8))
        self.actionImporter_Dossier.setObjectName(_fromUtf8("actionImporter_Dossier"))
        self.actionChercher_Serveur = QtGui.QAction(ProjetGherkin)
        self.actionChercher_Serveur.setText(QtGui.QApplication.translate("ProjetGherkin", "Chercher un serveur", None, QtGui.QApplication.UnicodeUTF8))
        self.actionChercher_Serveur.setObjectName(_fromUtf8("actionChercher_Serveur"))
        self.actionPr_f_rence = QtGui.QAction(ProjetGherkin)
        self.actionPr_f_rence.setText(QtGui.QApplication.translate("ProjetGherkin", "Préférence", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPr_f_rence.setObjectName(_fromUtf8("actionPr_f_rence"))
        self.menuMedia.addAction(self.actionImporter_Dossier)
        self.menuMedia.addAction(self.actionChercher_Serveur)
        self.menuEdition.addAction(self.actionPr_f_rence)
        self.MenuBarPG.addAction(self.menuMedia.menuAction())
        self.MenuBarPG.addAction(self.menuAffichage.menuAction())
        self.MenuBarPG.addAction(self.menuEdition.menuAction())

 


       




#        QtCore.QMetaObject.connectSlotsByName(ProjetGherkin)

    def retranslateUi(self, ProjetGherkin):
        pass

    def addAlbum(self, albumName):
        itemAT=QtGui.QTreeWidgetItem()
        try:
            itemAT.setText(0, albumName)
        except:
            itemAT.setText(0,config.defaultUnknown)
        self.Album.addTopLevelItem(itemAT)

    def addArtist(self, artistName):
        itemAT=QtGui.QTreeWidgetItem()
        try:
            itemAT.setText(0, artistName)
        except:
            itemAT.setText(0,config.defaultUnknown)
        self.Artist.addTopLevelItem(itemAT)

    def addTrack(self,u):
#        item_0 = QtGui.QTreeWidgetItem(self.AudioTrack)
#        self.AudioTrack.topLevelItem(self.iteratorAudioTrack).setText(0, QtGui.QApplication.translate("ProjetGherkin", u['title'], None, QtGui.QApplication.UnicodeUTF8))
#        self.AudioTrack.topLevelItem(self.iteratorAudioTrack).setText(1, QtGui.QApplication.translate("ProjetGherkin", str(u['id']), None, QtGui.QApplication.UnicodeUTF8))
               
        itemAT=QtGui.QTreeWidgetItem()
        try:
            itemAT.setText(tracknumber, str(u['tracknumber']))
        except:
            itemAT.setText(tracknumber, config.defaultUnknown)
        try:
            itemAT.setText(title, u['title'])
        except:
            itemAT.setText(title, config.defaultUnknown)
        try:
            itemAT.setText(artist, u['artist'])
        except:
            itemAT.setText(artist, config.defaultUnknown)
        try:
            itemAT.setText(album, u['album'])
        except:
            itemAT.setText(album, config.defaultUnknown)

        itemAT.setText(location, u['location'])
        itemAT.setText(id, u['id'])
        self.AudioTrack.addTopLevelItem(itemAT)
 

    def addPlaylist(self,u):
    	item_0 = QtGui.QTreeWidgetItem(self.Playlist)
        self.Playlist.topLevelItem(self.iteratorPlaylist).setText(0, QtGui.QApplication.translate("ProjetGherkin", playlist, None, QtGui.QApplication.UnicodeUTF8))
        self.iteratorPlaylist=1

   

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ProjetGherkin = QtGui.QMainWindow()
    ui = Ui_ProjetGherkin()
    ui.setupUi(ProjetGherkin)
    ProjetGherkin.show()
    sys.exit(app.exec_())
