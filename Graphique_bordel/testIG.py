# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Gherkin.ui'
#
# Created: Wed Jan 11 11:53:46 2012
#      by: PyQt4 UI code generator 4.8.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

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
        self.centralwidget = QtGui.QWidget(ProjetGherkin)
        self.centralwidget.setAcceptDrops(False)
        self.centralwidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.centralwidget.setAutoFillBackground(True)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setSizeConstraint(QtGui.QLayout.SetNoConstraint)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.Playlist = QtGui.QTreeWidget(self.centralwidget)
        self.Playlist.setObjectName(_fromUtf8("Playlist"))
        self.Playlist.headerItem().setText(0, QtGui.QApplication.translate("ProjetGherkin", "Playlist", None, QtGui.QApplication.UnicodeUTF8))
        self.Playlist.headerItem().setTextAlignment(0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.gridLayout.addWidget(self.Playlist, 4, 0, 8, 1)
        self.Album = QtGui.QTreeWidget(self.centralwidget)
        self.Album.setObjectName(_fromUtf8("Album"))
        self.Album.headerItem().setText(0, QtGui.QApplication.translate("ProjetGherkin", "Album", None, QtGui.QApplication.UnicodeUTF8))
        self.Album.headerItem().setTextAlignment(0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.gridLayout.addWidget(self.Album, 4, 2, 4, 1)
        self.Artist = QtGui.QTreeWidget(self.centralwidget)
        self.Artist.setObjectName(_fromUtf8("Artiste"))
        self.Artist.headerItem().setText(0, QtGui.QApplication.translate("ProjetGherkin", "Artiste", None, QtGui.QApplication.UnicodeUTF8))
        self.Artist.headerItem().setTextAlignment(0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.gridLayout.addWidget(self.Artist, 4, 1, 4, 1)
        self.RandomButton = QtGui.QPushButton(self.centralwidget)
        self.RandomButton.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("Random.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.RandomButton.setIcon(icon)
        self.RandomButton.setIconSize(QtCore.QSize(30, 30))
        self.RandomButton.setFlat(True)
        self.RandomButton.setObjectName(_fromUtf8("RandomButton"))
        self.RandomRepeat = QtGui.QButtonGroup(ProjetGherkin)
        self.RandomRepeat.setObjectName(_fromUtf8("RandomRepeat"))
        self.RandomRepeat.addButton(self.RandomButton)
        self.gridLayout.addWidget(self.RandomButton, 3, 3, 1, 1)
        self.AudioTrack = QtGui.QTreeWidget(self.centralwidget)
        self.AudioTrack.setObjectName(_fromUtf8("AudioTrack"))
        self.AudioTrack.headerItem().setText(0, QtGui.QApplication.translate("ProjetGherkin", "Piste audio", None, QtGui.QApplication.UnicodeUTF8))
        self.AudioTrack.headerItem().setTextAlignment(0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
	self.AudioTrack.headerItem().setText(1, QtGui.QApplication.translate("ProjetGherkin", "id", None, QtGui.QApplication.UnicodeUTF8))
        self.gridLayout.addWidget(self.AudioTrack, 8, 1, 4, 2)
        self.verticalSlider = QtGui.QSlider(self.centralwidget)
        self.verticalSlider.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider.setTickPosition(QtGui.QSlider.TicksBelow)
        self.verticalSlider.setObjectName(_fromUtf8("verticalSlider"))
        self.gridLayout.addWidget(self.verticalSlider, 11, 3, 1, 1)
        self.LookingFor = QtGui.QLineEdit(self.centralwidget)
        self.LookingFor.setText(_fromUtf8(""))
        self.LookingFor.setReadOnly(False)
        self.LookingFor.setObjectName(_fromUtf8("LookingFor"))
        self.gridLayout.addWidget(self.LookingFor, 3, 2, 1, 1)
        self.LookingForNoTouch = QtGui.QLineEdit(self.centralwidget)
        self.LookingForNoTouch.setText(QtGui.QApplication.translate("ProjetGherkin", "Recherche :", None, QtGui.QApplication.UnicodeUTF8))
        self.LookingForNoTouch.setReadOnly(True)
        self.LookingForNoTouch.setObjectName(_fromUtf8("LookingForNoTouch"))
        self.gridLayout.addWidget(self.LookingForNoTouch, 3, 1, 1, 1)
        self.NextButton = QtGui.QPushButton(self.centralwidget)
        self.NextButton.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8("forward.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.NextButton.setIcon(icon1)
        self.NextButton.setIconSize(QtCore.QSize(30, 30))
        self.NextButton.setAutoDefault(False)
        self.NextButton.setDefault(False)
        self.NextButton.setFlat(True)
        self.NextButton.setObjectName(_fromUtf8("NextButton"))
        self.PlayPN = QtGui.QButtonGroup(ProjetGherkin)
        self.PlayPN.setObjectName(_fromUtf8("PlayPN"))
        self.PlayPN.addButton(self.NextButton)
        self.gridLayout.addWidget(self.NextButton, 9, 3, 1, 1)
        self.PlayButton = QtGui.QPushButton(self.centralwidget)
        self.PlayButton.setText(_fromUtf8(""))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8("play.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
	icon2.addPixmap(QtGui.QPixmap(_fromUtf8("pause.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.PlayButton.setIcon(icon2)
        self.PlayButton.setIconSize(QtCore.QSize(30, 30))
        self.PlayButton.setFlat(True)
        self.PlayButton.setObjectName(_fromUtf8("PlayButton"))
        self.PlayPN.addButton(self.PlayButton)
        self.gridLayout.addWidget(self.PlayButton, 8, 3, 1, 1)
        self.PreviousButton = QtGui.QPushButton(self.centralwidget)
        self.PreviousButton.setText(_fromUtf8(""))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8("backward.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.PreviousButton.setIcon(icon3)
        self.PreviousButton.setIconSize(QtCore.QSize(30, 30))
        self.PreviousButton.setFlat(True)
        self.PreviousButton.setObjectName(_fromUtf8("PreviousButton"))
        self.PlayPN.addButton(self.PreviousButton)
        self.gridLayout.addWidget(self.PreviousButton, 7, 3, 1, 1)
        self.RepeatButton = QtGui.QPushButton(self.centralwidget)
        self.RepeatButton.setText(_fromUtf8(""))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8("Repeat.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.RepeatButton.setIcon(icon4)
        self.RepeatButton.setIconSize(QtCore.QSize(30, 30))
        self.RepeatButton.setFlat(True)
        self.RepeatButton.setObjectName(_fromUtf8("RepeatButton"))
        self.RandomRepeat.addButton(self.RepeatButton)
        self.gridLayout.addWidget(self.RepeatButton, 4, 3, 1, 1)
        self.SongBar = QtGui.QSlider(self.centralwidget)
        self.SongBar.setOrientation(QtCore.Qt.Horizontal)
        self.SongBar.setObjectName(_fromUtf8("SongBar"))
        self.gridLayout.addWidget(self.SongBar, 2, 1, 1, 2)
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setText(_fromUtf8(""))
        self.label.setPixmap(QtGui.QPixmap(_fromUtf8("Cornichon.png")))
        self.label.setScaledContents(True)
        self.label.setWordWrap(False)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 4, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 10, 3, 1, 1)
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
        self.actionImporter_Fichier = QtGui.QAction(ProjetGherkin)
        self.actionImporter_Fichier.setText(QtGui.QApplication.translate("ProjetGherkin", "Importer Fichier", None, QtGui.QApplication.UnicodeUTF8))
        self.actionImporter_Fichier.setObjectName(_fromUtf8("actionImporter_Fichier"))
        self.actionPr_f_rence = QtGui.QAction(ProjetGherkin)
        self.actionPr_f_rence.setText(QtGui.QApplication.translate("ProjetGherkin", "Préférence", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPr_f_rence.setObjectName(_fromUtf8("actionPr_f_rence"))
        self.menuMedia.addAction(self.actionImporter_Dossier)
        self.menuMedia.addAction(self.actionImporter_Fichier)
        self.menuEdition.addAction(self.actionPr_f_rence)
        self.MenuBarPG.addAction(self.menuMedia.menuAction())
        self.MenuBarPG.addAction(self.menuAffichage.menuAction())
        self.MenuBarPG.addAction(self.menuEdition.menuAction())


    def changePlay(self):
        if self.isPlaying == True:
            self.isPlaying = False
        else:
            self.isPlaying = True
 


    def iconChange(self):
        self.changePlay()
        if self.isPlaying:
            icon2 = QtGui.QIcon()
            icon2.addPixmap(QtGui.QPixmap(_fromUtf8("pause.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.PlayButton.setIcon(icon2)
            self.PlayButton.setIconSize(QtCore.QSize(30, 30))
    	else:
            icon2 = QtGui.QIcon()
            icon2.addPixmap(QtGui.QPixmap(_fromUtf8("play.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    	    self.PlayButton.setIcon(icon2)
            self.PlayButton.setIconSize(QtCore.QSize(30, 30))
        




#        QtCore.QMetaObject.connectSlotsByName(ProjetGherkin)

    def retranslateUi(self, ProjetGherkin):
        pass

    def addAlbum(self,album):
        item_0 = QtGui.QTreeWidgetItem(self.Album)
        self.Album.topLevelItem(self.iteratorAlbum).setText(0, QtGui.QApplication.translate("ProjetGherkin", album, None, QtGui.QApplication.UnicodeUTF8))
        self.iteratorAlbum+=1

    def addArtist(self,artist):
        item_0 = QtGui.QTreeWidgetItem(self.Artist)
        self.Artist.topLevelItem(self.iteratorArtist).setText(0, QtGui.QApplication.translate("ProjetGherkin", artist, None, QtGui.QApplication.UnicodeUTF8))
        self.iteratorArtist+=1

    def addTrack(self,u,v):
#        item_0 = QtGui.QTreeWidgetItem(self.AudioTrack)
#        self.AudioTrack.topLevelItem(self.iteratorAudioTrack).setText(0, QtGui.QApplication.translate("ProjetGherkin", u['title'], None, QtGui.QApplication.UnicodeUTF8))
#        self.AudioTrack.topLevelItem(self.iteratorAudioTrack).setText(1, QtGui.QApplication.translate("ProjetGherkin", str(u['id']), None, QtGui.QApplication.UnicodeUTF8))
#        self.iteratorAudioTrack+=1
        item_0 = QtGui.QTreeWidgetItem()
        item_0.setText(0,u)
        item_1 = QtGui.QTreeWidgetItem()
        item_1.setText(0,v)
        item_1.setHidden(True)
        item_0.addChild(item_1)
        print item_0.text(0)
        self.AudioTrack.addTopLevelItem(item_0)
        

    def addPlaylist(self,playlist):
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
